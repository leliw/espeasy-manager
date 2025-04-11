from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerConfig(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    version: str = "0.0.1"
    data_dir: str = "./data/"
    
    mqtt_host: str = "192.168.0.2"
    mqtt_port: int = 1883


class ClientConfig(BaseModel):
    version: str
