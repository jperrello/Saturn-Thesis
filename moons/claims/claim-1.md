# Claim 1: Zero-Config AI Provisioning is Feasible

> Zero-configuration network protocols (mDNS/DNS-SD) can provision AI services without end-user configuration.

## Core argument

Saturn is the existence proof. A working protocol (`_saturn._tcp.local.`), cross-platform implementation, real hardware deployment (GL.iNet router), and client integrations demonstrate that mDNS/DNS-SD can provision AI services without end-user configuration.

## Literature grounding

- **Guttman (2001)** -- Zeroconf was designed to "enable direct communications between two or more computing devices via IP" with no configuration; Saturn applies this to AI
- **Siddiqui et al. (2012)** -- Zeroconf foundations; "allows users to discover services and devices with little end-user intervention"
- **Siljanovski et al. (2014)** -- mDNS/DNS-SD adapts to new domains (printers -> IoT -> AI); "when possible it would be better to adopt preexisting Internet protocols"
- **Kim & Reeves (2020)** -- mDNS literally originated as printer discovery; Saturn extends the lineage to AI

## Evidence

**Server side**: `discovery.py:SaturnAdvertiser` registers services on `_saturn._tcp.local.` using the zeroconf library. One call to `register()` and the service is broadcasting. Running a service is one command: `saturn run ollama`.

**Client side**: `discovery.py:discover()` listens for mDNS responses, parses TXT records, returns `SaturnService` objects. `select_best_service()` sorts by priority and filters by capability. No URLs, no keys, no config files needed by the consumer.

**Protocol interoperability**: Five independent mDNS libraries (Python `zeroconf`, Rust `mdns-sd`, TypeScript `multicast-dns`, Python `dns-sd` subprocess, Python `Zeroconf` in OWUI) all consume `_saturn._tcp.local.`.
