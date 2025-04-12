# ESPEasy Manger

Manages ESPEasy network in colaboration with Home Assistant

* Listen on UDP 8266 port and doscover all ESP nodes in local network
* Sends MQTT discovery message to Home Assistant

## Development

Run in development environment

```bash
source ./run_dev.sh
```

The docker image is built by GitHub CI/CD.
If you want, you can built it manually.

```bash
docker build -t ghcr.io/leliw/espeasy-manager .
docker push ghcr.io/leliw/espeasy-manager:latest
```

## Production

```bash
docker pull ghcr.io/leliw/espeasy-manager:latest
docker run -d -p 8080:8080 -p 8266:8266/udp --name espeasy-manager ghcr.io/leliw/espeasy-manager 
```
