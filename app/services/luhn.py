from functools import lru_cache
from fastapi import HTTPException
from app.models.generated_models import CardRequest, CardValidation, ErrorResponse

class LuhnService:

    def validate(self, card_req: CardRequest) -> CardValidation:
        try:
            cleaned_number = self.clean_credit_number(card_req.number)

            if len(cleaned_number) > 19 or len(cleaned_number) < 12:
                raise HTTPException(status_code=400, detail=self.error_response_builder("400", "Credit card number must be 12-19 digits").dict())

            total = 0
            reverse_digits = cleaned_number[::-1]
            is_valid=False


            for i, digit in enumerate(reverse_digits):
                n = int(digit)
                if i % 2 == 1:
                    n *= 2
                    if n > 9:
                        n -= 9
                total += n

            is_valid=total % 10 == 0

            return self.card_validation_response_builder(cleaned_number, is_valid)
        except HTTPException as http_exc:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=self.error_response_builder("500", "Internal server error.").dict())
            
        
    def clean_credit_number(self,number: str) -> str:
        return ''.join(filter(str.isdigit, number))

    def get_card_scheme(self, number: str) -> str:
        if number.startswith('4'):
            return 'visa'
        elif number.startswith(('34', '37')):
            return 'amex'
        elif number.startswith(('51', '52', '53', '54', '55')):
            return 'mastercard'
        else:
            return 'unknown'

    def card_validation_response_builder(self, number: str, is_valid:bool) -> CardValidation:
        scheme = self.get_card_scheme(number)
        return CardValidation(valid=is_valid, scheme=scheme, message="OK")
    
    def error_response_builder(self, number: int, message:str) -> ErrorResponse:
        return ErrorResponse(code=str(number),error_message=message)


@lru_cache()
def get_luhn_service() -> LuhnService:
    return LuhnService()