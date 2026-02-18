# Beacons

Saturn's announcement architecture. A beacon broadcasts service metadata and credentials via mDNS — it does not proxy API traffic.

## Beacon vs Proxy
- **Beacon**: announces credentials/endpoints via mDNS TXT records. No API traffic flows through the announcer. Deliberate security decision.
- **Proxy client**: client-side convenience. Runs on user's machine, discovers beacons, presents stable localhost endpoint. Architecturally distinct from Saturn itself.
- The proxy pattern exists because most apps won't add native Saturn discovery.

## What beacons do
1. Register service under `_saturn._tcp.local.`
2. Broadcast endpoint URL, API type, priority, features
3. For cloud backends: rotate ephemeral keys on schedule
4. Monitor health and auto-deregister on failure

## What beacons don't do
- No API request proxying (user connects directly to backend)
- No traffic inspection (can't see user's prompts/responses)
- No single point of failure (beacon down = no discovery, but direct connections still work)

## Deployment types (from code)
- **Cloud beacon** (deployment=cloud): distributes ephemeral keys to cloud APIs (OpenRouter, etc.). BeaconAdvertiser hardcodes deployment='cloud'.
- **Local beacon** (deployment=local): announces local services (Ollama, etc.) with health monitoring. Uses SaturnAdvertiser with deployment from TOML config.
- **Network** (deployment=network): config value in orbeacon.toml for services announced on LAN. Functionally similar to local but signifies the service is shared.

## Chapters
- Ch 3.3: concept definition
- Ch 3.5: "beacon not proxy" architecture decision
- Ch 4.4: GL.iNet router as physical beacon
