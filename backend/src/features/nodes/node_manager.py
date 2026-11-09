"""This module manages the list of ESPEasy nodes."""

import asyncio
import datetime
import logging
from collections.abc import AsyncGenerator

import httpx2
from ampf.base import BaseAsyncFactory, KeyNotExistsException

from features.esp_easy import EspEasyService, NodeInfo, NodeReceiver, UdpReceiver
from features.home_assistant import HomeAssistantMqtt

from .discovery_messages_factory import DiscoveryMessagesFactory
from .node_model import Node, NodeHeader


class NodeManager(NodeReceiver):
    """This class manages the list of ESPEasy nodes."""

    _log = logging.getLogger(__name__)

    def __init__(self, factory: BaseAsyncFactory, mqtt: HomeAssistantMqtt):
        self.storage = factory.create_storage("nodes", Node, key="ip")
        self.factory = DiscoveryMessagesFactory()
        self.mqtt = mqtt
        self._esp_receiver = UdpReceiver(self)

    # NodeManager
    async def start(self):
        self._receiver_task = asyncio.create_task(self._esp_receiver.receive_forever())

    async def stop(self):
        self._receiver_task.cancel()
        await asyncio.gather(self._receiver_task, return_exceptions=True)

    async def received_node(self, ip: str, name: str, unit_no: int):
        """Add a node to the list of nodes"""
        try:
            node = await self.get(ip)
            node.name = name
            node.unit_no = unit_no
            node.last_seen = datetime.datetime.now()
            await self.storage.save(node)
        except KeyNotExistsException:
            try:
                node_info = await self.get_node_info(ip)
                node = Node(
                    ip=ip,
                    name=name,
                    unit_no=unit_no,
                    last_seen=datetime.datetime.now(),
                    build=node_info.System.Build,
                    age=node_info.System.Uptime,
                    sensors=node_info.Sensors,
                )
                await self.storage.save(node)
            except httpx2.HTTPError as e:
                self._log.warning("Nie udało się pobrać danych z %s: %s", ip, e)

    async def refresh_node_information(self, ip: str) -> Node:
        node = await self.get(ip)
        esp = EspEasyService(ip)
        node_info = await esp.get_node_info()
        node.last_seen = datetime.datetime.now()
        node.mac = node_info.WiFi.STA_MAC
        node.sensors = node_info.Sensors
        node.controllers = await esp.get_controllers()
        await self.storage.save(node)
        return node

    async def get_node_info(self, ip: str) -> NodeInfo:
        async with httpx2.AsyncClient(timeout=5) as client:
            response = await client.get(f"http://{ip}/json")
            response.raise_for_status()
            return NodeInfo.model_validate(response.json())

    async def get_all(self) -> AsyncGenerator[NodeHeader]:
        async for v in self.storage.get_all():
            yield NodeHeader(**v.model_dump())

    async def get(self, ip: str) -> Node:
        return await self.storage.get(ip)

    async def send_discovery_message(self, ip: str) -> None:
        """Send Home Assistant MQTT discovery messages for the node sensors."""
        node = await self.get(ip)
        for sensor in node.sensors:
            if sensor.TaskEnabled == "true":
                self._log.debug(" {%d} : %s - %s", sensor.TaskNumber, sensor.TaskName, sensor.Type)
                msg = self.factory.create_discovery_message(node, sensor)
                if msg:
                    self.mqtt.send_discovery_message(msg)
