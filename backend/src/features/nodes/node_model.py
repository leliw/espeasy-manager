import datetime
from typing import List

from pydantic import BaseModel

from features.esp_easy.model import Sensor


class NodeHeader(BaseModel):
    unit_no: int
    name: str
    ip: str
    build: int
    age: int
    last_seen: datetime.datetime

class Node(NodeHeader):
    Sensors: List[Sensor]