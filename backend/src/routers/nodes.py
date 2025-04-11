from typing import Iterable

from fastapi import APIRouter

from dependencies import NodeManagerDep
from features.nodes import Node, NodeHeader

router = APIRouter(tags=["ESP Easy Nodes"])


@router.get("")
async def get_all(node_manager: NodeManagerDep) -> Iterable[NodeHeader]:
    """Returns a list of all nodes"""
    return node_manager.get_all()


@router.get("/{ip}")
async def get(node_manager: NodeManagerDep, ip: str) -> Node:
    """Returns a node by ip"""
    return node_manager.get(ip)

@router.post("/{ip}/refresh")
async def refresh_node_information(node_manager: NodeManagerDep,ip: str) -> Node:
    return await node_manager.refresh_node_information(ip)

@router.post("/{ip}/send-discovery-message")
async def send_discovery_message(node_manager: NodeManagerDep,ip: str) -> None:
    """Send a Home Assistant MQTT discovery message for the node sensors."""
    node_manager.send_discovery_message(ip)
