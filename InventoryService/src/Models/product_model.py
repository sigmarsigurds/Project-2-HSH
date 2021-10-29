from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal


class ProductModel(BaseModel):
    id: Optional[int] = None  # * Before Product is create id is not provided, so id needs to be allowed to be none
    merchant_id: int = Field(..., alias='merchantId')  # alias allows use to receive JSON from client with camel case
    name: str = Field(..., alias='productName')
    price: Decimal
    quantity: int
    reserved: int
