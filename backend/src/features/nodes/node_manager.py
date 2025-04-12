"""This module manages the list of ESPEasy nodes."""

import datetime
import logging
import threading
from typing import Iterator

import requests
from ampf.base import BaseFactory, KeyNotExistsException

from features.esp_easy import EspEasyService, NodeInfo, NodeReceiver, UdpReceiver
from features.home_assistant import HomeAssistantMqtt

from .discovery_messages_factory import DiscoveryMessagesFactory
from .node_model import Node, NodeHeader


class NodeManager(NodeReceiver):
    """This class manages the list of ESPEasy nodes."""

    _log = logging.getLogger(__name__)

    def __init__(self, factory: BaseFactory, mqtt: HomeAssistantMqtt):
        self.storage = factory.create_storage("nodes", Node, key_name="ip")
        self.factory = DiscoveryMessagesFactory()
        self.mqtt = mqtt
        self._esp_receiver = UdpReceiver(self)
        threading.Thread(target=self._esp_receiver.receive_forever, daemon=True).start()

    def received_node(self, ip: str, name: str, unit_no: int):
        """Add a node to the list of nodes"""
        try:
            node = self.get(ip)
            node.last_seen = datetime.datetime.now()
            self.storage.save(node)
        except KeyNotExistsException:
            try:
                node_info = self.get_node_info(ip)
                node = Node(
                    ip=ip,
                    name=name,
                    unit_no=unit_no,
                    last_seen=datetime.datetime.now(),
                    build=node_info.System.Build,
                    age=node_info.System.Uptime,
                    sensors=node_info.Sensors,
                )
                self.storage.save(node)
            except requests.exceptions.RequestException as e:
                self._log.warning(e)

    async def refresh_node_information(self, ip: str) -> Node:
        node = self.get(ip)
        esp = EspEasyService(ip)
        node_info = await esp.get_node_info()
        node.last_seen = datetime.datetime.now()
        node.mac = node_info.WiFi.STA_MAC
        node.sensors = node_info.Sensors
        node.controllers = await esp.get_controllers()
        self.storage.save(node)
        return node

    def get_node_info(self, ip) -> NodeInfo:
        """Get the node info from the device."""
        req = requests.get("http://" + ip + "/json", timeout=5)
        return NodeInfo.model_validate(req.json())

    def get_all(self) -> Iterator[NodeHeader]:
        return [NodeHeader(**v.model_dump()) for v in self.storage.get_all()]

    def get(self, ip: str) -> Node:
        return self.storage.get(ip)

    def send_discovery_message(self, ip: str) -> None:
        """Send Home Assistant MQTT discovery messages for the node sensors."""
        node = self.get(ip)
        for sensor in node.sensors:
            if sensor.TaskEnabled == "true":
                self._log.debug(
                    " {%d} : %s - %s", sensor.TaskNumber, sensor.TaskName, sensor.Type
                )
                msg = self.factory.create_discovery_message(node, sensor)
                if msg:
                    self.mqtt.send_discovery_message(msg)
