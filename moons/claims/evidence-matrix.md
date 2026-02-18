# Claims Evidence Matrix

Cross-reference of all Saturn components against the three thesis claims. Each cell summarizes the evidence type and key citation.

| Component | Language | Claim 1: Feasibility | Claim 2: Reduced Config | Claim 3: Security |
|-----------|----------|---------------------|------------------------|-------------------|
| Core Python Package | Python | Existence proof: `discover()` finds `_saturn._tcp.local.` with zero client config. One `saturn run` command on server side. | Admin: TOML + env var. Consumer: `discover()` returns endpoints. Complexity centralized, not eliminated. | Ephemeral keys (10-min expiry, 5-min rotation). Plaintext TXT records -- deliberate trade-off. |
| saturn-router | Rust | 3rd protocol implementation. Runs on GL.iNet MIPS32 router (~128MB RAM). Saturn in the infrastructure layer alongside DHCP/DNS. | LuCI web UI: 4-5 fields + Save. UCI config with `chmod 600`. Auto-download binary from GitHub. | Full ephemeral lifecycle: generate -> broadcast -> rotate -> delete. Health-based auto-deregistration. |
| ai-sdk-provider-saturn | TypeScript | Cross-language interop. `multicast-dns` npm queries same `_saturn._tcp.local.` as Python `zeroconf`. No bridging layer needed. | Developer: `npm install` + `import`. Zero keys, zero env vars, zero URLs. | Circuit breaker (3 failures -> trip -> 30s cooldown). Auto key refresh on 401. |
| owui-saturn | Python | 4th protocol consumer. Real web app with native plugin architecture. Standard `Zeroconf` + `ServiceBrowser`. | Admin: upload one file. Replaces N per-backend configs. New servers appear automatically. | Honest gap: no auth logic. Security boundary is upstream. |
| saturn-mcp | Python | 5th protocol consumer. MCP ecosystem -- dominant AI assistant extension protocol. | One JSON entry replaces per-provider key management. `list_available_models` aggregates all services. | Ephemeral headers correct. New surface: AI assistant acts on user behalf. |
| VLC Extension | Lua/Python | Consumer app proof. Bridge pattern: Lua -> FastAPI -> mDNS -> Saturn. PyInstaller exe, no Python needed. | Consumer: copy dir, click menu. Zero keys, zero accounts. Auto-detects OS, auto-finds port. | Localhost bridge (127.0.0.1). Unauthenticated `/shutdown`. Rogue service risk via mDNS. |

## Key Observations

**Protocol interoperability**: Five independent mDNS libraries (Python `zeroconf`, Rust `mdns-sd`, TypeScript `multicast-dns`, Python `dns-sd` subprocess, Python `Zeroconf` in OWUI) all consume `_saturn._tcp.local.`. Validates Claim 1 beyond a single-language demo.

**Consumer path convergence**: Every component achieves zero consumer config through different patterns -- native SDK, web plugin, MCP tool, subprocess bridge. The protocol is the constant; the integration is the variable.

**Security honesty gradient**: Components range from full ephemeral lifecycle (saturn-router) to no security features (owui-saturn). Different contexts warrant different postures; Saturn's modular architecture allows this.

**For Adam**: The matrix shows that the code IS the research -- six independent artifacts, each grounded in literature, each backing the same three claims from different angles. The code docs in `code/` contain the detailed evidence with line-number citations.
