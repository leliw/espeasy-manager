from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.concurrency import asynccontextmanager

from config import ServerConfig
from features.esp_easy import NodeManager, HomeAssistantMqtt

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = ServerConfig()
    app.state.config = config
    mqtt = HomeAssistantMqtt(config.mqtt_host, config.mqtt_port)
    app.state.esp_manager = NodeManager(mqtt)
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
