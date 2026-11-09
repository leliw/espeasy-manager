from typing import Annotated

from ampf.base import BaseAsyncFactory
from ampf.local import LocalAsyncFactory
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.concurrency import asynccontextmanager

from app_config import AppConfig
from features.home_assistant import HomeAssistantMqtt
from features.nodes import NodeManager

load_dotenv()


def lifespan(config: AppConfig):

    @asynccontextmanager
    async def _lifespan(app: FastAPI):
        app.state.config = config
        mqtt = HomeAssistantMqtt(config.mqtt_host, config.mqtt_port, config.mqtt_user, config.mqtt_pass)
        try:
            factory = LocalAsyncFactory(app.state.config.data_dir)
            app.state.factory = factory
            app.state.esp_manager = NodeManager(factory, mqtt)
            async with app.state.esp_manager:
                yield
        finally:
            mqtt.close()

    return _lifespan


def get_app(request: Request) -> FastAPI:
    return request.app


AppDep = Annotated[FastAPI, Depends(get_app)]


def get_server_config(app: AppDep) -> AppConfig:
    return app.state.config


AppConfigDep = Annotated[AppConfig, Depends(get_server_config)]


def get_esp_manager(app: AppDep):
    return app.state.esp_manager


NodeManagerDep = Annotated[NodeManager, Depends(get_esp_manager)]


def get_factory(app: AppDep) -> BaseAsyncFactory:
    return app.state.factory


FactoryDep = Annotated[BaseAsyncFactory, Depends(get_factory)]
