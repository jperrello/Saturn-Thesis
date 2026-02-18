# mDNS (Multicast DNS)

Link-local name resolution without infrastructure. RFC 6762.

## How it works
- Queries sent via multicast to 224.0.0.251:5353 (IPv4) or ff02::fb (IPv6)
- Any device on the local network can respond to queries for names it owns
- Names use `.local` TLD (e.g., `myserver.local`)
- No DNS server required — devices answer for themselves

## Saturn's use
Saturn registers service names under `_saturn._tcp.local.` so any device on the LAN can discover AI endpoints without configuration. This is the foundation of Claim 1.

## Key properties
- Zero-configuration: no server, no setup, no accounts
- Link-local scope: only works on the same network segment
- Cross-platform: Bonjour (macOS/Windows), Avahi (Linux)
- Same protocol used for printer discovery, AirPlay, Chromecast

## Limitations
- AP isolation blocks multicast (eduroam, UCSC-guest — confirmed Jan 2026 experiment)
- Passive eavesdropping: anyone on network sees all announcements (Kaiser & Waldvogel 2014a)
- 59% of device names contain real user names (Könings 2013)

## Papers
- guttman-2001, siddiqui-2012, siljanovski-2014, kim-reeves-2020
- kaiser-waldvogel-2014a (privacy), kaiser-waldvogel-2014b (privacy-preserving)

## Chapters
- Ch 2.2: deep dive
- Ch 3.4: protocol specification
- Ch 7.1: threat models
