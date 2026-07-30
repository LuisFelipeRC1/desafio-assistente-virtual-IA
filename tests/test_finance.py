import pytest

from src.finance import compound_interest, loan_payment, monthly_savings_for_goal


def test_compound_interest() -> None:
    result = compound_interest(1000, 1, 12)

    assert result.details["montante_estimado"] == pytest.approx(1126.83, abs=0.01)
    assert result.details["rendimento_estimado"] == pytest.approx(126.83, abs=0.01)


def test_zero_interest_loan() -> None:
    result = loan_payment(1200, 0, 12)

    assert result.details["parcela_estimada"] == 100
    assert result.details["juros_estimados"] == 0


def test_price_loan_payment() -> None:
    result = loan_payment(10000, 2, 24)

    assert result.details["parcela_estimada"] == pytest.approx(528.71, abs=0.02)
    assert result.details["total_estimado"] > 10000


def test_goal_without_interest() -> None:
    result = monthly_savings_for_goal(12000, 0, 12)

    assert result.details["aporte_mensal_estimado"] == 1000


def test_invalid_term() -> None:
    with pytest.raises(ValueError):
        compound_interest(1000, 1, 0)
