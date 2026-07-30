"""Recuperação simples de respostas em uma base local de FAQs."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from .safety import normalize_text

DEFAULT_FAQ_PATH = Path(__file__).resolve().parents[1] / "data" / "faqs.json"


@dataclass(frozen=True)
class KnowledgeMatch:
    """Uma resposta recuperada e seu grau de correspondência."""

    title: str
    answer: str
    score: float
    source_id: str


class KnowledgeBase:
    """Base local com busca por palavras e sobreposição de termos."""

    def __init__(self, path: str | Path = DEFAULT_FAQ_PATH) -> None:
        faq_path = Path(path)
        with faq_path.open("r", encoding="utf-8") as file:
            self.entries: list[dict[str, object]] = json.load(file)

    @staticmethod
    def _tokens(text: str) -> set[str]:
        normalized = normalize_text(text)
        return {
            token
            for token in re.findall(r"[a-z0-9]+", normalized)
            if len(token) > 2
        }

    def search(self, query: str, minimum_score: float = 0.18) -> KnowledgeMatch | None:
        """Busca a FAQ mais relevante para a pergunta."""

        query_tokens = self._tokens(query)
        if not query_tokens:
            return None

        best: KnowledgeMatch | None = None
        normalized_query = normalize_text(query)

        for entry in self.entries:
            title = str(entry["title"])
            answer = str(entry["answer"])
            keywords = [str(item) for item in entry.get("keywords", [])]

            document_tokens = self._tokens(" ".join([title, answer, *keywords]))
            overlap = len(query_tokens & document_tokens) / len(query_tokens)

            keyword_bonus = sum(
                0.18 for keyword in keywords if normalize_text(keyword) in normalized_query
            )
            score = min(overlap + keyword_bonus, 1.0)

            candidate = KnowledgeMatch(
                title=title,
                answer=answer,
                score=score,
                source_id=str(entry["id"]),
            )
            if best is None or candidate.score > best.score:
                best = candidate

        if best is None or best.score < minimum_score:
            return None
        return best
