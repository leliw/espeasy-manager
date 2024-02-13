"""ESPEasy REST API"""
from typing import Union
import logging
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import ESPEasy
from static_file_response import static_file_response

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main_py")
log.setLevel(logging.INFO)

@asynccontextmanager
async def lifespan(_: FastAPI):
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
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(_: Request, full_path: str):
    """Catch all for Angular routing"""
    return static_file_response("static/browser", full_path)
