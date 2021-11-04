from pydantic import BaseModel, Field
from typing import Optional


class CreditCardModel(BaseModel):
    card_number: str
    expiration_month: int
    expiration_year: int
    cvc: str
