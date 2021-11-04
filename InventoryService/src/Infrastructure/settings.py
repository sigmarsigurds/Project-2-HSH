from enum import Enum
from pydantic import (BaseSettings)


class ContainerSettingEnum(Enum):
    def get(self, *argv):
        return self.value


class Environment(ContainerSettingEnum):
    DEV = 'dev'
    STAGING = 'staging'
    PROD = 'prod'


class Settings(BaseSettings):
    host: str
    port: int

    postgres_host: str
    postgres_database: str
    postgres_user: str
    postgres_password: str

    merchant_service_host: str
    merchant_service_port: str

    rabbitmq_server_host: str

    environment: Environment

    class Config:
        # env_prefix = 'INVENTORY_SERVICE_'  # defaults to no prefix, i.e. ""
        fields = {
            'host': {
                'env': 'HOST'
            },
            'port': {
                'env': 'PORT'
            },
            'postgres_host': {
                'env': 'POSTGRES_HOST',
            },
            'postgres_database': {
                'env': 'POSTGRES_DATABASE',
            },
            'postgres_user': {
                'env': 'POSTGRES_USER',
            },
            'postgres_password': {
                'env': 'POSTGRES_PASSWORD',
            },
            'environment': {
                'env': 'ENVIRONMENT'
            },
            "merchant_service_host": {
                'env': 'MERCHANT_SERVICE_HOST'
            },
            'merchant_service_port': {
                'env': 'MERCHANT_SERVICE_PORT'
            },
            'rabbitmq_server_host': {
                'env': 'RABBITMQ_SERVER_HOST'
            }
        }

