from typing import Optional
from pydantic import BaseModel, Field

from src.Models.credit_card_model import CreditCardModel


class OrderPaymentInformationModel(BaseModel):
    order_id: int
    buyer_email: str
    merchant_email: str
    product_id: int
    merchant_id: int
    credit_card: CreditCardModel
    quantity: int = 1
