"""ESP Easy data structure based on JSON format."""

from __future__ import annotations

from pydantic import BaseModel, Field

# ESPEasy data structure based on JSON format


class System(BaseModel):
    """ESP Easy node system information."""

    Load: float | None = None
    Load_LC: int | None = Field(None, alias="Load LC")
    Build: int
    Git_Build: str = Field(..., alias="Git Build")
    System_Libraries: str = Field(..., alias="System Libraries")
    Plugin_Count: int | None = Field(None, alias="Plugin Count")
    Plugin_Description: str | list[str] | None = Field(None, alias="Plugin Description")
    Build_Time: str | None = Field(None, alias="Build Time")
    Binary_Filename: str | None = Field(None, alias="Binary Filename")
    Local_Time: str = Field(..., alias="Local Time")
    UTC_time_stored_in_RTC_chip: str | None = Field(None, alias="UTC time stored in RTC chip")
    Time_Source: str | None = Field(None, alias="Time Source")
    Time_Wander: float | None = Field(None, alias="Time Wander")
    Use_NTP: str | None = Field(None, alias="Use NTP")
    Unit_Number: int = Field(..., alias="Unit Number")
    Unit_Name: str = Field(..., alias="Unit Name")
    Uptime: int | None = Field(None, alias="Uptime")
    Uptime__ms_: int | None = Field(None, alias="Uptime (ms)")
    Last_Boot_Cause: str = Field(..., alias="Last Boot Cause")
    Reset_Reason: str = Field(..., alias="Reset Reason")
    CPU_Eco_Mode: str = Field(..., alias="CPU Eco Mode")
    Heap_Max_Free_Block: int | None = Field(None, alias="Heap Max Free Block")
    Heap_Fragmentation: int | None = Field(None, alias="Heap Fragmentation")
    Free_RAM: int = Field(..., alias="Free RAM")
    Free_Stack: int | None = Field(None, alias="Free Stack")
    ESP_Chip_Model: str | None = Field(None, alias="ESP Chip Model")
    Sunrise: str | None = Field(None, alias="Sunrise")
    Sunset: str | None = Field(None, alias="Sunset")
    Timezone_Offset: int | None = Field(None, alias="Timezone Offset")
    Latitude: float | None = Field(None, alias="Latitude")
    Longitude: float | None = Field(None, alias="Longitude")
    Syslog_Log_Level: str | None = Field(None, alias="Syslog Log Level")
    Serial_Log_Level: str | None = Field(None, alias="Serial Log Level")
    Web_Log_Level: str | None = Field(None, alias="Web Log Level")


class WiFi(BaseModel):
    """ESP Easy node WiFi information."""

    Hostname: str
    IP_Config: str = Field(..., alias="IP Config")
    IP_Address: str = Field(..., alias="IP Address")
    IP_Subnet: str = Field(..., alias="IP Subnet")
    Gateway: str
    STA_MAC: str = Field(..., alias="STA MAC")
    DNS_1: str = Field(..., alias="DNS 1")
    DNS_2: str = Field(..., alias="DNS 2")
    SSID: str
    BSSID: str
    Channel: int
    Encryption_Type: str | None = Field(None, alias="Encryption Type")
    Connected_msec: int = Field(..., alias="Connected msec")
    Last_Disconnect_Reason: int = Field(..., alias="Last Disconnect Reason")
    Last_Disconnect_Reason_str: str = Field(..., alias="Last Disconnect Reason str")
    Number_Reconnects: int = Field(..., alias="Number Reconnects")
    Configured_SSID1: str | None = Field(None, alias="Configured SSID1")
    Configured_SSID2: str | None = Field(None, alias="Configured SSID2")
    Force_WiFi_B_G: str = Field(..., alias="Force WiFi B/G")
    Restart_WiFi_Lost_Conn: str = Field(..., alias="Restart WiFi Lost Conn")
    Force_WiFi_No_Sleep: str = Field(..., alias="Force WiFi No Sleep")
    Periodical_send_Gratuitous_ARP: str = Field(..., alias="Periodical send Gratuitous ARP")
    Connection_Failure_Threshold: int = Field(..., alias="Connection Failure Threshold")
    Max_WiFi_TX_Power: float | None = Field(None, alias="Max WiFi TX Power")
    Current_WiFi_TX_Power: float | None = Field(None, alias="Current WiFi TX Power")
    WiFi_Sensitivity_Margin: int | None = Field(None, alias="WiFi Sensitivity Margin")
    Send_With_Max_TX_Power: str | None = Field(None, alias="Send With Max TX Power")
    Extra_WiFi_scan_loops: int | None = Field(None, alias="Extra WiFi scan loops")
    Use_Last_Connected_AP_from_RTC: str | None = Field(None, alias="Use Last Connected AP from RTC")
    RSSI: int


class Node(BaseModel):
    """Node information received by one ESP Easy node from other nodes."""

    nr: int
    name: str
    build: int
    platform: str | None = None
    ip: str
    age: int


class TaskValue(BaseModel):
    """ESP Easy node sensor task value information."""

    ValueNumber: int
    Name: str
    NrDecimals: int
    Value: float | None = None


class DataAcquisitionItem(BaseModel):
    """ESP Easy node sensor controller (data acquisition) item information."""

    Controller: int
    IDX: int
    Enabled: str


class Sensor(BaseModel):
    """ESP Easy node sensor information."""

    TaskValues: list[TaskValue]
    DataAcquisition: list[DataAcquisitionItem]
    TaskInterval: int
    Type: str
    TaskName: str
    TaskDeviceNumber: int
    TaskDeviceGPIO1: int | None = None
    TaskDeviceGPIO2: int | None = None
    TaskDeviceGPIO3: int | None = None
    TaskEnabled: str
    TaskNumber: int


class NodeInfo(BaseModel):
    """ESP Easy node information."""

    System: System
    WiFi: WiFi
    nodes: list[Node]
    Sensors: list[Sensor]
    TTL: int


class Controller(BaseModel):
    """ESP Easy node controller information."""

    controller_no: int
    enabled: bool
    protocol: str | None = None
    host: str | None = None
    port: int | None = None
