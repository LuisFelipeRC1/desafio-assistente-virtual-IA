"""Modelos de dados usados pelo assistente."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SimulationResult:
    """Resultado estruturado de uma simulação financeira."""

    title: str
    summary: str
    details: dict[str, Any]
    formula: str
    disclaimer: str = (
        "Simulação educacional. Valores reais podem variar por impostos, tarifas, "
        "inflação, perfil de risco e condições da instituição."
    )


@dataclass(frozen=True)
class AssistantReply:
    """Resposta produzida pelo assistente."""

    text: str
    intent: str
    sources: list[str] = field(default_factory=list)
    used_generative_ai: bool = False
