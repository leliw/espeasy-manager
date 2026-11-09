from ampf.fastapi import get_static_file_response
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app_config import AppConfig
from dependencies import lifespan
from log_config import setup_logging
from routers import config, nodes

load_dotenv()
setup_logging()
app_config = AppConfig()
app = FastAPI(
    title="ESPEasy Manager",
    lifespan=lifespan(app_config),
)

# Include the client config router
app.include_router(config.router, prefix="/api/config")
app.include_router(nodes.router, prefix="/api/nodes")


@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    if not (full_path == "api" or full_path.startswith("api/")):
        return await get_static_file_response("static/browser", full_path)
    else:
        raise HTTPException(status_code=404, detail="Not found")
