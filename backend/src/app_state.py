import logging
from dataclasses import dataclass

import httpx2
from ampf.base import BaseAsyncFactory
from ampf.fastapi import BaseAppState

from app_config import AppConfig
from features.home_assistant.home_assistant_mqtt import HomeAssistantMqtt
from features.nodes.node_manager import NodeManager
from storage_def import STORAGE_DEF

_log = logging.getLogger(__name__)


@dataclass(kw_only=True)
class AppState(BaseAppState):
    config: AppConfig
    factory: BaseAsyncFactory
    httpx_client: httpx2.AsyncClient
    mqtt: HomeAssistantMqtt
    esp_manager: NodeManager

    @classmethod
    def create(cls, config: AppConfig) -> "AppState":
        httpx_client = httpx2.AsyncClient()
        if config.data_dir:
            from ampf.local import LocalAsyncFactory

            factory = LocalAsyncFactory(config.data_dir)
            _log.info(f"Local storage: {config.data_dir}")
        elif not config.production:
            from ampf.in_memory import InMemoryAsyncFactory

            factory = InMemoryAsyncFactory()
            _log.warning("InMemoryFactory is used - it's only for tests!")
        else:
            raise ValueError("No factory setup!")
        factory.register_collections(STORAGE_DEF)

        mqtt = HomeAssistantMqtt(config.mqtt_host, config.mqtt_port, config.mqtt_user, config.mqtt_pass)
        esp_manager = NodeManager(factory, mqtt, httpx_client)
        return cls(
            config=config,
            factory=factory,
            httpx_client=httpx_client,
            mqtt=mqtt,
            esp_manager=esp_manager,
        )
