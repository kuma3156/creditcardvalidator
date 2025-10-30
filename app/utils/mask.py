class Mask:
    @staticmethod
    def mask_card_number(card_number: str) -> str:
        if len(card_number) < 4:
            return "*" * len(card_number)
        return "*" * (len(card_number) - 4) + card_number[-4:]
