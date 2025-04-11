from typing import List

import httpx

from features.esp_easy.esp_easy_model import Controller, NodeInfo
from features.esp_easy.html_parser import HtmlParser


class EspEasyService:
    """Service to communicate with ESPEasy devices."""

    def __init__(self, ip: str):
        self.ip = ip

    async def get_node_info(self) -> NodeInfo:
        """Get the node info from the device."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://{self.ip}/json")
            response.raise_for_status()
            return NodeInfo.model_validate(response.json())
    
    async def get_controllers(self) -> List[Controller]:
        """Get the controllers from the device."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://{self.ip}/controllers")
            response.raise_for_status()
            parser = HtmlParser(response.text)
            return parser.parse_controllers()

