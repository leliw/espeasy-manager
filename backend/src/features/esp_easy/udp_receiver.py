"""This module listens for UDP packets from ESPEasy devices."""
import logging
import socket
from abc import ABC, abstractmethod


class NodeReceiver(ABC):
    """This class receives nodes from the UdpReceiver class."""
    @abstractmethod
    def received_node(self, ip: str, name: str, unit_no: int):
        """Add a node to the list of nodes"""


class UdpReceiver:
    """This class listens for UDP packets from ESPEasy devices."""
    # Port to listen for UDP packets 8266 is the default port for ESPEasy or 65500 (old one)
    def __init__(self, node_receiver: NodeReceiver, port: int = 8266):
        self._log = logging.getLogger(__name__)
        self._udp_port = port
        self._node_manager = node_receiver

    def receive_forever(self):
        """Listen for UDP packets from ESPEasy devices."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", self._udp_port))
        while True:
            data, _ = sock.recvfrom(1024) # buffer size is 1024 bytes
            if data[0:2] == b'\xff\x01':
                ip = (str(int.from_bytes(data[8:9])) + "."
                      + str(int.from_bytes(data[9:10])) + "."
                      + str(int.from_bytes(data[10:11])) + "."
                      + str(int.from_bytes(data[11:12])))
                name = data[15:40].split(b'\00')[0].decode("ascii", errors='ignore')
                unit_no = int.from_bytes(data[12:13])
                self._log.debug("%s -> %s - %d, %d, %d",
                                ip, name, unit_no,
                                int.from_bytes(data[13:15]), int.from_bytes(data[40:41]))
                self._node_manager.received_node(ip, name, unit_no)
