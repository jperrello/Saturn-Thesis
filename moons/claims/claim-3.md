# Claim 3: Security Trade-offs are Known and Addressable

> The security and privacy trade-offs of broadcast-based AI discovery are documented in existing literature and can be mitigated without destroying the zero-config property.

## Core argument

Saturn trades enterprise-grade verification for zero-config access. This is a deliberate design choice for the target environment (campus WiFi, coffee shops, homes), not an oversight. The threat model is well-documented in existing mDNS literature, and mitigations exist.

## Literature grounding

- **Kaiser & Waldvogel (2014a)** -- Passive eavesdropping threat model for mDNS-SD; "every machine in the same network will automatically receive all the announcement traffic"
- **Kaiser & Waldvogel (2014b)** -- Privacy-preserving mDNS-SD is feasible; privacy sockets + pairing maintain backward compatibility
- **Konings et al. (2013)** -- Empirical measurement: 59% of mDNS device names contain real names; 32% of users unaware
- **Ward & Beyer (2014)** -- BeyondCorp zero-trust as the opposing philosophy; Saturn deliberately diverges for consumer/educational access
- **Meli et al. (2019)** -- Static API key model is fundamentally broken: 81% of leaked secrets never removed, best scanning tools only 25% effective, "all mitigations act too late"; Saturn's ephemeral keys (10-min expiry) sidestep the entire leakage class
- **Qazi (2023)** -- Organizations can't track their own API keys; users default to trusting network-level security -- aligns with Saturn's model

## Evidence

**Methodology**: Analytical — protocol analysis, STRIDE threat comparison, exposure window modeling. No empirical packet capture experiment.

**Information leakage surface**: 11 TXT record fields exposed by protocol design. 0 credential material in base (local) configuration. Cloud deployments add one ephemeral key field (10-min expiry, 5-min rotation). Derived from protocol spec (Ch 3 TXT schema), not from runtime capture.

**STRIDE comparison**: Saturn eliminates all three high-severity threats present in static API keys (spoofing, repudiation, elevation of privilege). Trade-off: three medium-severity local-network threats requiring LAN proximity.

**Exposure window**: Saturn key max lifetime 10 minutes vs unbounded for static keys. Meli et al. (2019) found 81% of leaked keys never revoked — Saturn's automatic expiry removes revocation from the equation.

**AP isolation (hard blocker)**: Enterprise/institutional WiFi blocks multicast between clients. Confirmed Jan 2026: eduroam and UCSC-guest both block mDNS. Directly undermines the campus deployment scenario. Not solvable within Saturn protocol — infrastructure decision. See `claims/feasibility/blockers.md`.

**Current mitigations**: Beacon credentials (ephemeral JWTs, 10-min expiry, 5-min rotation). Spending limits cap financial exposure.

**Future work**: Kaiser & Waldvogel's privacy sockets for sensitive deployments, Osborn et al.'s (2016) tiered trust model for granular access control.

**Security honesty gradient**: Components range from full ephemeral lifecycle (saturn-router) to no security features (owui-saturn). Different contexts warrant different postures; Saturn's modular architecture allows this.
