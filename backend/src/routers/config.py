from fastapi import APIRouter

from config import ClientConfig
from dependencies import ServerConfigDep

router = APIRouter(tags=["Client config"])


@router.get("")
async def get_client_config(server_config: ServerConfigDep) -> ClientConfig:
    return ClientConfig(**server_config.model_dump())
