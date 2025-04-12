from typing import List, Optional, Tuple

from pydantic import BaseModel

class Device(BaseModel):
    """Home Assistant MQTT discovery message device format."""

    configuration_url: Optional[str] = None
    connections: Optional[List[Tuple[str, str]]] = None
    hw_version: Optional[str] = None
    identifiers: Optional[list[str]] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    name: Optional[str] = None
    serial_number: Optional[str] = None
    suggested_area: Optional[str] = None
    sw_version: Optional[str] = None
    via_device: Optional[str] = None

# See: https://www.home-assistant.io/integrations/mqtt#mqtt-discovery
class DiscoveryPayload(BaseModel):
    """Home Assistant MQTT discovery message payload format."""

    name: str
    unique_id: Optional[str] = None
    icon: Optional[str] = None
    platform: str
    device: Optional[Device] = None
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
