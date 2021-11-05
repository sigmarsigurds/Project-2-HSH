from dependency_injector import containers, providers

import src.Infrastructure.settings as settings
from src.ApiModels import ServiceModel


class Container(containers.DeclarativeContainer):
    config: settings.Settings = providers.Configuration()

    order_service_endpoint_provider = providers.Singleton(ServiceModel,
                                                          host=config.order_service_host,
                                                          port=config.order_service_port)

    merchant_service_endpoint_provider = providers.Singleton(ServiceModel,
                                                             host=config.merchant_service_host,
                                                             port=config.merchant_service_port)

    buyer_service_endpoint_provider = providers.Singleton(ServiceModel,
                                                          host=config.buyer_service_host,
                                                          port=config.buyer_service_port)

    inventory_service_endpoint_provider = providers.Singleton(ServiceModel,
                                                              host=config.inventory_service_host,
                                                              port=config.inventory_service_port)
