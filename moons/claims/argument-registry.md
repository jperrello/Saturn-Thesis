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
- **A8**: TXT record schema carries all connection parameters (endpoint, auth, API type, priority) without out-of-band config → **V1** — protocol analysis
- **A9**: Three API backends (Ollama/none, DeepInfra/JWT, OpenRouter/ephemeral) operate through the same TXT schema → **V1** — implementation evidence
- **A10**: Seven consumers across 3 languages and 5 mDNS libraries interoperate on `_saturn._tcp.local.` with no bridging layer → **V1** — interop census (refines A1, A2)
- **A11**: Cognitive walkthrough (Wharton 1994) across three personas shows 53% total step reduction (38→18) → **V2** — measurement
- **A12**: App developer burden drops 79% (19→4 steps) because Saturn eliminates the entire billing/payment stack → **V2** — measurement
- **A13**: End user payment friction drops 100% (7→0 additional steps); Saturn removes the paywall entirely → **V2** — measurement
- **A14**: Scaling formula: Traditional = 12+19N+7M, Saturn = 14+4N+0M; at N=10, M=100, reduction is 94% → **V2** — analytical extrapolation
- **A15**: Syed 2025 documents AIaaS status quo (API keys, accounts, platform lock-in) as the baseline Saturn displaces → **V2** — literature
- **A16**: Meli 2019 shows static API key management fails at scale (100k+ repos with leaked secrets); Saturn eliminates per-user key handling → **V2**, **V3** — literature
- **A17**: AP isolation (enterprise WiFi blocking multicast) is Saturn's hardest deployment constraint; confirmed on eduroam/UCSC-guest. Saturn works on target networks (home, office, lab) but fails on institutional networks with client isolation → **V3** — honest limitation (see **B5**)
- **A18**: Nielsen heuristic evaluation identifies 4 usability strengths (H1 visibility, H5 error prevention, H6 recognition > recall, H7 flexibility), 3 trade-offs (H2 sysadmin terminology, H3 role-dependent control, H4 schema drift), and 3 limitations (H8 schema inconsistency, H9 weak error recovery, H10 docs gaps) → **V1**, **V2**, **V3** — analytical evaluation

## Alternative Views
- **AV1**: Zero-trust (BeyondCorp) says trust-the-network is fundamentally wrong → disputes **V3** — literature
- **AV2**: mDNS doesn't scale beyond the LAN → disputes **V1** — protocol limitation
- **AV3**: Manual configuration gives users more control and awareness → disputes **V2** — practice
- **AV4**: Saturn sysadmin does *more* work than traditional key distribution → disputes **V2** — walkthrough data

## Counter-Arguments
- **CA1**: BeyondCorp requires device-level authentication that Saturn omits → supports **AV1** — Ward & Beyer 2014
- **CA2**: mDNS is limited to link-local multicast scope by design → supports **AV2** — RFC 6762
- **CA3**: Sysadmin step count is 14–26 vs traditional 12 (+17% to +117%) → supports **AV4** — walkthrough data. Rebutted by **A12**, **A13**, **A14**: the sysadmin increase is amortized across N developers and M users

## Barriers
- **B1**: No ecosystem adoption — Saturn is the only implementation of this pattern — active
- **B2**: mDNS is unfamiliar to AI developers; mental model mismatch — active
- **B3**: Existing AI platforms have no incentive to support local discovery — active
- **B4**: Cognitive walkthroughs are single-author analytical step counts, not empirical user timing — active (acknowledged as limitation in C2)
- **B5**: AP isolation on enterprise/institutional WiFi blocks multicast between clients; confirmed on eduroam and UCSC-guest (Jan 2026). Directly undermines campus deployment scenario. Not solvable within Saturn protocol — active (documented in C3, Section 6.4)
- **B6**: TXT record schema drift — `auth` field TypeScript-only, `capabilities`/`cost`/`context` missing from Rust implementation; core 4 fields consistent — active (H4/H8 finding, documented in heuristic evaluation)
