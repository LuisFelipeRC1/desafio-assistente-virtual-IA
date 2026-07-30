"""Integração opcional com IA generativa."""

from __future__ import annotations

import os
from typing import Sequence


SYSTEM_INSTRUCTIONS = """
Você é o FinIA, um assistente financeiro educacional em português do Brasil.

Regras:
1. Use linguagem simples, respeitosa e objetiva.
2. Não diga que acessou conta, saldo, fatura ou transações reais.
3. Não solicite CPF, senha, token, CVV ou número completo de cartão.
4. Não prometa lucro, aprovação de crédito ou ausência de risco.
5. Diferencie informação geral de recomendação individual.
6. Preserve os números e as premissas de simulações fornecidas pelo sistema.
7. Quando não houver informação suficiente, explique a limitação.
8. Finalize orientações financeiras relevantes com um aviso breve para conferir
   taxas, riscos e condições nos canais oficiais.
""".strip()


class OpenAIGenerativeResponder:
    """Gera uma resposta final usando a API, quando configurada."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5")

    @property
    def enabled(self) -> bool:
        return bool(os.getenv("OPENAI_API_KEY"))

    def generate(
        self,
        user_message: str,
        grounded_answer: str,
        history: Sequence[dict[str, str]] | None = None,
    ) -> str | None:
        """Refina uma resposta fundamentada sem tornar a API obrigatória."""

        if not self.enabled:
            return None

        try:
            from openai import OpenAI

            client = OpenAI()
            recent_history = list(history or [])[-6:]
            context = "\n".join(
                f"{item.get('role', 'user')}: {item.get('content', '')}"
                for item in recent_history
            )

            prompt = f"""
Contexto recente da conversa:
{context or "Sem contexto anterior."}

Pergunta atual:
{user_message}

Resposta fundamentada produzida pelos módulos locais:
{grounded_answer}

Reescreva a resposta fundamentada de forma natural e útil. Não altere valores,
fórmulas ou avisos de segurança. Não invente produtos, taxas ou dados da conta.
""".strip()

            response = client.responses.create(
                model=self.model,
                instructions=SYSTEM_INSTRUCTIONS,
                input=prompt,
            )
            output = response.output_text.strip()
            return output or None
        except Exception:
            # A aplicação deve continuar funcionando em modo local quando a API
            # estiver indisponível, sem expor detalhes técnicos ou credenciais.
            return None
