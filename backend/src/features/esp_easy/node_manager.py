"""This module manages the list of ESPEasy nodes."""

import datetime
import logging
import os
import threading
from typing import Iterator

import requests
from ampf.base import BaseFactory, KeyNotExistsException

from features.nodes import Node, NodeHeader

from .home_assistant_mqtt import DiscoveryMessage, HomeAssistantMqtt
from .model import NodeInfo
from .udp_receiver import NodeReceiver, UdpReceiver


class NodeManager(NodeReceiver):
    """This class manages the list of ESPEasy nodes."""

    _log = logging.getLogger(__name__)

    def __init__(self, factory: BaseFactory, mqtt: HomeAssistantMqtt):
        self.storage = factory.create_storage("nodes", Node, key_name="ip")
        self.mqtt = mqtt
        self._esp_nodes = {}
        self._esp_receiver = UdpReceiver(self)
        threading.Thread(target=self._esp_receiver.receive_forever, daemon=True).start()

    def received_node(self, ip: str, name: str, unit_no: int):
        """Add a node to the list of nodes"""
        try:
            node = self.get(ip)
            node.last_seen = datetime.datetime.now()
            self.storage.save(node)
        except KeyNotExistsException:
            self._esp_nodes[ip] = {
                "ip": ip,
                "name": name,
                "unit_no": unit_no,
                "last_seen": datetime.datetime.now(),
            }
            try:
                node_info = self.get_node_info(ip)
                self.save_node(node_info)
                node = Node(
                    ip=ip,
                    name=name,
                    unit_no=unit_no,
                    last_seen=datetime.datetime.now(),
                    build=node_info.System.Build,
                    age=node_info.System.Uptime,
                    Sensors=node_info.Sensors,
                )
                self.storage.save(node)
                if unit_no in [31, 33, 61]:
                    self.send_node_info(node_info)
            except requests.exceptions.RequestException as e:
                self._log.warning(e)

    def get_node_info(self, ip) -> NodeInfo:
        """Get the node info from the device."""
        req = requests.get("http://" + ip + "/json", timeout=5)
        return NodeInfo.model_validate(req.json())

    def get_all(self) -> Iterator[NodeHeader]:
        return [NodeHeader(**v.model_dump()) for v in self.storage.get_all()]

    def get(self, ip: str) -> Node:
        return self.storage.get(ip)

    def save_node(self, node_info: NodeInfo):
        """Save the node info to a file."""
        json = node_info.model_dump_json(exclude_none=True)
        os.makedirs("data", exist_ok=True)
        file = "data/" + node_info.System.Unit_Name + ".json"
        with open(file, "tw", encoding="UTF-8") as outfile:
            outfile.write(json)

    def send_node_info(self, node_info: NodeInfo):
        """Send Home Assistant MQTT discovery messages for the node sensors."""
        node_name = node_info.System.Unit_Name
        for sensor in node_info.Sensors:
            if sensor.TaskEnabled == "true":
                self._log.debug(
                    " {%d} : %s - %s", sensor.TaskNumber, sensor.TaskName, sensor.Type
                )
                entity_type, msg = self.create_discovery_message(
                    node_name,
                    sensor.TaskName,
                    sensor.TaskNumber,
                    sensor.TaskValues[0].Name,
                    sensor.Type,
                )
                if msg:
                    self._log.debug(
                        "Sending discovery message: %s",
                        msg.model_dump_json(exclude_none=True),
                    )
                    self.mqtt.send_discovery_message(entity_type, msg)

    def create_discovery_message(
        self,
        node_name: str,
        task_name: str,
        task_number: int,
        value_name: str,
        device_type: str,
    ) -> tuple[str, DiscoveryMessage]:
        """Create a Home Assistant MQTT discovery message."""
        unique_id = node_name + "_" + task_name + "_" + value_name
        state_topic = node_name + "/" + task_name + "/" + value_name
        name = node_name.replace("_", " ") + " - " + task_name.replace("_", " ")
        if device_type == "Environment - DS18b20":
            msg = DiscoveryMessage(
                name=name,
                device_class="temperature",
                unique_id=unique_id,
                state_topic=state_topic,
            )
            msg.unit_of_measurement = "°C"
            return ("sensor", msg)
        elif value_name == "State":
            msg = DiscoveryMessage(
                name=name,
                device_class="switch",
                unique_id=unique_id,
                state_topic=state_topic,
            )
            msg.icon = "mdi:light-switch"
            msg.unit_of_measurement = None
            msg.command_topic = node_name + "/cmd"
            msg.payload_on = "TaskValueSet," + str(task_number) + ",1,1"
            msg.payload_off = "TaskValueSet," + str(task_number) + ",1,0"
            msg.state_on = "1"
            msg.state_off = "0"
            return ("switch", msg)
        else:
            return (None, None)
