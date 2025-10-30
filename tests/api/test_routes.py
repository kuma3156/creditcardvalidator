import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from fastapi import HTTPException
from fastapi import FastAPI
from app.api.routes import router
from app.models.generated_models import CardRequest, CardValidation, ErrorResponse
from app.services.luhn import LuhnService, get_luhn_service

# Create a FastAPI app with just the router
app = FastAPI()
app.include_router(router)


@pytest.fixture
def mock_luhn_service():
    mock_service = MagicMock(spec=LuhnService)
    return mock_service


@pytest.fixture
def client(mock_luhn_service):
    app.dependency_overrides[get_luhn_service] = lambda: mock_luhn_service
    return TestClient(app)


def test_validate_card_valid(client, mock_luhn_service):
    mock_luhn_service.validate.return_value = CardValidation(
        valid=True, scheme="visa", message="OK"
    )

    payload = {"number": "4111111111111111"}
    response = client.post("/validate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["valid"] is True
    assert data["scheme"] == "visa"
    assert data["message"] == "OK"

    # Ensure the service validate method was called exactly once
    mock_luhn_service.validate.assert_called_once()
    called_arg = mock_luhn_service.validate.call_args[0][0]
    assert isinstance(called_arg, CardRequest)
    assert called_arg.number == payload["number"]


def test_validate_card_invalid(client, mock_luhn_service):
    mock_luhn_service.validate.side_effect = HTTPException(
        status_code=400,
        detail=ErrorResponse(
            code="400", error_message="Credit card number must be 12-19 digits"
        ).dict(),
    )

    payload = {"number": "123abc"}
    response = client.post("/validate", json=payload)
    assert response.status_code == 400  # Your endpoint returns ErrorResponse directly

    data = response.json()
    assert data["detail"]["code"] == "400"
    assert "must be 12-19 digits" in data["detail"]["error_message"]

    mock_luhn_service.validate.assert_called_once()
    called_arg = mock_luhn_service.validate.call_args[0][0]
    assert isinstance(called_arg, CardRequest)
    assert called_arg.number == payload["number"]
