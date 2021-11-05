from typing import Optional
from pydantic import BaseModel, Field

from src.ApiModels.credit_card_model import CreditCardModel


class OrderRequestModel(BaseModel):
    productId: int
    merchantId: int
    buyerId: int
    creditCard: CreditCardModel
    discount: Optional[float]
