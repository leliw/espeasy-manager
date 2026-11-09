from fastapi import APIRouter
from pydantic import BaseModel

from dependencies import AppConfigDep

router = APIRouter(tags=["Client config"])


class ClientConfig(BaseModel):
    version: str


@router.get("")
async def get_client_config(server_config: AppConfigDep) -> ClientConfig:
    return ClientConfig(**server_config.model_dump())
