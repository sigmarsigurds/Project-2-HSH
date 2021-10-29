from typing import Optional
from pydantic import BaseModel
from pydantic.fields import Field


class BuyerModel(BaseModel):
    buyerId: Optional[int]  # = Field(None, alias="buyerId")
    name: str
    ssn: str
    email: str
    phoneNumber: str  # = Field(..., alias="phoneNumber")
