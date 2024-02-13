"""ESPEasy REST API"""
import os
from typing import Union
import logging
import threading
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
import ESPEasy

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
    request_path = Path("static/browser") / full_path
    if request_path.exists() and request_path.is_file():
        file_extension = os.path.splitext(request_path)[1]
        match file_extension:
            case ".js":
                media_type = "text/javascript"
            case ".css":
                media_type = "text/css"
            case ".ico":
                media_type = "image/x-icon"
            case _:
                media_type = "text/html"
        return HTMLResponse(content=request_path.read_text(), 
                            status_code=200, 
                            headers={"Content-Type": media_type})
    index_path = Path("static/browser") / 'index.html'
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Page not found")
    return HTMLResponse(content=index_path.read_text(), status_code=200)
