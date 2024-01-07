from pydantic import BaseModel
import socket
import logging


class Node(BaseModel):
    ip: str
    name: str
    unit_no: int

def udp_receive(UDP_PORT = 8266, esp_nodes = {}):
    UDP_IP = "0.0.0.0"
    log = logging.getLogger("udp_receive")
    log.setLevel(logging.INFO)
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
            esp_nodes[ip] = { "ip": ip, "name": name, "unit_no": unit_no }
            log.debug("%s -> %s - %d, %d, %d", ip, name, unit_no,
                int.from_bytes(data[13:15]),
                int.from_bytes(data[40:41]))
