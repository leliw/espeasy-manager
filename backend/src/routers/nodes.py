from typing import Union

from fastapi import APIRouter

from features import esp_easy

router = APIRouter(tags=["ESP Easy Nodes"])

esp_manager = esp_easy.NodeManager()


@router.get("")
async def read_nodes() -> list[esp_easy.NodeHeader]:
    """Returns a list of all nodes"""
    return esp_manager.get_nodes()


@router.get("/{ip}")
async def read_node(ip: str) -> Union[esp_easy.NodeInfo, None]:
    """Returns a node by ip"""
    return esp_manager.get_node(ip)
