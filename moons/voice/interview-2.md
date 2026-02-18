# Interview Session 2
**Date**: 2026-02-07

## Key Architectural Clarifications

**Saturn is a protocol, not a language-specific implementation.** Implementations exist in Python (general use) and Rust (router hardware constraints). Any language that can do mDNS can participate. The thesis should not frame any one language as "the" implementation.

**Beacon vs. Proxy -- resolved framing:**
- **Beacon** = what Saturn *is*. Announces credentials/endpoints via mDNS TXT records. No API traffic flows through the announcer. Deliberate security decision.
- **Proxy client** = a *client-side* convenience pattern. Runs on the user's machine, discovers Saturn beacons, presents a stable `localhost` endpoint to apps that can't do mDNS discovery (Jan, etc.). Architecturally distinct from Saturn itself.
- The proxy pattern is necessary because most apps will never add native Saturn discovery.
- **In the thesis**: Ch.3 (Design) defines Saturn as beacon-only. Ch.4 (Implementation) describes proxy as a client pattern.

## Router Deployment Details (from saturn-router README)
- **Hardware**: GL.iNet GL-MT300N-V2, mipsel_24kc, ~128MB RAM, ~800KB available flash
- **Language**: Rust (binary size constraints -- TLS alone is ~2MB)
- **Deploys to RAM** (not persistent storage) -- must redeploy after router restart
- **Build**: Rust nightly, `build-std` for MIPS32 little-endian + musl libc, Docker cross-compilation
- **Config flow**: UCI (`/etc/config/saturn`) -> init script -> per-service JSON in `/tmp/saturn.d/` -> individual beacon processes
- **Two deployment types**: cloud (ephemeral key rotation) and network (health monitoring)
- **LuCI web interface** for router-based configuration
- **Deployment**: PowerShell script (`deploy-to-router.ps1`) via SCP

## Beacon Credential System (from openrouter_beacon.py)
- `KeyManager` creates ephemeral API keys via OpenRouter's provisioning API
- **10-minute key lifetime**, **5-minute rotation interval** (overlap for zero-downtime transitions)
- Keys broadcast in mDNS TXT records as `ephemeral_key` property
- Previous keys deleted after 5-second grace period post-rotation
- Thread-safe (locks), graceful shutdown (deletes current key)
- Warns if key exceeds 240 chars (mDNS TXT record 255-byte limit)

## Evaluation Decision
- **No user study.** Config-step comparison only (counting steps for manual setup vs. Saturn).
- Baselines TBD but likely: manual API setup, existing aggregators, Saturn.

## Target Deployers
- **Both** institutions and hobbyists. University IT provisions Saturn like WiFi; hobbyist runs Ollama on a Pi.

## Outstanding
- Significant changes since Fall25 report (Dec 2025). Joey needs to catch me up.
- Advisor expectations (Adam, Ram) -- not yet discussed.
- Figures/diagrams -- not yet discussed.
