from dependency_injector import containers, providers
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
        queue_name=config.queue_name,
        rabbitmq_server=config.rabbitmq_server,
    )

    merchant_exists_validation_provider = providers.Singleton(
        MerchantExistsValidation, "http://merchant-service-api:8001/merchants/"
    )

    merchant_allows_discount_validation_provider = providers.Singleton(
        MerchantAllowsDiscountValidation, "http://merchant-service-api:8001/merchants/"
    )

    buyer_exists_validation_provider = providers.Singleton(
        BuyerExistsValidation, "http://buyer_container:8002/buyers/"
    )

    order_validator_provider = providers.Singleton(OrderValidator)