from typing import Annotated

from ampf.base import BaseAsyncFactory
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.concurrency import asynccontextmanager

from app_config import AppConfig
from app_state import AppState
from features.nodes import NodeManager

load_dotenv()


def lifespan(config: AppConfig):
    app_state = AppState.create(config)

    @asynccontextmanager
    async def _lifespan(app: FastAPI):
        app.state.app_state = app_state
        async with app_state.manage_lifecycle(app):
            yield

    return _lifespan


def get_app_state(request: Request) -> AppState:
    return request.app.state.app_state


AppStateDep = Annotated[AppState, Depends(get_app_state)]


def get_config(app_state: AppStateDep) -> AppConfig:
    return app_state.config


AppConfigDep = Annotated[AppConfig, Depends(get_config)]


def get_esp_manager(app_state: AppStateDep):
    return app_state.esp_manager


NodeManagerDep = Annotated[NodeManager, Depends(get_esp_manager)]


def get_factory(app_state: AppStateDep) -> BaseAsyncFactory:
    return app_state.factory


FactoryDep = Annotated[BaseAsyncFactory, Depends(get_factory)]
