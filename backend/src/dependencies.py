from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.concurrency import asynccontextmanager

from config import ServerConfig

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.config = ServerConfig()
    yield


def get_app(request: Request) -> FastAPI:
    return request.app


AppDep = Annotated[FastAPI, Depends(get_app)]


def get_server_config(app: FastAPI = Depends(get_app)) -> ServerConfig:
    return app.state.config


ServerConfigDep = Annotated[ServerConfig, Depends(get_server_config)]
