from pydantic import BaseModel, Field


class OrderEmailInformationModel(BaseModel):
    order_id: int = Field(..., alias="orderId")
    buyer_email: str = Field(..., alias="buyerEmail")
    merchant_email: str = Field(..., alias="merchantEmail")
    product_name: str = Field(..., alias="productName")
    order_price: str = Field(..., alias="orderPrice")
