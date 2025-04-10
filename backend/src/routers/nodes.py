from typing import Union

from fastapi import APIRouter

from dependencies import NodeManagerDep
from features.esp_easy import NodeHeader, NodeInfo

router = APIRouter(tags=["ESP Easy Nodes"])


@router.get("")
async def read_nodes(esp_manager: NodeManagerDep) -> list[NodeHeader]:
    """Returns a list of all nodes"""
    return esp_manager.get_nodes()


@router.get("/{ip}")
async def read_node(esp_manager: NodeManagerDep, ip: str) -> Union[NodeInfo, None]:
    """Returns a node by ip"""
    return esp_manager.get_node(ip)
