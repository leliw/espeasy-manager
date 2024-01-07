from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field
import datetime

# ESPEasy data structure based on JSON format

class NodeHeader(BaseModel):
    ip: str
    name: str
    unit_no: int
    last_seen: datetime.datetime

class System(BaseModel):
    Load: float
    Load_LC: int = Field(..., alias='Load LC')
    Build: int
    Git_Build: str = Field(..., alias='Git Build')
    System_Libraries: str = Field(..., alias='System Libraries')
    Plugin_Count: int = Field(..., alias='Plugin Count')
    Plugin_Description: str = Field(..., alias='Plugin Description')
    Build_Time: str = Field(..., alias='Build Time')
    Binary_Filename: str = Field(..., alias='Binary Filename')
    Local_Time: str = Field(..., alias='Local Time')
    UTC_time_stored_in_RTC_chip: str = Field(..., alias='UTC time stored in RTC chip')
    Time_Source: str = Field(..., alias='Time Source')
    Time_Wander: float = Field(..., alias='Time Wander')
    Use_NTP: str = Field(..., alias='Use NTP')
    Unit_Number: int = Field(..., alias='Unit Number')
    Unit_Name: str = Field(..., alias='Unit Name')
    Uptime: int
    Uptime__ms_: int = Field(..., alias='Uptime (ms)')
    Last_Boot_Cause: str = Field(..., alias='Last Boot Cause')
    Reset_Reason: str = Field(..., alias='Reset Reason')
    CPU_Eco_Mode: str = Field(..., alias='CPU Eco Mode')
    Heap_Max_Free_Block: int = Field(..., alias='Heap Max Free Block')
    Heap_Fragmentation: int = Field(..., alias='Heap Fragmentation')
    Free_RAM: int = Field(..., alias='Free RAM')
    Free_Stack: int = Field(..., alias='Free Stack')
    ESP_Chip_Model: str = Field(..., alias='ESP Chip Model')
    Sunrise: str
    Sunset: str
    Timezone_Offset: int = Field(..., alias='Timezone Offset')
    Latitude: float
    Longitude: float
    Syslog_Log_Level: str = Field(..., alias='Syslog Log Level')
    Serial_Log_Level: str = Field(..., alias='Serial Log Level')
    Web_Log_Level: str = Field(..., alias='Web Log Level')


class WiFi(BaseModel):
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
    Encryption_Type: str = Field(..., alias='Encryption Type')
    Connected_msec: int = Field(..., alias='Connected msec')
    Last_Disconnect_Reason: int = Field(..., alias='Last Disconnect Reason')
    Last_Disconnect_Reason_str: str = Field(..., alias='Last Disconnect Reason str')
    Number_Reconnects: int = Field(..., alias='Number Reconnects')
    Configured_SSID1: str = Field(..., alias='Configured SSID1')
    Configured_SSID2: str = Field(..., alias='Configured SSID2')
    Force_WiFi_B_G: str = Field(..., alias='Force WiFi B/G')
    Restart_WiFi_Lost_Conn: str = Field(..., alias='Restart WiFi Lost Conn')
    Force_WiFi_No_Sleep: str = Field(..., alias='Force WiFi No Sleep')
    Periodical_send_Gratuitous_ARP: str = Field(
        ..., alias='Periodical send Gratuitous ARP'
    )
    Connection_Failure_Threshold: int = Field(..., alias='Connection Failure Threshold')
    Max_WiFi_TX_Power: float = Field(..., alias='Max WiFi TX Power')
    Current_WiFi_TX_Power: float = Field(..., alias='Current WiFi TX Power')
    WiFi_Sensitivity_Margin: int = Field(..., alias='WiFi Sensitivity Margin')
    Send_With_Max_TX_Power: str = Field(..., alias='Send With Max TX Power')
    Extra_WiFi_scan_loops: int = Field(..., alias='Extra WiFi scan loops')
    Use_Last_Connected_AP_from_RTC: str = Field(
        ..., alias='Use Last Connected AP from RTC'
    )
    RSSI: int


class Node(BaseModel):
    nr: int
    name: str
    build: int
    platform: str
    ip: str
    age: int


class TaskValue(BaseModel):
    ValueNumber: int
    Name: str
    NrDecimals: int
    Value: int


class DataAcquisitionItem(BaseModel):
    Controller: int
    IDX: int
    Enabled: str


class Sensor(BaseModel):
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
    System: System
    WiFi: WiFi
    nodes: List[Node]
    Sensors: List[Sensor]
    TTL: int
