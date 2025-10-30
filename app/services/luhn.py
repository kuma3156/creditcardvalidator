from functools import lru_cache
from fastapi import HTTPException
from app.models.generated_models import CardRequest, CardValidation, ErrorResponse
from app.utils.mask import Mask
from fastapi.logger import logger


class LuhnService:
    ## This method validates the credit card number using the Luhn algorithm.
    def validate(self, card_req: CardRequest) -> CardValidation:
        try:
            logger.info(f"Received new reuqest for validation")
            cleaned_number = self.clean_credit_number(card_req.number)
            masked_number = Mask.mask_card_number(cleaned_number)
            logger.info(
                f"Request for card number: {masked_number}, excuting Luhn validation"
            )
            if len(cleaned_number) > 19 or len(cleaned_number) < 12:
                raise HTTPException(
                    status_code=400,
                    detail=self.error_response_builder(
                        "400", "Credit card number must be 12-19 digits"
                    ).dict(),
                )
            response: CardValidation = self.card_validation_response_builder(
                cleaned_number, self.luhn_calculator(cleaned_number)
            )
            logger.info(
                f"Card number {masked_number} validation completed successfully, returning response"
            )
            return response
        except HTTPException as http_exc:
            logger.error(f"HTTP Exception occurred: {http_exc.detail}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=self.error_response_builder(
                    "500", "Internal server error."
                ).dict(),
            )

    ## Helper method to clean the credit card number
    def clean_credit_number(self, number: str) -> str:
        return "".join(filter(str.isdigit, number))

    ## Helper method to determine the card scheme based on the number prefix
    def get_card_scheme(self, number: str) -> str:
        if number.startswith("4"):
            return "visa"
        elif number.startswith(("34", "37")):
            return "amex"
        elif number.startswith(("51", "52", "53", "54", "55")):
            return "mastercard"
        else:
            return "unknown"

    ## Helper method to build the CardValidation response
    def card_validation_response_builder(
        self, number: str, is_valid: bool
    ) -> CardValidation:
        scheme = self.get_card_scheme(number)
        return CardValidation(valid=is_valid, scheme=scheme, message="OK")

    ## Helper method to build the ErrorResponse
    def error_response_builder(self, number: int, message: str) -> ErrorResponse:
        return ErrorResponse(code=str(number), error_message=message)

    ## Luhn algorithm implementation to validate the credit card number
    def luhn_calculator(self, cleaned_number: str) -> bool:
        ## Maintain a running total for the Luhn algorithm
        total = 0
        reverse_digits = cleaned_number[::-1]
        is_valid = False

        ## Apply the Luhn algorithm
        for i, digit in enumerate(reverse_digits):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        ## Determine if the card number is valid
        is_valid = (total % 10) == 0
        return is_valid


## Dependency injection with caching to provide a singleton LuhnService instance
@lru_cache()
def get_luhn_service() -> LuhnService:
    return LuhnService()
