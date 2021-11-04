from typing import Optional
from pydantic import BaseModel, Field


class MerchantModel(BaseModel):
    merchant_id: int = Field(..., alias="merchantId")
    name: str
    ssn: str
    email: str
    phone_number: str = Field(..., alias="phoneNumber")
    allows_discount: bool = Field(..., alias="allowsDiscount")
