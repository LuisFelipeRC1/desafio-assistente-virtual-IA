"""Regras simples de segurança, privacidade e uso responsável."""

from __future__ import annotations

import re
import unicodedata

SENSITIVE_PATTERNS = {
    "CPF": re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"),
    "número de cartão": re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
    "código de segurança": re.compile(
        r"\b(?:cvv|cvc|codigo de seguranca|código de segurança)\s*[:=-]?\s*\d{3,4}\b",
        re.IGNORECASE,
    ),
    "senha": re.compile(
        r"\b(?:senha|password)\s*[:=-]\s*\S+",
        re.IGNORECASE,
    ),
}

GUARANTEE_TERMS = (
    "lucro garantido",
    "retorno garantido",
    "sem risco",
    "dinheiro garantido",
)


def normalize_text(text: str) -> str:
    """Remove acentos e uniformiza o texto para comparações."""

    normalized = unicodedata.normalize("NFKD", text)
    return "".join(char for char in normalized if not unicodedata.combining(char)).lower()


def find_sensitive_data(text: str) -> list[str]:
    """Retorna categorias de dados sensíveis identificadas na mensagem."""

    found: list[str] = []
    for label, pattern in SENSITIVE_PATTERNS.items():
        if pattern.search(text):
            found.append(label)
    return found


def contains_guarantee_request(text: str) -> bool:
    """Identifica linguagem de promessa de retorno ou ausência de risco."""

    normalized = normalize_text(text)
    return any(term in normalized for term in GUARANTEE_TERMS)


def privacy_warning(categories: list[str]) -> str:
    """Cria uma orientação de privacidade sem repetir os dados detectados."""

    joined = ", ".join(categories)
    return (
        f"⚠️ Identifiquei possível dado sensível na mensagem ({joined}). "
        "Por segurança, não compartilhe CPF, número completo do cartão, senha, "
        "token ou código de segurança em chats. Remova essas informações e envie "
        "novamente apenas a dúvida geral. Em caso de suspeita de fraude, utilize "
        "somente os canais oficiais da sua instituição."
    )


def financial_disclaimer() -> str:
    """Aviso padrão para respostas de caráter financeiro."""

    return (
        "Conteúdo educacional e demonstrativo. Antes de contratar um produto ou "
        "tomar uma decisão financeira, confira taxas, riscos, impostos e condições "
        "nos canais oficiais da instituição."
    )
