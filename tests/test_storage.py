from src.storage import SQLiteConversationStore


def test_store_persists_and_clears_messages(tmp_path) -> None:
    store = SQLiteConversationStore(tmp_path / "test.db")

    store.add_message("session-1", "user", "Olá")
    store.add_message("session-1", "assistant", "Como posso ajudar?")

    messages = store.get_messages("session-1")
    assert [message["role"] for message in messages] == ["user", "assistant"]
    assert messages[0]["content"] == "Olá"

    store.clear("session-1")
    assert store.get_messages("session-1") == []
