"""ESPEasy REST API"""
from typing import Union
import logging
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI
from my_starlette.staticfiles import StaticFiles
import ESPEasy

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("main_py")
log.setLevel(logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup event"""
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
    """Returns a list of all nodes"""
    return ESPEasy.get_nodes()

@app.get("/api/nodes/{ip}", tags=["nodes"])
async def read_node(ip: str) -> Union[ESPEasy.NodeInfo, None]:
    """Returns a node by ip"""
    return ESPEasy.get_node(ip)

# Angular static files
app.mount("/", StaticFiles(directory="static/browser", html = True), name="static")
