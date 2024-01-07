from typing import Union
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI
from my_starlette.staticfiles import StaticFiles
from pydantic import BaseModel

import logging

import udp_receive

udp_port = 8266
esp_nodes = {}

class Node(BaseModel):
    ip: str
    name: str
    unit_no: int

log = logging.getLogger("main_py")
log.setLevel(logging.DEBUG)

def receive_call():
    udp_receive.udp_receive(udp_port, esp_nodes)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.debug("Startup event")
    threading.Thread(target=receive_call, daemon=True).start()
    log.debug("Startup event end")
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/api/nodes")
async def read_nodes() -> list[Node]:
    return [v for (_, v) in esp_nodes.items()]

# Angular static files
app.mount("/", StaticFiles(directory="static/browser", html = True), name="static")