# Argument Registry

Single source of truth for all labeled thesis elements. Check here before assigning new IDs.

## Definitions
- **D1**: *Saturn service* — any AI endpoint advertised via `_saturn._tcp.local.` mDNS records
- **D2**: *Zero-configuration* — operational without end-user setup of URLs, API keys, or account credentials
- **D3**: *Beacon* — Saturn's announcement architecture that broadcasts metadata, not proxy traffic

## Views (Thesis Claims)
- **V1**: Zero-config AI provisioning is feasible via mDNS/DNS-SD — Ch 1, 3, 4
- **V2**: Network-provisioned AI reduces total configuration effort — Ch 1, 5, 6
- **V3**: Security trade-offs of broadcast AI discovery are documented and addressable — Ch 1, 7

## Arguments
- **A1**: Six cross-platform implementations prove mDNS/DNS-SD AI provisioning works → **V1** — existence proof
- **A2**: Five independent mDNS libraries interoperate on `_saturn._tcp.local.` → **V1** — interop evidence
- **A3**: Consumer path is zero-config across all integration patterns → **V1**, **V2** — comparison
- **A4**: Admin complexity centralizes to one TOML + env var; N users do zero work → **V2** — comparison
- **A5**: Ephemeral keys (10-min expiry, 5-min rotation) sidestep the static key leakage class → **V3** — literature + implementation
- **A6**: Security posture is modular — components range from full ephemeral lifecycle to none → **V3** — existence proof
- **A7**: Saturn runs on a $30 MIPS32 router alongside DHCP/DNS → **V1**, **V2** — existence proof

## Alternative Views
- **AV1**: Zero-trust (BeyondCorp) says trust-the-network is fundamentally wrong → disputes **V3** — literature
- **AV2**: mDNS doesn't scale beyond the LAN → disputes **V1** — protocol limitation
- **AV3**: Manual configuration gives users more control and awareness → disputes **V2** — practice

## Counter-Arguments
- **CA1**: BeyondCorp requires device-level authentication that Saturn omits → supports **AV1** — Ward & Beyer 2014
- **CA2**: mDNS is limited to link-local multicast scope by design → supports **AV2** — RFC 6762

## Barriers
- **B1**: No ecosystem adoption — Saturn is the only implementation of this pattern — active
- **B2**: mDNS is unfamiliar to AI developers; mental model mismatch — active
- **B3**: Existing AI platforms have no incentive to support local discovery — active
