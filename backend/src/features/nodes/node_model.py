import datetime

from pydantic import BaseModel, Field

from features.esp_easy import Sensor
from features.esp_easy.esp_easy_model import Controller


class NodeHeader(BaseModel):
    unit_no: int
    name: str
    ip: str
    mac: str | None = None
    build: int
    age: int | None = None
    last_seen: datetime.datetime

class Node(NodeHeader):
    controllers: list[Controller] = Field(default_factory=list)
    sensors: list[Sensor] = Field(default_factory=list)
