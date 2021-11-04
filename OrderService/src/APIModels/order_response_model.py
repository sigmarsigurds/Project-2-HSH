from pydantic import BaseModel, Field


class OrderResponseModel(BaseModel):
    product_id: int = Field(..., alias="productId")
    merchant_id: int = Field(..., alias="merchantId")
    buyer_id: int = Field(..., alias="buyerId")
    card_number: str = Field(..., alias="cardNumber")
    total_price: float = Field(..., alias="totalPrice")
