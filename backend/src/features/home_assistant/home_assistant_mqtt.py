"""This module provides a class to send Home Assistant MQTT discovery messages."""

from typing import Optional
from pydantic import BaseModel
import paho.mqtt.client as mqtt
from unidecode import unidecode


# See: https://www.home-assistant.io/integrations/mqtt#mqtt-discovery
class DiscoveryPayload(BaseModel):
    """Home Assistant MQTT discovery message payload format."""

    name: str
    unique_id: Optional[str] = None
    icon: Optional[str] = None
    device_class: str
    state_topic: str
    unit_of_measurement: Optional[str] = None
    state_on: Optional[str] = None
    state_off: Optional[str] = None
    command_topic: Optional[str] = None
    payload_on: Optional[str] = None
    payload_off: Optional[str] = None


class DiscoveryMessage(BaseModel):
    topic: str
    payload: DiscoveryPayload


class HomeAssistantMqtt:
    def __init__(self, host: str, port: int = 1883, keepalive: int = 60):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(host, port, keepalive)

    def send_discovery_message(self, msg: DiscoveryMessage):
        """Send a Home Assistant MQTT discovery message."""
        self.mqtt_client.publish(
            msg.topic,
            msg.payload.model_dump_json(exclude_none=True),
            qos=0,
            retain=True,
        )

    def create_discovery_message(
        self,
        node_name: str,
        task_name: str,
        task_number: int,
        value_name: str,
        device_type: str,
    ) -> DiscoveryMessage:
        """Create a Home Assistant MQTT discovery message."""
        unique_id = f"{node_name}_{task_name}_{value_name}"
        state_topic = f"{node_name}/{task_name}/{value_name}"
        name = node_name.replace("_", " ") + " - " + task_name.replace("_", " ")
        if device_type == "Environment - DS18b20":
            entity_type = "sensor"
            payload = DiscoveryPayload(
                name=name,
                device_class="temperature",
                unique_id=unique_id,
                state_topic=state_topic,
                unit_of_measurement="°C",
            )
        elif value_name == "State":
            entity_type = "switch"
            payload = DiscoveryPayload(
                name=name,
                device_class="switch",
                unique_id=unique_id,
                state_topic=state_topic,
                icon="mdi:light-switch",
                unit_of_measurement=None,
                command_topic=node_name + "/cmd",
                payload_on="TaskValueSet," + str(task_number) + ",1,1",
                payload_off="TaskValueSet," + str(task_number) + ",1,0",
                state_on="1",
                state_off="0",
            )
        else:
            return None
        discovery_topic = unidecode(
            f"homeassistant/{entity_type}/{node_name}/{task_name}/config"
        )
        return DiscoveryMessage(topic=discovery_topic, payload=payload)
