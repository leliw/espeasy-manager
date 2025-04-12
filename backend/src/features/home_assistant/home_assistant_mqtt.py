import logging

import paho.mqtt.client as mqtt

from .home_assistant_model import DiscoveryMessage


class HomeAssistantMqtt:
    _log = logging.getLogger(__name__)

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
