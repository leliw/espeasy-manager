from typing import Union
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI
from my_starlette.staticfiles import StaticFiles

import logging

from udp_receive import Node, udp_receive

log = logging.getLogger("main_py")
log.setLevel(logging.DEBUG)


udp_port = 8266
esp_nodes = {}

def receive_call():
    udp_receive(udp_port, esp_nodes)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.debug("Startup event")
    threading.Thread(target=receive_call, daemon=True).start()
    log.debug("Startup event end")
    yield

openapi_tags = [
    {
        "name": "nodes",
        "description": "List of ESPEasy nodes",
    },
]


app = FastAPI(lifespan=lifespan, openapi_tags=openapi_tags)

@app.get("/api/nodes", tags=["nodes"])
async def read_nodes() -> list[Node]:
    return [v for (_, v) in esp_nodes.items()]

# Angular static files
app.mount("/", StaticFiles(directory="static/browser", html = True), name="static")