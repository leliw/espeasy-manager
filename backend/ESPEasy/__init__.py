from pydantic import BaseModel
import socket
import datetime
import requests
import logging
from  ESPEasy.Model import NodeHeader, NodeInfo
from ESPEasy.HomeAssistant_MQTT import DiscoveryMessage, send_discovery_message

# Port to listen for UDP packets 8266 is the default port for ESPEasy or 65500 (old one)
__udp_port = 8266
__esp_nodes = {}

def set_udp_port(port: int):
    __udp_port = port

def get_nodes():
    return [v for (_, v) in __esp_nodes.items()]

def save_node(node_info: NodeInfo):
    json = node_info.model_dump_json(exclude_none=True)
    file = "data/" + node_info.System.Unit_Name + ".json"
    with open(file, 'tw', encoding="UTF-8") as outfile:
        outfile.write(json)

def udp_receive():
    UDP_IP = "0.0.0.0"
    log = logging.getLogger("udp_receive")
    log.setLevel(logging.DEBUG)
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, __udp_port))
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
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
                node_info = get_node_info(ip, name, unit_no)
                save_node(node_info)
                if unit_no == 31 or unit_no == 33:
                    send_node_info(node_info)


def get_node_info(ip, name, unit_no) -> NodeInfo:
    req = requests.get("http://" + ip + "/json")
    return NodeInfo.model_validate(req.json())


def send_node_info(node_info: NodeInfo):
    log = logging.getLogger("send_node_info")
    log.setLevel(logging.DEBUG)
    node_name = node_info.System.Unit_Name
    for sensor in node_info.Sensors:
        if sensor.TaskEnabled=="true":
            log.debug(" {%d} : %s - %s", sensor.TaskNumber, sensor.TaskName, sensor.Type)
            type, msg = create_discovery_message(node_name, sensor.TaskName, sensor.TaskNumber, sensor.TaskValues[0].Name, sensor.Type)
            if msg:
                log.debug("Sending discovery message: %s", msg.model_dump_json(exclude_none=True))
                send_discovery_message(type, msg)


def create_discovery_message(node_name: str, task_name: str, task_number: int, value_name: str, type: str) -> (str, DiscoveryMessage):
    unique_id = node_name + "_" + task_name + "_" + value_name
    state_topic = node_name + "/" + task_name + "/" + value_name
    name = node_name.replace("_", " ") + " - " + task_name.replace("_", " ")
    if type == "Environment - DS18b20":
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