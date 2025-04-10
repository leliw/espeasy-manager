"""ESP Easy data structure based on JSON format."""
from __future__ import annotations
from typing import List, Optional
import datetime
from pydantic import BaseModel, Field

# ESPEasy data structure based on JSON format

class NodeHeader(BaseModel):
    """Node header information."""
    ip: str
    name: str
    unit_no: int
    last_seen: datetime.datetime

class System(BaseModel):
    """"ESP Easy node system information."""
    Load: float
    Load_LC: int = Field(..., alias='Load LC')
    Build: int
    Git_Build: str = Field(..., alias='Git Build')
    System_Libraries: str = Field(..., alias='System Libraries')
    Plugin_Count: Optional[int] = Field(None, alias='Plugin Count')
    Plugin_Description: Optional[str] = Field(None, alias='Plugin Description')
    Build_Time: Optional[str] = Field(None, alias='Build Time')
    Binary_Filename: Optional[str] = Field(None, alias='Binary Filename')
    Local_Time: str = Field(..., alias='Local Time')
    UTC_time_stored_in_RTC_chip: Optional[str] = Field(None, alias='UTC time stored in RTC chip')
    Time_Source: Optional[str] = Field(None, alias='Time Source')
    Time_Wander: Optional[float] = Field(None, alias='Time Wander')
    Use_NTP: Optional[str] = Field(None, alias='Use NTP')
    Unit_Number: int = Field(..., alias='Unit Number')
    Unit_Name: str = Field(..., alias='Unit Name')
    Uptime: Optional[int] = Field(None, alias='Uptime')
    Uptime__ms_: Optional[int] = Field(None, alias='Uptime (ms)')
    Last_Boot_Cause: str = Field(..., alias='Last Boot Cause')
    Reset_Reason: str = Field(..., alias='Reset Reason')
    CPU_Eco_Mode: str = Field(..., alias='CPU Eco Mode')
    Heap_Max_Free_Block: Optional[int] = Field(None, alias='Heap Max Free Block')
    Heap_Fragmentation: Optional[int] = Field(None, alias='Heap Fragmentation')
    Free_RAM: int = Field(..., alias='Free RAM')
    Free_Stack: Optional[int] = Field(None, alias='Free Stack')
    ESP_Chip_Model: Optional[str] = Field(None, alias='ESP Chip Model')
    Sunrise: Optional[str] = Field(None, alias='Sunrise')
    Sunset: Optional[str] = Field(None, alias='Sunset')
    Timezone_Offset: Optional[int] = Field(None, alias='Timezone Offset')
    Latitude: Optional[float] = Field(None, alias='Latitude')
    Longitude: Optional[float] = Field(None, alias='Longitude')
    Syslog_Log_Level: Optional[str] = Field(None, alias='Syslog Log Level')
    Serial_Log_Level: Optional[str] = Field(None, alias='Serial Log Level')
    Web_Log_Level: Optional[str] = Field(None, alias='Web Log Level')


class WiFi(BaseModel):
    """ESP Easy node WiFi information."""
    Hostname: str
    IP_Config: str = Field(..., alias='IP Config')
    IP_Address: str = Field(..., alias='IP Address')
    IP_Subnet: str = Field(..., alias='IP Subnet')
    Gateway: str
    STA_MAC: str = Field(..., alias='STA MAC')
    DNS_1: str = Field(..., alias='DNS 1')
    DNS_2: str = Field(..., alias='DNS 2')
    SSID: str
    BSSID: str
    Channel: int
    Encryption_Type: Optional[str] = Field(None, alias='Encryption Type')
    Connected_msec: int = Field(..., alias='Connected msec')
    Last_Disconnect_Reason: int = Field(..., alias='Last Disconnect Reason')
    Last_Disconnect_Reason_str: str = Field(..., alias='Last Disconnect Reason str')
    Number_Reconnects: int = Field(..., alias='Number Reconnects')
    Configured_SSID1: Optional[str] = Field(None, alias='Configured SSID1')
    Configured_SSID2: Optional[str] = Field(None, alias='Configured SSID2')
    Force_WiFi_B_G: str = Field(..., alias='Force WiFi B/G')
    Restart_WiFi_Lost_Conn: str = Field(..., alias='Restart WiFi Lost Conn')
    Force_WiFi_No_Sleep: str = Field(..., alias='Force WiFi No Sleep')
    Periodical_send_Gratuitous_ARP: str = Field(
        ..., alias='Periodical send Gratuitous ARP'
    )
    Connection_Failure_Threshold: int = Field(..., alias='Connection Failure Threshold')
    Max_WiFi_TX_Power: Optional[float] = Field(None, alias='Max WiFi TX Power')
    Current_WiFi_TX_Power: Optional[float] = Field(None, alias='Current WiFi TX Power')
    WiFi_Sensitivity_Margin: Optional[int] = Field(None, alias='WiFi Sensitivity Margin')
    Send_With_Max_TX_Power: Optional[str] = Field(None, alias='Send With Max TX Power')
    Extra_WiFi_scan_loops: Optional[int] = Field(None, alias='Extra WiFi scan loops')
    Use_Last_Connected_AP_from_RTC: Optional[str] = Field(None, alias='Use Last Connected AP from RTC'
    )
    RSSI: int


class Node(BaseModel):
    """Node information received by one ESP Easy node from other nodes."""
    nr: int
    name: str
    build: int
    platform: Optional[str] = None
    ip: str
    age: int


class TaskValue(BaseModel):
    """ESP Easy node sensor task value information."""
    ValueNumber: int
    Name: str
    NrDecimals: int
    Value: float


class DataAcquisitionItem(BaseModel):
    """ESP Easy node sensor controller (data acquisition) item information."""
    Controller: int
    IDX: int
    Enabled: str


class Sensor(BaseModel):
    """ESP Easy node sensor information."""
    TaskValues: List[TaskValue]
    DataAcquisition: List[DataAcquisitionItem]
    TaskInterval: int
    Type: str
    TaskName: str
    TaskDeviceNumber: int
    TaskDeviceGPIO1: Optional[int] = None
    TaskDeviceGPIO2: Optional[int] = None
    TaskDeviceGPIO3: Optional[int] = None
    TaskEnabled: str
    TaskNumber: int


class NodeInfo(BaseModel):
    """ESP Easy node information."""
    System: System
    WiFi: WiFi
    nodes: List[Node]
    Sensors: List[Sensor]
    TTL: int
