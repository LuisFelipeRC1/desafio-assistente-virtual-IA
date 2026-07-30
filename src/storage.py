"""Persistência local de conversas usando SQLite."""

from __future__ import annotations

import sqlite3
from pathlib import Path


class SQLiteConversationStore:
    """Armazena mensagens por sessão em um banco SQLite local."""

    def __init__(self, database_path: str | Path = "data/conversations.db") -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_messages_session
                ON messages(session_id, id)
                """
            )

    def add_message(self, session_id: str, role: str, content: str) -> None:
        """Insere uma mensagem na conversa."""

        if role not in {"user", "assistant"}:
            raise ValueError("role deve ser 'user' ou 'assistant'")
        if not session_id.strip() or not content.strip():
            raise ValueError("session_id e content são obrigatórios")

        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO messages(session_id, role, content)
                VALUES (?, ?, ?)
                """,
                (session_id, role, content),
            )

    def get_messages(self, session_id: str, limit: int = 100) -> list[dict[str, str]]:
        """Lista as mensagens mais recentes em ordem cronológica."""

        if limit <= 0:
            raise ValueError("limit deve ser maior que zero")

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT role, content, created_at
                FROM (
                    SELECT id, role, content, created_at
                    FROM messages
                    WHERE session_id = ?
                    ORDER BY id DESC
                    LIMIT ?
                )
                ORDER BY id ASC
                """,
                (session_id, limit),
            ).fetchall()

        return [dict(row) for row in rows]

    def clear(self, session_id: str) -> None:
        """Apaga o histórico da sessão informada."""

        with self._connect() as connection:
            connection.execute(
                "DELETE FROM messages WHERE session_id = ?",
                (session_id,),
            )
