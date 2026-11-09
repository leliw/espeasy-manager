import importlib
import logging
from collections.abc import Generator

import pytest
from ampf.testing import ApiTestClient
from fastapi import FastAPI

import main
from app_config import AppConfig
from dependencies import lifespan
from log_config import setup_logging

_log = logging.getLogger(__name__)


@pytest.fixture
def config() -> AppConfig:
    return AppConfig()

@pytest.fixture
def app(config: AppConfig) -> FastAPI:
    setup_logging()
    importlib.reload(main)
    app = main.app
    # Reconfigure the lifespan to use the test server config
    app.router.lifespan_context = lifespan(config)
    return app

@pytest.fixture
def client(app: FastAPI) -> Generator[ApiTestClient]:
    with ApiTestClient(app) as client:
        yield client
