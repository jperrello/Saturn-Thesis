# Ephemeral Keys

Time-limited API credentials distributed via mDNS TXT records.

## How it works
- KeyManager creates API keys via provider's provisioning API (e.g., OpenRouter POST /api/v1/keys)
- Keys broadcast in mDNS TXT records as `ephemeral_key` property
- 10-minute key lifetime, 5-minute rotation interval
- Overlap period ensures zero-downtime transitions
- Previous keys deleted after 5-second grace period post-rotation
- On shutdown, current key is deleted

## Why ephemeral
Static API keys fail at scale (see api-key-leakage for full problem statement). Saturn's approach: keys that expire before they can be usefully leaked.

## Analogy
Parallels Kerberos: distribute time-limited credentials for session establishment. The beacon pattern provides session-layer coordination using application-layer protocols.

## Implementation
- Python: `KeyManager` class in openrouter_beacon.py, thread-safe with locks
- Rust: Full ephemeral lifecycle in saturn-router (generate → broadcast → rotate → delete)
- TXT record warns if key exceeds 240 chars (255-byte limit)

## Papers
- meli-2019 (why static keys fail), qazi-2023 (API inventory problem)

## Chapters
- Ch 3.3: concept definition
- Ch 3.4: TXT record schema
- Ch 7.1: threat model context
