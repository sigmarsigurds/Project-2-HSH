from dependency_injector import containers, providers
from APIModels.service_model import ServiceModel
from Validations.ProductExistsValidation import ProductExistsValidation
from Validations.MerchantAllowsDiscountValidation import (
    MerchantAllowsDiscountValidation,
)
from Validations.BuyerExistsValidation import BuyerExistsValidation
from Validations.MerchantExistsValidation import MerchantExistsValidation
from Validations.OrderValidator import OrderValidator

from Repositories.order_repository import OrderRepository
from Infrastructure.settings import Settings
from DBConnections.db_config import DbConfig
from DBConnections.postgres_db_connection import PostgresDbConnection
from order_sender import OrderSender


class Container(containers.DeclarativeContainer):
    config: Settings = providers.Configuration()

    __db_config = providers.Singleton(
        DbConfig,
        host=config.postgres_host,
        user=config.postgres_user,
        database=config.postgres_database,
        password=config.postgres_password,
    )

    __db_connection = providers.Singleton(PostgresDbConnection, __db_config)

    order_repository_provider = providers.Singleton(
        OrderRepository, connection=__db_connection
    )

    order_sender_provider = providers.Singleton(
        OrderSender,
        # queue_name=config.queue_name,
        rabbitmq_server_host=config.rabbitmq_server_host,
    )
    __merchant_service = providers.Factory(
        ServiceModel,
        host=config.merchant_service_host,
        port=config.merchant_service_port,
        endpoint=config.merchant_service_endpoint,
    )

    merchant_exists_validation_provider = providers.Singleton(
        MerchantExistsValidation, __merchant_service
    )

    merchant_allows_discount_validation_provider = providers.Singleton(
        MerchantAllowsDiscountValidation, __merchant_service
    )

    __buyer_service = providers.Factory(
        ServiceModel,
        host=config.buyer_service_host,
        port=config.buyer_service_port,
        endpoint=config.buyer_service_endpoint,
    )

    buyer_exists_validation_provider = providers.Singleton(
        BuyerExistsValidation, __buyer_service
    )

    __inventory_service = providers.Factory(
        ServiceModel,
        host=config.inventory_service_host,
        port=config.inventory_service_port,
        endpoint=config.inventory_service_endpoint,
    )

    product_exists_validation_provider = providers.Singleton(
        ProductExistsValidation, __inventory_service
    )

    order_validator_provider = providers.Singleton(OrderValidator)
