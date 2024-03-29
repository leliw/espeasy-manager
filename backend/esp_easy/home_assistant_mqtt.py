"""This module provides a class to send Home Assistant MQTT discovery messages."""
from pydantic import BaseModel
import paho.mqtt.client as mqtt
from unidecode import unidecode

# See: https://www.home-assistant.io/integrations/mqtt#mqtt-discovery
class DiscoveryMessage(BaseModel):
    """Home Assistant MQTT discovery message format."""
    name: str
    unique_id: str = None
    icon: str = None
    device_class: str
    state_topic: str
    unit_of_measurement: str = None
    state_on: str = None
    state_off: str = None
    command_topic: str = None
    payload_on: str = None
    payload_off: str = None


mqtt_client = mqtt.Client()
mqtt_client.connect("192.168.0.2", 1883, 60)

def send_discovery_message(entity_type: str, msg: DiscoveryMessage):
    """Send a Home Assistant MQTT discovery message."""
    names = msg.state_topic.split("/")
    msg.unit_of_measurement = "°C"
    discovery_topic = unidecode("homeassistant/" + entity_type + "/" + names[0] + "/" + names[1] + "/config")
    mqtt_client.publish(discovery_topic, msg.model_dump_json(exclude_none=True), qos=0, retain=True) 