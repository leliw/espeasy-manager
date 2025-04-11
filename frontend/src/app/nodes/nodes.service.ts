import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';


export interface NodeHeader {
  unit_no: number;
  name: string;
  ip: string;
  build: number;
  age: number;
  last_seen: string;
}
export interface Controller {
  controller_no: number;
  enabled: boolean;
  protocol: string;
  host: string;
  port: number;
}

export interface Node {
  System: System;
  WiFi: WiFi;
  nodes: NodeInfo[];
  controllers: Controller[];
  sensors: Sensor[];
  TTL: number;
}

export interface System {
  Load: number
  "Load LC": number
  Build: number
  "Git Build": string
  "System Libraries": string
  "Plugin Count": number
  "Plugin Description": string
  "Build Time": string
  "Binary Filename": string
  "Local Time": string
  "UTC time stored in RTC chip": string
  "Time Source": string
  "Time Wander": number
  "Use NTP": string
  "Unit Number": number
  "Unit Name": string
  Uptime: number
  "Uptime (ms)": number
  "Last Boot Cause": string
  "Reset Reason": string
  "CPU Eco Mode": string
  "Heap Max Free Block": number
  "Heap Fragmentation": any
  "Free RAM": number
  "Free Stack": number
  "ESP Chip Model": string
  Sunrise: string
  Sunset: string
  "Timezone Offset": number
  Latitude: number
  Longitude: number
  "Syslog Log Level": string
  "Serial Log Level": string
  "Web Log Level": string
}

export interface WiFi {
  Hostname: string
  "IP Config": string
  "IP Address": string
  "IP Subnet": string
  Gateway: string
  "STA MAC": string
  "DNS 1": string
  "DNS 2": string
  SSID: string
  BSSID: string
  Channel: number
  "Encryption Type": string
  "Connected msec": number
  "Last Disconnect Reason": number
  "Last Disconnect Reason str": string
  "Number Reconnects": number
  "Configured SSID1": string
  "Configured SSID2": string
  "Force WiFi B/G": string
  "Restart WiFi Lost Conn": string
  "Force WiFi No Sleep": string
  "Periodical send Gratuitous ARP": string
  "Connection Failure Threshold": number
  "Max WiFi TX Power": number
  "Current WiFi TX Power": number
  "WiFi Sensitivity Margin": number
  "Send With Max TX Power": string
  "Extra WiFi scan loops": number
  "Use Last Connected AP from RTC": string
  RSSI: number
}

export interface NodeInfo {
  nr: number
  name: string
  build: number
  platform: string
  ip: string
  age: number
}

export interface Sensor {
  TaskValues: TaskValue[]
  DataAcquisition: DataAcquisition[]
  TaskInterval: number
  Type: string
  TaskName: string
  TaskDeviceNumber: number
  TaskDeviceGPIO1?: number
  TaskDeviceGPIO2: any
  TaskDeviceGPIO3: any
  TaskEnabled: string
  TaskNumber: number
}

export interface TaskValue {
  ValueNumber: number
  Name: string
  NrDecimals: number
  Value: number
}

export interface DataAcquisition {
  Controller: number
  IDX: number
  Enabled: string
}


@Injectable({
  providedIn: 'root'
})
export class NodesService {

  constructor(private http: HttpClient) { }

  getNodes() {
    return this.http.get<NodeHeader[]>('/api/nodes');
  }

  getNode(ip: string): Observable<Node> {
    return this.http.get<Node>(`/api/nodes/${ip}`);
  }

  refreshNodeInformation(ip: string): Observable<Node> {
    return this.http.post<Node>(`/api/nodes/${ip}/refresh`, {});
  }
}
