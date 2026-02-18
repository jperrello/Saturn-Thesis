# UPnP / SSDP

Universal Plug and Play with Simple Service Discovery Protocol. Rejected alternative for Saturn.

## What it is
- SSDP: multicast discovery (like mDNS but different protocol)
- UPnP: full device control framework on top of SSDP
- SOAP/XML messaging for device interaction
- Used by routers (port forwarding), media servers, smart home devices

## Why Saturn rejected it
- **Too much scope**: UPnP includes device control, not just discovery. Saturn only needs discovery.
- **Security history**: UPnP has well-documented vulnerabilities (remote code execution, unauthorized port forwarding)
- **Protocol overhead**: SOAP/XML is heavyweight compared to DNS record types
- **Declining adoption**: modern ecosystems prefer mDNS/DNS-SD (Apple, Google, Microsoft)
- **No metadata flexibility**: designed for device profiles, not arbitrary service metadata

## Chapters
- Ch 2.1: rejected alternative
