import logging

from unidecode import unidecode

from features.esp_easy import Sensor
from features.home_assistant import DiscoveryMessage, DiscoveryPayload

from .node_model import Node

_log = logging.getLogger(__name__)


class DiscoveryMessagesFactory:
    """Factory for creating Home Assistant MQTT discovery messages."""

    def create_discovery_message(self, node: Node, sensor: Sensor) -> DiscoveryMessage | None:
        """Create a Home Assistant MQTT discovery message."""
        task_name = sensor.TaskName
        value_name = sensor.TaskValues[0].Name
        unique_id = f"{node.name}_{task_name}_{value_name}"
        state_topic = f"{node.name}/{task_name}/{value_name}"
        name = node.name.replace("_", " ") + " - " + task_name.replace("_", " ")
        _log.info("create_discovery_message %s - %s", sensor.Type, value_name)
        common = {
            "name": name,
            "unique_id": unique_id,
            "state_topic": state_topic,
            "unit_of_measurement": None,
        }
        switch_icons = {
            "State": "mdi:light-switch",
            "Light": "mdi:lightbulb",
            "Level": "mdi:gauge",
            "Valve": "mdi:heating-coil",
            "Zawor": "mdi:heating-coil",
            "Zawór": "mdi:heating-coil",
        }
        icon = switch_icons.get(value_name)

        if sensor.Type in {
            "Environment - DS18b20",
            "Environment - 1-Wire Temperature",
        }:
            entity_type = "sensor"
            options = {
                "platform": "temperature",
                "unit_of_measurement": "°C",
            }

        elif sensor.Type == "Generic - Dummy Device":
            entity_type = "switch"
            options = {
                "platform": "switch",
                "icon": icon,
                "state_on": "1",
                "state_off": "0",
                "command_topic": f"{node.name}/cmd",
                "payload_on": f"TaskValueSet,{sensor.TaskNumber},1,1",
                "payload_off": f"TaskValueSet,{sensor.TaskNumber},1,0",
            }

        elif value_name == "Level":
            entity_type = "sensor"
            options = {
                "platform": "sensor",
                "icon": icon,
            }

        else:
            if icon is None:
                return None

            entity_type = "switch"
            options = {
                "platform": "switch",
                "icon": icon,
                "state_on": "1",
                "state_off": "0",
                "command_topic": f"{node.name}/cmd",
                "payload_on": f"GPIO,{sensor.TaskDeviceGPIO1},1",
                "payload_off": f"GPIO,{sensor.TaskDeviceGPIO1},0",
            }

        payload = DiscoveryPayload.model_validate({**common, **options})
        topic = unidecode(f"homeassistant/{entity_type}/{node.name}/{task_name}/config")
        return DiscoveryMessage(topic=topic, payload=payload)
