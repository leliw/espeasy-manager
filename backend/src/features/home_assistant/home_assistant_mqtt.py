import asyncio
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
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._keepalive = keepalive

        self._connected = Event()
        self._connect_error = None
        self._loop_started = False

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self._on_connect

        if user:
            self.mqtt_client.username_pw_set(user, password)

    async def __aenter__(self):
        try:
            await asyncio.to_thread(self._connect)
        except Exception:
            await asyncio.to_thread(self._close)
            raise

        return self

    async def __aexit__(self, exc_type, exc, tb):
        await asyncio.to_thread(self._close)
        return False  # nie tłumacz wyjątków z bloku async with

    def _connect(self):
        _log.info("Connecting: %s:%d", self._host, self._port)
        self.mqtt_client.connect(self._host, self._port, self._keepalive)
        self.mqtt_client.loop_start()
        self._loop_started = True

        if not self._connected.wait(timeout=10):
            raise TimeoutError("Timeout while connecting to MQTT broker")

        if self._connect_error:
            raise ConnectionError(self._connect_error)

    def _on_connect(self, client, userdata, flags, reason_code, *args):
        failed = getattr(reason_code, "is_failure", None)
        if failed is None:  # zgodność ze starszym Paho
            failed = reason_code != 0

        if failed:
            self._connect_error = f"MQTT connection failed: {reason_code}"

        self._connected.set()

    async def send_discovery_message(self, msg: DiscoveryMessage):
        await asyncio.to_thread(self._send_discovery_message, msg)

    def _send_discovery_message(self, msg: DiscoveryMessage):
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

    def _close(self):
        if self._loop_started:
            try:
                self.mqtt_client.disconnect()
            finally:
                self.mqtt_client.loop_stop()
                self._loop_started = False
