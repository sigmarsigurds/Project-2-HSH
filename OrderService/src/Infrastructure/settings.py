from enum import Enum

from pydantic import BaseSettings


class ContainerSettingEnum(Enum):
    def get(self, *argv):
        return self.value


class Environment(ContainerSettingEnum):
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"


class Settings(BaseSettings):
    postgres_host: str
    postgres_database: str
    postgres_user: str
    postgres_password: str

    environment: Environment

    # queue_name: str
    rabbitmq_server_host: str

    merchant_service_host: str
    merchant_service_endpoint: str
    merchant_service_port: str

    buyer_service_host: str
    buyer_service_endpoint: str
    buyer_service_port: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
