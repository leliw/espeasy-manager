from unidecode import unidecode

from features.esp_easy import Sensor
from features.home_assistant import DiscoveryMessage, DiscoveryPayload

from .node_model import Node


class DiscoveryMessagesFactory:
    """Factory for creating Home Assistant MQTT discovery messages."""

    def __init__(self):
        pass

    def create_discovery_message(self, node: Node, sensor: Sensor) -> DiscoveryMessage:
        """Create a Home Assistant MQTT discovery message."""
        task_name = sensor.TaskName
        value_name = sensor.TaskValues[0].Name
        unique_id = f"{node.name}_{task_name}_{value_name}"
        state_topic = f"{node.name}/{task_name}/{value_name}"
        name = node.name.replace("_", " ") + " - " + task_name.replace("_", " ")
        if sensor.Type == "Environment - DS18b20":
            entity_type = "sensor"
            payload = DiscoveryPayload(
                name=name,
                platform="temperature",
                unique_id=unique_id,
                state_topic=state_topic,
                unit_of_measurement="°C",
            )
        elif value_name == "State":
            entity_type = "switch"
            payload = DiscoveryPayload(
                name=name,
                platform="switch",
                unique_id=unique_id,
                state_topic=state_topic,
                icon="mdi:light-switch",
                unit_of_measurement=None,
                command_topic=node.name + "/cmd",
                payload_on=f"GPIO,{sensor.TaskDeviceGPIO1},1",
                payload_off=f"GPIO,{sensor.TaskDeviceGPIO1},0",
                state_on="1",
                state_off="0",
                # device=Device(suggested_area="Garaż", connections=[("mac", "02:5b:26:a8:dc:12")]),
            )
        else:
            return None
        discovery_topic = unidecode(
            f"homeassistant/{entity_type}/{node.name}/{task_name}/config"
        )
        return DiscoveryMessage(topic=discovery_topic, payload=payload)
