from pydantic import BaseModel, Field
from typing import Optional


class CreditCardModel(BaseModel):
    card_number: str = Field(..., alias="cardNumber")
    expiration_month: int = Field(..., alias="expirationMonth")
    expiration_year: int = Field(..., alias="expirationYear")
    cvc: str
