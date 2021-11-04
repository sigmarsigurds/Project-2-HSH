from typing import Optional
from pydantic import BaseModel
from pydantic.fields import Field


class BuyerModel(BaseModel):
    buyer_id: int = Field(None, alias="buyerId")
    name: str
    ssn: str
    email: str
    phone_number: str = Field(..., alias="phoneNumber")
