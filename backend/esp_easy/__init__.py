"""ESPEasy - A Python library to communicate with ESPEasy devices"""
import socket
import datetime
import logging
import os
import requests
from pydantic import BaseModel
from esp_easy.Model import NodeHeader, NodeInfo
from esp_easy.home_assistant_mqtt import DiscoveryMessage, send_discovery_message

# Port to listen for UDP packets 8266 is the default port for ESPEasy or 65500 (old one)
__udp_port = 8266
#__udp_port = 65500
__esp_nodes = {}

def set_udp_port(port: int):
    """Set the port to listen for UDP packets. Default is 8266."""
    __udp_port = port

def get_nodes():
    """Returns a list of all nodes"""
    return [v for (_, v) in __esp_nodes.items()]

def get_node(ip: str) -> NodeInfo:
    """Returns a node by ip"""
    if ip in __esp_nodes:
        node = __esp_nodes[ip]
        return get_node_info(node["ip"])
    else:
        return None

def save_node(node_info: NodeInfo):
    """Save the node info to a file."""
    json = node_info.model_dump_json(exclude_none=True)
    os.makedirs("data", exist_ok=True)
    file = "data/" + node_info.System.Unit_Name + ".json"
    with open(file, 'tw', encoding="UTF-8") as outfile:
        outfile.write(json)

def udp_receive():
    """Listen for UDP packets from ESPEasy devices."""
    log = logging.getLogger("udp_receive")
    log.setLevel(logging.DEBUG)
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind(("0.0.0.0", __udp_port))
    while True:
        data, _ = sock.recvfrom(1024) # buffer size is 1024 bytes
        # print("received message: %s" % data)
        # print(data[0:2])
        # print(data[2:8])
        if data[0:2] == b'\xff\x01':
            ip = str(int.from_bytes(data[8:9])) + "." + str(int.from_bytes(data[9:10])) + "." + str(int.from_bytes(data[10:11])) + "." + str(int.from_bytes(data[11:12]))
            name = data[15:40].split(b'\00')[0].decode("ascii", errors='ignore')
            unit_no = int.from_bytes(data[12:13])
            log.debug("%s -> %s - %d, %d, %d", ip, name, unit_no, int.from_bytes(data[13:15]), int.from_bytes(data[40:41]))
            if ip in __esp_nodes:
                __esp_nodes[ip]["last_seen"] = datetime.datetime.now()
            else:
                __esp_nodes[ip] = { "ip": ip, "name": name, "unit_no": unit_no, "last_seen": datetime.datetime.now() }
                node_info = get_node_info(ip)
                save_node(node_info)
                if unit_no == 31 or unit_no == 33:
                    send_node_info(node_info)


def get_node_info(ip) -> NodeInfo:
    """Get the node info from the device."""
    req = requests.get("http://" + ip + "/json", timeout=5)
    return NodeInfo.model_validate(req.json())


def send_node_info(node_info: NodeInfo):
    """Send Home Assistant MQTT discovery messages for the node sensors."""
    log = logging.getLogger("send_node_info")
    log.setLevel(logging.DEBUG)
    node_name = node_info.System.Unit_Name
    for sensor in node_info.Sensors:
        if sensor.TaskEnabled=="true":
            log.debug(" {%d} : %s - %s", sensor.TaskNumber, sensor.TaskName, sensor.Type)
            entity_type, msg = create_discovery_message(node_name, sensor.TaskName, sensor.TaskNumber, sensor.TaskValues[0].Name, sensor.Type)
            if msg:
                log.debug("Sending discovery message: %s", msg.model_dump_json(exclude_none=True))
                send_discovery_message(entity_type, msg)


def create_discovery_message(node_name: str, task_name: str, task_number: int, value_name: str, device_type: str) -> tuple[str, DiscoveryMessage]:
    """Create a Home Assistant MQTT discovery message."""
    unique_id = node_name + "_" + task_name + "_" + value_name
    state_topic = node_name + "/" + task_name + "/" + value_name
    name = node_name.replace("_", " ") + " - " + task_name.replace("_", " ")
    if device_type == "Environment - DS18b20":
        msg = DiscoveryMessage(name=name, device_class="temperature", unique_id=unique_id, state_topic=state_topic)
        msg.unit_of_measurement = "°C"
        return ('sensor', msg)
    elif value_name == "State":
        msg = DiscoveryMessage(name=name, device_class="switch", unique_id=unique_id, state_topic=state_topic)
        msg.icon = "mdi:light-switch"
        msg.unit_of_measurement = None
        msg.command_topic = node_name + "/cmd"
        msg.payload_on = "TaskValueSet," + str(task_number) + ",1,1"
        msg.payload_off = "TaskValueSet," + str(task_number) + ",1,0"
        msg.state_on = "1"
        msg.state_off = "0"
        return ('switch', msg)
    else:
        return (None, None)
