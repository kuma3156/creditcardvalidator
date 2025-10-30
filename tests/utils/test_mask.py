# tests/utils/test_mask.py
import pytest
from app.utils.mask import Mask


def test_mask_card_number_normal():
    card_number = "1234567812345678"
    masked = Mask.mask_card_number(card_number)
    assert masked == "************5678"


def test_mask_card_number_short():
    card_number = "123"
    masked = Mask.mask_card_number(card_number)
    assert masked == "***"


def test_mask_card_number_exact_4():
    card_number = "1234"
    masked = Mask.mask_card_number(card_number)
    assert masked == "1234"


def test_mask_card_number_empty():
    card_number = ""
    masked = Mask.mask_card_number(card_number)
    assert masked == ""
