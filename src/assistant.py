"""Orquestra segurança, intenções, FAQ, simulações e IA generativa."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Sequence

from .finance import (
    compound_interest,
    format_simulation,
    loan_payment,
    monthly_savings_for_goal,
)
from .generative import OpenAIGenerativeResponder
from .knowledge_base import KnowledgeBase
from .models import AssistantReply
from .safety import (
    contains_guarantee_request,
    financial_disclaimer,
    find_sensitive_data,
    normalize_text,
    privacy_warning,
)


def parse_pt_number(raw: str) -> float:
    """Converte números comuns em português para float."""

    cleaned = raw.strip().replace("R$", "").replace(" ", "")
    if not cleaned:
        raise ValueError("número vazio")

    if "." in cleaned and "," in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    elif "," in cleaned:
        cleaned = cleaned.replace(",", ".")
    elif cleaned.count(".") > 1:
        cleaned = cleaned.replace(".", "")
    elif "." in cleaned:
        left, right = cleaned.split(".", 1)
        if len(right) == 3 and len(left) >= 1:
            cleaned = left + right

    return float(cleaned)


def _extract_numbers(text: str) -> list[float]:
    raw_numbers = re.findall(r"(?:R\$\s*)?\d+(?:[.,]\d+)*", text, flags=re.IGNORECASE)
    return [parse_pt_number(value) for value in raw_numbers]


class FinancialAssistant:
    """Assistente financeiro educacional com fallback totalmente local."""

    def __init__(
        self,
        faq_path: str | Path | None = None,
        generative_responder: OpenAIGenerativeResponder | None = None,
    ) -> None:
        self.knowledge_base = KnowledgeBase(faq_path) if faq_path else KnowledgeBase()
        self.generative = generative_responder or OpenAIGenerativeResponder()

    def _simulation_answer(self, message: str) -> tuple[str, str] | None:
        normalized = normalize_text(message)
        numbers = _extract_numbers(message)

        is_goal = any(
            term in normalized
            for term in ("meta", "guardar por mes", "economizar", "alcancar")
        )
        is_loan = any(
            term in normalized
            for term in ("emprestimo", "financiamento", "parcelamento", "parcela")
        )
        is_investment = any(
            term in normalized
            for term in ("simule", "investir", "investimento", "rendimento", "montante")
        )

        try:
            if is_goal and len(numbers) >= 3:
                target, rate, months = numbers[:3]
                initial = numbers[3] if len(numbers) >= 4 else 0
                result = monthly_savings_for_goal(
                    target=target,
                    monthly_rate_percent=rate,
                    months=int(months),
                    initial_amount=initial,
                )
                return format_simulation(result), "simulation_goal"

            if is_loan and len(numbers) >= 3:
                principal, rate, months = numbers[:3]
                result = loan_payment(
                    principal=principal,
                    monthly_rate_percent=rate,
                    months=int(months),
                )
                return format_simulation(result), "simulation_loan"

            if is_investment and len(numbers) >= 3:
                principal, rate, months = numbers[:3]
                result = compound_interest(
                    principal=principal,
                    monthly_rate_percent=rate,
                    months=int(months),
                )
                return format_simulation(result), "simulation_investment"
        except ValueError as error:
            return (
                f"Não consegui concluir a simulação: {error}. "
                "Revise os valores e tente novamente.",
                "simulation_error",
            )

        if is_goal or is_loan or is_investment:
            return (
                "Para fazer a simulação, informe valor, taxa mensal e prazo em meses. "
                "Exemplo: `Simule R$ 1.000 a 1% ao mês por 12 meses.`",
                "simulation_missing_data",
            )

        return None

    def _local_answer(self, message: str) -> tuple[str, str, list[str]]:
        simulation = self._simulation_answer(message)
        if simulation:
            text, intent = simulation
            return text, intent, ["simuladores locais"]

        match = self.knowledge_base.search(message)
        if match:
            answer = (
                f"**{match.title}**\n\n{match.answer}\n\n"
                f"_{financial_disclaimer()}_"
            )
            return answer, "faq", [f"FAQ local: {match.source_id}"]

        normalized = normalize_text(message)
        if any(term in normalized for term in ("oi", "ola", "bom dia", "boa tarde")):
            return (
                "Olá! Sou o **FinIA**, um assistente financeiro educacional. "
                "Posso explicar PIX, cartão, empréstimos, investimentos e segurança, "
                "além de fazer simulações simples. Como posso ajudar?",
                "greeting",
                [],
            )

        return (
            "Posso ajudar com dúvidas gerais sobre produtos financeiros, segurança "
            "digital e simulações educacionais. Tente perguntar, por exemplo: "
            "`Como comparar um empréstimo?` ou "
            "`Simule R$ 1.000 a 1% ao mês por 12 meses.`\n\n"
            f"_{financial_disclaimer()}_",
            "fallback",
            [],
        )

    def answer(
        self,
        message: str,
        history: Sequence[dict[str, str]] | None = None,
    ) -> AssistantReply:
        """Produz uma resposta segura e, opcionalmente, refinada por IA."""

        if not message.strip():
            return AssistantReply(
                text="Digite uma pergunta para continuar.",
                intent="empty",
            )

        sensitive = find_sensitive_data(message)
        if sensitive:
            return AssistantReply(
                text=privacy_warning(sensitive),
                intent="sensitive_data",
            )

        local_text, intent, sources = self._local_answer(message)

        if contains_guarantee_request(message):
            local_text = (
                "Não é seguro tratar qualquer investimento ou produto financeiro "
                "como livre de risco ou com retorno garantido.\n\n" + local_text
            )
            intent = "risk_warning"

        generated = self.generative.generate(
            user_message=message,
            grounded_answer=local_text,
            history=history,
        )
        if generated:
            return AssistantReply(
                text=generated,
                intent=intent,
                sources=sources,
                used_generative_ai=True,
            )

        return AssistantReply(
            text=local_text,
            intent=intent,
            sources=sources,
            used_generative_ai=False,
        )
