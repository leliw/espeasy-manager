from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    version: str = "0.0.1"
    data_dir: str = "./data/"
    
    mqtt_host: str = "192.168.0.2"
    mqtt_port: int = 1883
    mqtt_user: str | None = None
    mqtt_pass: str | None = None
