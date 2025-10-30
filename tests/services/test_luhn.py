import pytest
from fastapi import HTTPException
from app.services.luhn import LuhnService, get_luhn_service
from app.models.generated_models import (
    CardRequest,
    CardValidation,
    ErrorResponse,
    Scheme,
    Message,
)


@pytest.fixture
def luhn_service():
    return LuhnService()


def test_luhn_valid_card(luhn_service):
    # Pick a card where doubling > 9 occurs to cover n -= 9
    card_req = CardRequest(number="4111111111111111")  # valid Visa
    result = luhn_service.validate(card_req)
    assert isinstance(result, CardValidation)
    assert result.valid is True
    assert result.scheme == Scheme.visa
    assert result.message == Message.OK


def test_luhn_invalid_card(luhn_service):
    card_req = CardRequest(number="4111111111111112")  # fails Luhn
    result = luhn_service.validate(card_req)
    assert isinstance(result, CardValidation)
    assert result.valid is False
    assert result.scheme == Scheme.visa
    assert result.message == Message.OK


@pytest.mark.parametrize("number", ["123456789", "4" * 20])
def test_card_invalid_length(luhn_service, number):
    card_req = CardRequest(number=number)
    with pytest.raises(HTTPException) as exc_info:
        luhn_service.validate(card_req)
    assert exc_info.value.status_code == 400
    detail = exc_info.value.detail
    assert detail["code"] == "400"
    assert "12-19 digits" in detail["error_message"]


def test_invalid_card_number_non_digit(luhn_service):
    card_req = CardRequest(number="abcd1234efgh")
    with pytest.raises(HTTPException) as exc_info:
        luhn_service.validate(card_req)
    assert exc_info.value.status_code == 400
    detail = exc_info.value.detail
    assert detail["code"] == "400"


def test_internal_server_error(monkeypatch, luhn_service):
    def raise_exception(_):
        raise ValueError("Unexpected error")

    monkeypatch.setattr(luhn_service, "clean_credit_number", raise_exception)

    card_req = CardRequest(number="4111111111111111")
    with pytest.raises(HTTPException) as exc_info:
        luhn_service.validate(card_req)
    assert exc_info.value.status_code == 500
    detail = exc_info.value.detail
    assert detail["code"] == "500"
    assert "Internal server error" in detail["error_message"]


@pytest.mark.parametrize("number", ["34xxxxxxxxxxxxxxx", "37xxxxxxxxxxxxxxx"])
def test_get_card_scheme_amex(luhn_service, number):
    scheme = luhn_service.get_card_scheme(number)
    assert scheme == "amex"


@pytest.mark.parametrize(
    "number",
    [
        "51xxxxxxxxxxxxxxx",
        "52xxxxxxxxxxxxxxx",
        "53xxxxxxxxxxxxxxx",
        "54xxxxxxxxxxxxxxx",
        "55xxxxxxxxxxxxxxx",
    ],
)
def test_get_card_scheme_mastercard(luhn_service, number):
    scheme = luhn_service.get_card_scheme(number)
    assert scheme == "mastercard"  # new coverage for Mastercard branch


@pytest.mark.parametrize("number", ["60xxxxxxxxxxxxxx", "99xxxxxxxxxxxxxx", "1234"])
def test_get_card_scheme_unknown(luhn_service, number):
    scheme = luhn_service.get_card_scheme(number)
    assert scheme == "unknown"  # line 47


def test_get_luhn_service_instance():
    service = get_luhn_service()  # line 59
    assert isinstance(service, LuhnService)
