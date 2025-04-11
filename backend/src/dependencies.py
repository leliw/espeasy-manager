from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.concurrency import asynccontextmanager

from ampf.base import BaseFactory
from ampf.local import LocalFactory

from config import ServerConfig
from features.esp_easy import NodeManager, HomeAssistantMqtt

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = ServerConfig()
    app.state.config = config
    mqtt = HomeAssistantMqtt(config.mqtt_host, config.mqtt_port)
    factory = LocalFactory(app.state.config.data_dir)
    app.state.factory = factory
    app.state.esp_manager = NodeManager(factory, mqtt)
    yield


def get_app(request: Request) -> FastAPI:
    return request.app


AppDep = Annotated[FastAPI, Depends(get_app)]


def get_server_config(app: AppDep) -> ServerConfig:
    return app.state.config


ServerConfigDep = Annotated[ServerConfig, Depends(get_server_config)]


def get_esp_manager(app: AppDep):
    return app.state.esp_manager


NodeManagerDep = Annotated[NodeManager, Depends(get_esp_manager)]

def get_factory(app: FastAPI = Depends(get_app)) -> BaseFactory:
    return app.state.factory


FactoryDep = Annotated[BaseFactory, Depends(get_factory)]