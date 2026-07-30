from src.assistant import FinancialAssistant, parse_pt_number


class DisabledGenerativeResponder:
    def generate(self, *args, **kwargs):
        return None


def build_assistant() -> FinancialAssistant:
    return FinancialAssistant(generative_responder=DisabledGenerativeResponder())


def test_parse_brazilian_number() -> None:
    assert parse_pt_number("1.250,50") == 1250.50
    assert parse_pt_number("1000") == 1000


def test_detects_investment_simulation() -> None:
    reply = build_assistant().answer(
        "Simule R$ 1.000 a 1% ao mês por 12 meses"
    )

    assert reply.intent == "simulation_investment"
    assert "1,126.83" in reply.text


def test_detects_loan_simulation() -> None:
    reply = build_assistant().answer(
        "Calcule um empréstimo de 10000 a 2% ao mês em 24 meses"
    )

    assert reply.intent == "simulation_loan"
    assert "parcela estimada" in reply.text.lower()


def test_retrieves_security_faq() -> None:
    reply = build_assistant().answer("Como evitar golpe no PIX?")

    assert reply.intent == "faq"
    assert "destinatário" in reply.text


def test_blocks_sensitive_data() -> None:
    reply = build_assistant().answer("Meu CPF é 123.456.789-00, pode verificar?")

    assert reply.intent == "sensitive_data"
    assert "não compartilhe" in reply.text.lower()


def test_warns_about_guaranteed_return() -> None:
    reply = build_assistant().answer("Qual investimento tem lucro garantido?")

    assert reply.intent == "risk_warning"
    assert "retorno garantido" in reply.text.lower()
