from typing import Optional
from pydantic import BaseModel
from pydantic.fields import Field


class EmailModel(BaseModel):
    email_to: str = Field(..., alias="emailTo")
    subject: str
    content: str
