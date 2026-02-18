# BeyondCorp / Zero-Trust

Google's zero-trust security model. Saturn deliberately diverges from it.

## What BeyondCorp is
- No trusted internal network — every request authenticated regardless of origin
- Device inventory, access control engine, identity provider
- "Never trust, always verify" — opposite of Saturn's "trust the network" model

## Why Saturn diverges
Saturn targets consumer/educational environments where zero-trust is impractical:
- Campus WiFi users don't have managed devices
- Coffee shop patrons don't have identity providers
- Home networks don't need enterprise access control
- The overhead of verification destroys zero-config

## The honest trade-off
Saturn trades enterprise-grade verification for zero-config access. This is a deliberate design choice for the target environment, not an oversight. The thesis acknowledges this directly (Claim 3).

## Future bridge
Osborn et al. (2016) BeyondCorp v2 and Kaiser & Waldvogel (2014b) privacy sockets could enable tiered trust models — zero-config by default, opt-in verification for sensitive deployments.

## Papers
- ward-beyer-2014 (BeyondCorp), osborn-2016 (BeyondCorp v2)

## Chapters
- Ch 2.5: zero-trust as contrast
- Ch 7.1: threat model context
- Ch 7.5: future work (tiered trust)
