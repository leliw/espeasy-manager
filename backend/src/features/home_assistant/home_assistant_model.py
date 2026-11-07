from pydantic import BaseModel, computed_field


class Device(BaseModel):
    """Home Assistant MQTT discovery message device format."""

    configuration_url: str | None = None
    connections: list[tuple[str, str]] | None = None
    hw_version: str | None = None
    identifiers: list[str] | None = None
    manufacturer: str | None = None
    model: str | None = None
    name: str | None = None
    serial_number: str | None = None
    suggested_area: str | None = None
    sw_version: str | None = None
    via_device: str | None = None


# See: https://www.home-assistant.io/integrations/mqtt#mqtt-discovery
class DiscoveryPayload(BaseModel):
    """Home Assistant MQTT discovery message payload format."""

    name: str
    unique_id: str | None = None
    icon: str | None = None
    platform: str
    device: Device | None = None
    state_topic: str
    unit_of_measurement: str | None = None
    state_on: str | None = None
    state_off: str | None = None
    command_topic: str | None = None
    payload_on: str | None = None
    payload_off: str | None = None


    @computed_field
    @property
    def device_class(self) -> str:
        return self.platform

class DiscoveryMessage(BaseModel):
    topic: str
    payload: DiscoveryPayload
