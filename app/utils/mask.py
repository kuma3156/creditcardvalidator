class Mask:
    ## This method masks all but the last four digits of a credit card number.
    ## This is done to avoid logging PANs in their entirety.
    @staticmethod
    def mask_card_number(card_number: str) -> str:
        if len(card_number) < 4:
            return "*" * len(card_number)
        return "*" * (len(card_number) - 4) + card_number[-4:]
