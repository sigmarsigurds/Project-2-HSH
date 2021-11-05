from pydantic import BaseModel, Field
from typing import Optional


class CreditCardModel(BaseModel):
    cardNumber: str
    expirationMonth: int
    expirationYear: int
    cvc: str
