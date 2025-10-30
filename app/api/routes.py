from fastapi import APIRouter, Depends
from app.models.generated_models import CardRequest, CardValidation, ErrorResponse
from app.services.luhn import get_luhn_service, LuhnService

## This our routes folder creating the API router and defining the endpoint for card validation.
router = APIRouter()


## Here we define a POST endpoint /validate that accepts a CardRequest and returns a CardValidation response.
## We use dependency injection to get an instance of LuhnService to handle the validation logic.
@router.post("/validate", tags=["Validation"])
def validate_card(
    req: CardRequest, luhn_service: LuhnService = Depends(get_luhn_service)
):
    return luhn_service.validate(req)
