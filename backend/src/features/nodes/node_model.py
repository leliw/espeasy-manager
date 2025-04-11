import datetime
from typing import List

from pydantic import BaseModel, Field

from features.esp_easy import Sensor
from features.esp_easy.esp_easy_model import Controller


class NodeHeader(BaseModel):
    unit_no: int
    name: str
    ip: str
    build: int
    age: int
    last_seen: datetime.datetime

class Node(NodeHeader):
    controllers: List[Controller] = Field(default_factory=list)
    sensors: List[Sensor] = Field(default_factory=list)