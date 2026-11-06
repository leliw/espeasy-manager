import logging

import paho.mqtt.client as mqtt

from .home_assistant_model import DiscoveryMessage

_log = logging.getLogger(__name__)


class HomeAssistantMqtt:
    def __init__(
        self,
        host: str,
        port: int,
        user: str | None = None,
        password: str | None = None,
        keepalive: int = 60,
    ):
        _log.info("Connecting: %s:%d", host, port)
        self.mqtt_client = mqtt.Client()
        if user:
            self.mqtt_client.username_pw_set(user, password)
        self.mqtt_client.connect(host, port, keepalive)

    def send_discovery_message(self, msg: DiscoveryMessage):
        """Send a Home Assistant MQTT discovery message."""
        _log.debug("Sending: %s", msg.model_dump_json(indent=2, exclude_none=True))
        ret = self.mqtt_client.publish(
            msg.topic,
            msg.payload.model_dump_json(exclude_none=True),
            qos=0,
            retain=True,
        )
        _log.debug("MQTT publish mid=%s, published=%s", ret.mid, ret.is_published())
