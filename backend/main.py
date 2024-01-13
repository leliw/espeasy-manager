from typing import Union
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI
from my_starlette.staticfiles import StaticFiles
import ESPEasy
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("main_py")
log.setLevel(logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.debug("Startup event")
    threading.Thread(target=ESPEasy.udp_receive, daemon=True).start()
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
async def read_nodes() -> list[ESPEasy.NodeHeader]:
    return ESPEasy.get_nodes()

# Angular static files
app.mount("/", StaticFiles(directory="static/browser", html = True), name="static")