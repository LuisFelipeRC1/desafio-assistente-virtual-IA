"""Cliente de terminal para demonstração do FinIA."""

from __future__ import annotations

from src.assistant import FinancialAssistant


def main() -> None:
    assistant = FinancialAssistant()
    history: list[dict[str, str]] = []

    print("FinIA — Assistente financeiro educacional")
    print("Digite 'sair' para encerrar.\n")

    while True:
        try:
            message = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté logo!")
            break

        if message.lower() in {"sair", "exit", "quit"}:
            print("Até logo!")
            break

        reply = assistant.answer(message, history=history)
        print(f"\nFinIA: {reply.text}\n")

        history.extend(
            [
                {"role": "user", "content": message},
                {"role": "assistant", "content": reply.text},
            ]
        )


if __name__ == "__main__":
    main()
