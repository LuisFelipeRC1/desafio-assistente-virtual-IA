"""Simuladores financeiros demonstrativos."""

from __future__ import annotations

import math

from .models import SimulationResult


def _validate_positive(value: float, field: str, *, allow_zero: bool = False) -> None:
    minimum_ok = value >= 0 if allow_zero else value > 0
    if not minimum_ok or not math.isfinite(value):
        comparator = "maior ou igual a zero" if allow_zero else "maior que zero"
        raise ValueError(f"{field} deve ser {comparator}")


def compound_interest(
    principal: float,
    monthly_rate_percent: float,
    months: int,
) -> SimulationResult:
    """Calcula juros compostos com capitalização mensal."""

    _validate_positive(principal, "O valor inicial")
    _validate_positive(monthly_rate_percent, "A taxa", allow_zero=True)
    if months <= 0:
        raise ValueError("O prazo deve ser maior que zero")

    rate = monthly_rate_percent / 100
    future_value = principal * (1 + rate) ** months
    earnings = future_value - principal

    return SimulationResult(
        title="Simulação de juros compostos",
        summary=(
            f"Aplicando R$ {principal:,.2f} por {months} meses a "
            f"{monthly_rate_percent:.2f}% ao mês, o montante estimado é "
            f"R$ {future_value:,.2f}."
        ),
        details={
            "valor_inicial": round(principal, 2),
            "taxa_mensal_percentual": round(monthly_rate_percent, 4),
            "prazo_meses": months,
            "montante_estimado": round(future_value, 2),
            "rendimento_estimado": round(earnings, 2),
        },
        formula="M = C × (1 + i)ⁿ",
    )


def loan_payment(
    principal: float,
    monthly_rate_percent: float,
    months: int,
) -> SimulationResult:
    """Calcula a parcela fixa aproximada pelo Sistema Price."""

    _validate_positive(principal, "O valor financiado")
    _validate_positive(monthly_rate_percent, "A taxa", allow_zero=True)
    if months <= 0:
        raise ValueError("O número de parcelas deve ser maior que zero")

    rate = monthly_rate_percent / 100
    if rate == 0:
        payment = principal / months
    else:
        payment = principal * rate * (1 + rate) ** months / ((1 + rate) ** months - 1)

    total = payment * months
    interest = total - principal

    return SimulationResult(
        title="Simulação de empréstimo",
        summary=(
            f"Para R$ {principal:,.2f} em {months} parcelas, com taxa de "
            f"{monthly_rate_percent:.2f}% ao mês, a parcela estimada é "
            f"R$ {payment:,.2f}."
        ),
        details={
            "valor_financiado": round(principal, 2),
            "taxa_mensal_percentual": round(monthly_rate_percent, 4),
            "numero_de_parcelas": months,
            "parcela_estimada": round(payment, 2),
            "total_estimado": round(total, 2),
            "juros_estimados": round(interest, 2),
        },
        formula="PMT = PV × i × (1 + i)ⁿ ÷ ((1 + i)ⁿ − 1)",
    )


def monthly_savings_for_goal(
    target: float,
    monthly_rate_percent: float,
    months: int,
    initial_amount: float = 0,
) -> SimulationResult:
    """Calcula o aporte mensal estimado para alcançar uma meta."""

    _validate_positive(target, "A meta")
    _validate_positive(monthly_rate_percent, "A taxa", allow_zero=True)
    _validate_positive(initial_amount, "O valor inicial", allow_zero=True)
    if months <= 0:
        raise ValueError("O prazo deve ser maior que zero")
    if initial_amount >= target:
        monthly_contribution = 0.0
    else:
        rate = monthly_rate_percent / 100
        initial_future_value = initial_amount * (1 + rate) ** months

        if rate == 0:
            monthly_contribution = max(target - initial_amount, 0) / months
        else:
            annuity_factor = ((1 + rate) ** months - 1) / rate
            monthly_contribution = max(target - initial_future_value, 0) / annuity_factor

    total_contributed = initial_amount + monthly_contribution * months

    return SimulationResult(
        title="Planejamento de meta financeira",
        summary=(
            f"Para alcançar R$ {target:,.2f} em {months} meses, considerando "
            f"{monthly_rate_percent:.2f}% ao mês e valor inicial de "
            f"R$ {initial_amount:,.2f}, o aporte mensal estimado é "
            f"R$ {monthly_contribution:,.2f}."
        ),
        details={
            "meta": round(target, 2),
            "valor_inicial": round(initial_amount, 2),
            "taxa_mensal_percentual": round(monthly_rate_percent, 4),
            "prazo_meses": months,
            "aporte_mensal_estimado": round(monthly_contribution, 2),
            "total_aportado_estimado": round(total_contributed, 2),
        },
        formula="PMT = (FV − PV × (1 + i)ⁿ) ÷ (((1 + i)ⁿ − 1) ÷ i)",
    )


def format_simulation(result: SimulationResult) -> str:
    """Transforma um resultado estruturado em resposta legível."""

    lines = [f"**{result.title}**", "", result.summary, "", "**Detalhes:**"]
    labels = {
        "valor_inicial": "Valor inicial",
        "taxa_mensal_percentual": "Taxa mensal",
        "prazo_meses": "Prazo",
        "montante_estimado": "Montante estimado",
        "rendimento_estimado": "Rendimento estimado",
        "valor_financiado": "Valor financiado",
        "numero_de_parcelas": "Número de parcelas",
        "parcela_estimada": "Parcela estimada",
        "total_estimado": "Total estimado",
        "juros_estimados": "Juros estimados",
        "meta": "Meta",
        "aporte_mensal_estimado": "Aporte mensal estimado",
        "total_aportado_estimado": "Total aportado estimado",
    }

    currency_fields = {
        "valor_inicial",
        "montante_estimado",
        "rendimento_estimado",
        "valor_financiado",
        "parcela_estimada",
        "total_estimado",
        "juros_estimados",
        "meta",
        "aporte_mensal_estimado",
        "total_aportado_estimado",
    }

    for key, value in result.details.items():
        label = labels.get(key, key.replace("_", " ").title())
        if key in currency_fields:
            rendered = f"R$ {value:,.2f}"
        elif "percentual" in key:
            rendered = f"{value:.2f}% ao mês"
        elif "meses" in key or "parcelas" in key:
            rendered = str(value)
        else:
            rendered = str(value)
        lines.append(f"- {label}: {rendered}")

    lines.extend(
        [
            "",
            f"**Fórmula:** `{result.formula}`",
            "",
            f"_{result.disclaimer}_",
        ]
    )
    return "\n".join(lines)
