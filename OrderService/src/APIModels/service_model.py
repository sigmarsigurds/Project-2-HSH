from pydantic import BaseModel


class ServiceModel(BaseModel):
    host: str
    port: str
    endpoint: str
