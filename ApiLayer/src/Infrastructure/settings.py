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
    order_service_host: str
    order_service_port: int

    merchant_service_host: str
    merchant_service_port: int

    buyer_service_host: str
    buyer_service_port: int

    inventory_service_host: str
    inventory_service_port: int

    host: str
    port: int

    environment: Environment

    class Config:
        # env_prefix = 'MERCHANT_SERVICE_'  # defaults to no prefix, i.e. ""
        fields = {
            'host': {
                'env': 'HOST'
            },
            'port': {
                'PORT': 'PORT'
            },
            'order_service_host': {
                'env': 'ORDER_SERVICE_HOST',
            },
            'order_service_port': {
                'env': 'ORDER_SERVICE_PORT',
            },
            'merchant_service_host': {
                'env': 'MERCHANT_SERVICE_HOST',
            },
            'merchant_service_port': {
                'env': 'MERCHANT_SERVICE_PORT',
            },
            'buyer_service_host': {
                'env': 'BUYER_SERVICE_HOST',
            },
            'buyer_service_port': {
                'env': 'BUYER_SERVICE_PORT',
            },
            'inventory_service_host': {
                'env': 'INVENTORY_SERVICE_HOST',
            },
            'inventory_service_port': {
                'env': 'INVENTORY_SERVICE_PORT',
            },
            'environment': {
                'env': 'ENVIRONMENT'
            }
        }
