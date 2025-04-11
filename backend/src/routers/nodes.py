from typing import Iterable

from fastapi import APIRouter

from dependencies import NodeManagerDep
from features.nodes import Node, NodeHeader

router = APIRouter(tags=["ESP Easy Nodes"])


@router.get("")
async def read_nodes(node_manager: NodeManagerDep) -> Iterable[NodeHeader]:
    """Returns a list of all nodes"""
    return node_manager.get_all()


@router.get("/{ip}")
async def read_node(node_manager: NodeManagerDep, ip: str) -> Node:
    """Returns a node by ip"""
    return node_manager.get(ip)
