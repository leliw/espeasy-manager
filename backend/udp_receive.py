from pydantic import BaseModel
import socket
import datetime
import requests
import logging
from  ESPEasy.Model import NodeInfo
from ESPEasy.HomeAssistant_MQTT import DiscoveryMessage, send_discovery_message

def udp_receive(UDP_PORT = 8266, esp_nodes = {}):
    UDP_IP = "0.0.0.0"
    log = logging.getLogger("udp_receive")
    log.setLevel(logging.DEBUG)
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
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
            if ip in esp_nodes:
                esp_nodes[ip]["last_seen"] = datetime.datetime.now()
            else:
                esp_nodes[ip] = { "ip": ip, "name": name, "unit_no": unit_no, "last_seen": datetime.datetime.now() }
                node_info = get_node_info(ip, name, unit_no)
                if unit_no == 31:
                    send_node_info(node_info)


def get_node_info(ip, name, unit_no) -> NodeInfo:
    req = requests.get("http://" + ip + "/json")
    return req.json()


def send_node_info(node_info: NodeInfo):
    log = logging.getLogger("send_node_info")
    log.setLevel(logging.DEBUG)
    if node_info["System"]["Unit Number"] == 31:
        node_name = node_info["System"]["Unit Name"]
        for sensor in node_info["Sensors"]:
            if sensor["TaskEnabled"]=="true":
                log.debug(" {%d} : %s - %s", sensor["TaskNumber"], sensor["TaskName"], sensor["Type"])
                msg = create_discovery_message(node_name, sensor["TaskName"], sensor["TaskValues"][0]["Name"], sensor["Type"])
                if msg:
                    send_discovery_message(msg)


def create_discovery_message(node_name: str, task_name: str, value_name: str, type: str) -> DiscoveryMessage:
    unique_id = node_name + "_" + task_name + "_" + value_name
    state_topic = node_name + "/" + task_name + "/" + value_name
    if type == "Environment - DS18b20":
        msg = DiscoveryMessage(name=task_name, device_class="temperature", unique_id=unique_id, state_topic=state_topic)
        msg.unit_of_measurement = "°C"
        return msg
    else:
         return None