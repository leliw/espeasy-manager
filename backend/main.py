"""ESPEasy REST API"""
from typing import Union
import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

import esp_easy
from static_file_response import static_file_response

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main_py")
log.setLevel(logging.INFO)

esp_manager = esp_easy.NodeManager()

openapi_tags = [
    {
        "name": "nodes",
        "description": "List of ESPEasy nodes",
    },
]

app = FastAPI(openapi_tags=openapi_tags)

@app.get("/api/nodes", tags=["nodes"])
async def read_nodes() -> list[esp_easy.NodeHeader]:
    """Returns a list of all nodes"""
    return esp_manager.get_nodes()

@app.get("/api/nodes/{ip}", tags=["nodes"])
async def read_node(ip: str) -> Union[esp_easy.NodeInfo, None]:
    """Returns a node by ip"""
    return esp_manager.get_node(ip)

# Angular static files
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(_: Request, full_path: str):
    """Catch all for Angular routing"""
    return static_file_response("static/browser", full_path)
