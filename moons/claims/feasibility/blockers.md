# Feasibility Blockers

What prevents Saturn from working. Categorized by severity.

## Where Saturn works reliably

- **Home WiFi**: Consumer routers forward multicast by default. The GL.iNet router deployment was tested in this environment.
- **Small office LANs**: Flat network topology, no client isolation. Multicast works out of the box.
- **Ad-hoc / hotspot networks**: Device-created networks (phone hotspot, laptop sharing) have no AP isolation.
- **Lab / classroom networks**: Dedicated subnets without enterprise-grade isolation. The "teacher sets up Saturn for a class" scenario works here.
- **Wired Ethernet segments**: Switches forward multicast within a VLAN. Most reliable environment for Saturn.

The common thread: networks where the admin controls the infrastructure and multicast isn't filtered.

## Hard blockers (Saturn cannot work at all)

### AP isolation / client isolation
The biggest blocker. Enterprise and institutional WiFi networks block multicast traffic between clients. mDNS queries go to `224.0.0.251:5353` — if the AP doesn't forward multicast between clients, discovery fails silently.

**Confirmed**: Jan 2026 experiment — eduroam and UCSC-guest both block multicast. Discovery fails completely on these networks.

**Impact**: Directly undermines the campus deployment scenario that motivates the thesis. The environments where Saturn would help most (universities, libraries) are the environments most likely to run enterprise WiFi with client isolation.

**Not solvable within Saturn's protocol**: This is a network infrastructure decision made by campus IT. Saturn can't work around it without the network administrator enabling multicast forwarding or deploying Saturn on a separate network segment.

### VLANs without multicast bridging
If the admin's Saturn beacon is on VLAN 10 and users are on VLAN 20, mDNS doesn't cross the boundary. mDNS is link-local by design (RFC 6762).

**Impact**: Common in institutional deployments where servers and clients are on separate VLANs.

### Firewall rules blocking UDP 5353
Some corporate firewalls block mDNS outright.

**Impact**: Less common than AP isolation but equally fatal. Users see no Saturn services.

## Soft blockers (Saturn works but with degraded experience)

### No service identity verification
Any device on the network can broadcast `_saturn._tcp.local.`. Health checks verify HTTP 200 on `/v1/health` but don't validate identity or authenticity. A rogue service on coffee shop WiFi appears alongside legitimate ones.

**Threat model**: Kaiser & Waldvogel (2014a) — "every machine in the same network will automatically receive all the announcement traffic."

**Impact**: In open/shared networks, users could connect to malicious services. In trusted networks (home, managed office), risk is lower.

### Plaintext TXT records
Ephemeral keys are broadcast in cleartext mDNS TXT records. Anyone on the same network segment can passively read them. HTTP traffic to discovered services is also unencrypted.

**Mitigation**: 10-min key expiry limits window. Spending limits cap financial exposure. Kaiser & Waldvogel (2014b) showed privacy-preserving mDNS-SD is feasible — cited as future work.

### Router RAM-only deployment
On the GL.iNet router, the binary runs from `/tmp/saturn` because flash is too small (~800KB free). Lost on reboot.

**Mitigation**: Init script auto-downloads from GitHub releases on boot (`ensure_binary()` in `saturn.init`). Requires internet connectivity at boot.

**Impact**: Institutional deployments need routers with persistent storage or reliable internet for auto-download.

## Non-blockers (commonly confused)

### ARP
ARP operates at Layer 2 for IP-to-MAC resolution. It does not interfere with mDNS. ARP spoofing is a general network attack vector (man-in-the-middle), but it's not Saturn-specific — it affects all LAN traffic equally. Saturn's actual network-layer blocker is multicast filtering, not ARP.

## Architectural limits (by design, not bugs)

### Single network segment
mDNS is link-local. Saturn doesn't work across subnets, across the internet, or between different physical networks. This is by design — the security model depends on the network trust boundary. But it means Saturn can't serve a distributed campus with multiple L3 segments without running beacons on each segment.

### Discovery latency
mDNS discovery takes 1-5 seconds depending on network conditions and settle time. Not instant. Applications that need immediate model access on first launch must handle the discovery delay (ai-sdk-provider does this with background query + registry caching).
