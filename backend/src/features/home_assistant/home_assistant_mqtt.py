import logging
from threading import Event

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
        self._connected = Event()
        self._connect_error = None

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self._on_connect

        if user:
            self.mqtt_client.username_pw_set(user, password)

        _log.info("Connecting: %s:%d", host, port)
        self.mqtt_client.connect(host, port, keepalive)
        self.mqtt_client.loop_start()

        if not self._connected.wait(timeout=10):
            self.close()
            raise TimeoutError("Timeout while connecting to MQTT broker")

        if self._connect_error:
            self.close()
            raise ConnectionError(self._connect_error)

    def _on_connect(self, client, userdata, flags, reason_code, *args):
        failed = getattr(reason_code, "is_failure", None)
        if failed is None:  # zgodność ze starszym Paho
            failed = reason_code != 0

        if failed:
            self._connect_error = f"MQTT connection failed: {reason_code}"

        self._connected.set()

    def send_discovery_message(self, msg: DiscoveryMessage):
        """Send a Home Assistant MQTT discovery message."""
        _log.debug("Sending: %s", msg.model_dump_json(indent=2, exclude_none=True))

        info = self.mqtt_client.publish(
            msg.topic,
            msg.payload.model_dump_json(exclude_none=True),
            qos=0,
            retain=True,
        )

        if info.rc != mqtt.MQTT_ERR_SUCCESS:
            raise RuntimeError(f"MQTT publish failed, rc={info.rc}")

        info.wait_for_publish(timeout=10)
        if not info.is_published():
            raise TimeoutError(f"MQTT message was not sent: {msg.topic}")

    def close(self):
        self.mqtt_client.disconnect()
        self.mqtt_client.loop_stop()
