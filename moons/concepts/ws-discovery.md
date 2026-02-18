# WS-Discovery

Web Services Dynamic Discovery. SOAP-based service discovery protocol.

## What it is
- Multicast SOAP/XML messages for service advertisement
- Used primarily in enterprise environments (printers, scanners via WSD)
- Windows uses it for network printer discovery alongside mDNS

## Why Saturn rejected it
- **SOAP/XML overhead**: verbose protocol for what should be lightweight metadata exchange
- **Enterprise-oriented**: designed for managed networks with IT infrastructure
- **Limited ecosystem**: fewer cross-platform libraries than mDNS
- **No consumer adoption**: end users never interact with WS-Discovery directly

## Chapters
- Ch 2.1: rejected alternative
