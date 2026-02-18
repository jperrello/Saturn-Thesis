# DHCP

Dynamic Host Configuration Protocol. RFC 2131. Saturn's closest network-layer analogy.

## How DHCP works
- Client broadcasts DISCOVER on the LAN
- Server responds with OFFER (IP address, gateway, DNS, lease time)
- Client ACKs, gets network configuration automatically
- Zero configuration for the client — just plug in

## Why Saturn is like DHCP
- Both eliminate manual configuration for end users
- Both use broadcast/multicast for discovery
- Both shift complexity to a single administrator
- "Join the network, get the service" model

## Why not DHCP for service discovery
- **Temporal**: DHCP provides one-time config at join; Saturn services appear/disappear dynamically
- **Multiplicity**: DHCP gives one IP; Saturn discovers N services with different capabilities
- **Privilege**: DHCP requires root/system access; Saturn runs in userspace
- **Metadata**: DHCP carries minimal info; Saturn needs model lists, features, API types

## Saturn and DHCP are complementary
DHCP configures the network. Saturn configures AI services on that network. They operate at different layers but share the same philosophy: infrastructure should just work.

## Chapters
- Ch 2.4: comparison
- Ch 3.1: design goals rationale
