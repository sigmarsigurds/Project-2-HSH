from pydantic import BaseModel, Field
from typing import Optional
from APIModels.credit_card_model import CreditCardModel


class OrderDatabaseModel(BaseModel):
    order_id: int = Field(..., alias="orderId")
    product_id: int = Field(..., alias="productId")
    merchant_id: int = Field(..., alias="merchantId")
    buyer_id: int = Field(..., alias="buyerId")
    # credit_card: CreditCardModel = Field(..., alias="creditCard")
    card_number: str = Field(..., alias="cardNumber")
    total_price: float = Field(..., alias="totalPrice")
    # discount: Optional[float] = Field(..., alias="discount")
