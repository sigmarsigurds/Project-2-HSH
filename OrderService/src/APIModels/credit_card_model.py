from pydantic import BaseModel, Field
from typing import Optional


class CreditCardModel(BaseModel):
    # credit_card_id: Optional[int] = Field(None, alias="creditCardId")
    card_number: str = Field(..., alias="cardNumber")
    expiration_month: int = Field(..., alias="expirationMonth")
    expiration_year: int = Field(..., alias="expirationYear")
    cvc: str
