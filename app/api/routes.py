from fastapi import APIRouter, Depends
from app.models.generated_models import CardRequest, CardValidation, ErrorResponse
from app.services.luhn import get_luhn_service, LuhnService

router = APIRouter()

@router.post("/validate", tags=["Validation"])
def validate_card(req: CardRequest, luhn_service: LuhnService = Depends(get_luhn_service)):
    return luhn_service.validate(req)