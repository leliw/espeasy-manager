from typing import Optional

from pydantic import BaseModel


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
