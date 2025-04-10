from ampf.fastapi import StaticFileResponse
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from config import ServerConfig
from dependencies import lifespan
from log_config import setup_logging
from routers import config, nodes

load_dotenv()
setup_logging()
app = FastAPI(lifespan=lifespan)

# Initialize the server configuration
server_config = ServerConfig()

# Include the client config router
app.include_router(config.router, prefix="/api/config")
app.include_router(nodes.router, prefix="/api/nodes")


@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    if not full_path.startswith("api/"):
        return StaticFileResponse("static/browser", full_path)
    else:
        raise HTTPException(status_code=404, detail="Not found")
