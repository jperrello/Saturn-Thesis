# Feasibility Evidence

What proves Saturn works. Organized by evidence type.

## Protocol interoperability (strongest evidence)

Seven independent implementations consume `_saturn._tcp.local.`:

| Component | Language | mDNS Library | What it proves |
|-----------|----------|-------------|----------------|
| Core Python | Python | `zeroconf` | Server + client discovery. `saturn run ollama` starts broadcasting |
| saturn-router | Rust | `mdns-sd` | Runs on GL.iNet router (MIPS32, 128MB RAM) alongside DHCP/DNS |
| ai-sdk-provider | TypeScript | `multicast-dns` | Cross-language interop. `import { saturn }` — zero keys, zero env vars |
| owui-saturn | Python | `Zeroconf` | Real web app (Open WebUI) discovers via native plugin |
| saturn-mcp | Python | `zeroconf` (via core) | AI coding assistants discover through MCP |
| VLC extension | Lua/Python | `dns-sd` subprocess | Consumer app. Copy folder, click menu, talk to AI |
| OpenCode-Saturn | TypeScript | `multicast-dns` (via ai-sdk) | Full coding agent with tool calling, dynamic provider registration, live model updates |

Five different mDNS libraries in three languages. No bridging layer between them. The protocol is the interop surface.

## API-agnostic discovery

Saturn is not locked to the OpenAI API. The `api_type` TXT record field tells clients what kind of backend they're connecting to. Evidence of multiple API types working:

- **Ollama native endpoints**: Ollama exposes both OpenAI-compatible (`/v1/chat/completions`) and native (`/api/generate`, `/api/embeddings`, `/api/chat`) endpoints. Saturn discovers the Ollama service; the client connects directly and can use whichever API the client supports.
- **DeepInfra scoped JWTs**: DeepInfra uses scoped JWT tokens rather than simple API keys. Saturn's core Python package has a dedicated `providers/deepinfra.py` that generates scoped JWTs and broadcasts them as ephemeral credentials. The auth mechanism is provider-specific; Saturn's beacon layer accommodates it.
- **OpenRouter ephemeral keys**: OpenRouter's provisioning API creates time-limited API keys. `providers/openrouter.py` handles the full lifecycle (create, broadcast, rotate, revoke).

Saturn discovers services and provides connection info (URL + credentials). What the client does with that endpoint is between the client and the backend.

## Thin, proven protocol layer

The mDNS record structure:
- PTR record → service browsing (`_saturn._tcp.local.`)
- SRV record → host + port
- TXT record → `api_base`, `api_type`, `priority`, `ephemeral_key`, `rotation_interval`, `version`, `deployment`

This is the same record structure that printer discovery, AirPlay, and Chromecast have used for 20+ years (Guttman 2001, Kim & Reeves 2020).

## Security model (within constraints)

- Ephemeral keys: 10-min lifetime, 5-min rotation, auto-delete on shutdown
- saturn-router: full lifecycle (generate → broadcast → rotate → delete), `Drop` impl ensures cleanup on crash
- ai-sdk-provider: auto key refresh on 401, circuit breaker (3 failures → trip → 30s cooldown)
- Spending limits cap financial exposure per key
- Keys never enter source code, `.env` files, or CI pipelines

## Hardware deployment

saturn-router runs on a GL.iNet GL-MT300N-V2:
- MIPS32 little-endian, no FPU, ~128MB RAM, ~800KB free flash
- Binary: ~2MB (Rust, `opt-level = "z"`, LTO, stripped)
- Runs from RAM (`/tmp/saturn`), managed by procd alongside dnsmasq/hostapd
- LuCI web UI for admin (same interface as firewall/DHCP config)
- Auto-downloads binary from GitHub releases if missing

## Literature grounding

- Guttman (2001): zeroconf designed to "enable direct communications between two or more computing devices via IP" with no configuration
- Siddiqui et al. (2012): "allows users to discover services and devices with little end-user intervention"
- Siljanovski et al. (2014): mDNS adapts to new domains (printers → IoT → AI)
- Kim & Reeves (2020): mDNS originated as printer discovery; Saturn extends the lineage
