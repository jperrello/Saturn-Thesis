# DNS-SD (DNS-based Service Discovery)

Service advertisement and discovery using standard DNS record types. RFC 6763.

## How it works
- PTR records: enumerate available service instances for a type (e.g., `_saturn._tcp.local.`)
- SRV records: provide hostname + port for each instance
- TXT records: carry key-value metadata (max 255 bytes per string)
- Discovery flow: PTR → SRV/TXT → connect

## Saturn's use
Saturn uses DNS-SD to advertise AI service metadata:
- Service type: `_saturn._tcp.local.`
- TXT schema: version, deployment, api_type, api_base, priority, ephemeral_key, rotation_interval, features
- 4-step process: PTR query → SRV/TXT response → sort by priority → select endpoint

## Key properties
- Runs over mDNS (link-local) or unicast DNS (wide-area)
- Metadata-rich: TXT records carry configuration details
- Browsable: clients can enumerate all services of a type
- Standard: same mechanism as AirPrint, AirPlay, Spotify Connect

## Limitations
- TXT record 255-byte string limit constrains metadata size
- Ephemeral keys must fit within this limit (~240 chars usable)
- No built-in authentication or encryption

## Papers
- guttman-2001, siddiqui-2012, siljanovski-2014

## Chapters
- Ch 2.2: record types explained
- Ch 3.4: Saturn's TXT schema table
