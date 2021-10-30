from typing import Optional
from pydantic import BaseModel, Field
from APIModels.credit_card_model import CreditCardModel


class OrderReservationModel(BaseModel):
    order_id: int = Field(..., alias="orderId")
    buyer_email: str = Field(..., alias="buyerEmail")
    merchant_email: str = Field(..., alias="merchantEmail")
    product_name: str = Field(..., alias="productName")
    order_price: str = Field(..., alias="orderPrice")
