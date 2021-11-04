from pydantic import BaseModel, Field
from decimal import Decimal


class ProductModel(BaseModel):
    product_id: int = Field(..., alias="productId")
    merchant_id: int = Field(..., alias="merchantId")
    product_name: str = Field(..., alias="productName")
    price: Decimal
    quantity: int
    reserved: int
