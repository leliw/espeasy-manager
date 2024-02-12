# ESPEasy Manger

Manages ESPEasy network in colaboration with Home Assistant

* Listen on UDP 8266 port and doscover all ESP nodes
* Sends MQTT discovery message to Home Assistant

## Run docker image

```bash
docker pull ghcr.io/leliw/espeasy-manager
docker run -p 8088:8000 -p 8266:8266/udp ghcr.io/leliw/espeasy-manager
```
