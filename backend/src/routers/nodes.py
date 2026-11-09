from ampf.fastapi import JsonStreamingResponse
from fastapi import APIRouter

from dependencies import NodeManagerDep
from features.nodes import Node, NodeHeader

router = APIRouter(tags=["ESP Easy Nodes"])


@router.get("", response_model=list[NodeHeader])
async def get_all(node_manager: NodeManagerDep) -> JsonStreamingResponse:
    """Returns a list of all nodes"""
    return JsonStreamingResponse(node_manager.get_all())


@router.get("/{ip}")
async def get(node_manager: NodeManagerDep, ip: str) -> Node:
    """Returns a node by ip"""
    return await node_manager.get(ip)


@router.post("/{ip}/refresh")
async def refresh_node_information(node_manager: NodeManagerDep, ip: str) -> Node:
    return await node_manager.refresh_node_information(ip)


@router.post("/{ip}/send-discovery-message")
async def send_discovery_message(node_manager: NodeManagerDep, ip: str) -> None:
    """Send a Home Assistant MQTT discovery message for the node sensors."""
    await node_manager.send_discovery_message(ip)
