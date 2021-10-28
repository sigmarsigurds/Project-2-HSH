from typing import Optional
from pydantic import BaseModel, Field


class MerchantModel(BaseModel):
    id: Optional[int] = None  # * Before Merchant is create id is not provided, so id needs to be allowed to be none
    name: str
    ssn: str
    email: str
    phone_number: str = Field(..., alias='phoneNumber')
    allows_discount: bool = Field(..., alias='allowsDiscount')


