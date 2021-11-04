from pydantic import BaseModel
from pydantic.fields import Field


class EmailEventModel(BaseModel):
    email_to: str = Field(..., alias="emailTo")
    subject: str
    content: str
