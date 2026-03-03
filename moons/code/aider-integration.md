# Aider Integration
**Source**: code/aider-integration.md
**Claims**: Claim 1 (extends Saturn to existing tools), Claim 2 (zero-config pair programming)

## Source Files
- Part of the `saturn-ai` Python package — the `aider-saturn` CLI command is installed alongside the core Saturn package
- No Aider-side source code modified — Aider is launched unmodified with environment variables pre-configured

## What It Is

`aider-saturn` is a CLI wrapper (part of the `saturn-ai` package) that discovers Saturn services via mDNS, selects the best available service/model, sets `OPENAI_BASE_URL` and `OPENAI_API_KEY` environment variables, and launches Aider with the correct configuration. The user runs one command (`aider-saturn`) instead of manually configuring API keys, endpoint URLs, and model names.

Aider itself is unmodified — it receives standard environment variables and runs normally. The Saturn integration is entirely in the wrapper's discovery and env-var injection logic.

## Architecture

```
aider-saturn (CLI wrapper)
    |
    |  1. Discovers _saturn._tcp.local. services via mDNS
    |  2. Selects best service (priority, capabilities, context)
    |  3. Sets OPENAI_BASE_URL and OPENAI_API_KEY
    |  4. Launches aider with selected model
    v
Aider (unmodified)
    |
    v
Saturn Service (direct connection)
    - Ollama, OpenRouter, DeepInfra, etc.
```

## Implementation Details

### Discovery Flow
1. `aider-saturn` calls `discover()` from the `saturn-ai` package to find all `_saturn._tcp.local.` services on the network
2. Services are filtered by user-specified requirements (capabilities, minimum context window, cost preference)
3. Best service selected via `select_best_service()` — priority-sorted, health-checked

### Interactive Mode (`--select`)
When invoked with `--select`, the wrapper presents an interactive menu:
1. Lists all discovered services with metadata (host, models, context window, cost tier, priority)
2. User selects a service
3. Lists available models from the selected service
4. User selects a model
5. Wrapper sets environment and launches Aider

### Capability and Context Filtering
- `--saturn-needs code,chat` — filter services by required capabilities advertised in mDNS TXT records
- `--saturn-min-context 64000` — require minimum context window size
- `--saturn-prefer-free` — prefer free-tier services (local Ollama) over paid (cloud providers)

### Environment Variable Injection
The wrapper sets two environment variables before launching Aider:
- `OPENAI_BASE_URL` — the selected Saturn service's endpoint URL (e.g., `http://192.168.1.100:8080/v1`)
- `OPENAI_API_KEY` — the service's API key (or ephemeral key from beacon TXT records)

All other command-line arguments are passed through directly to Aider (e.g., `--yes`, `--auto-commits`, `--model`).

### Saturn-Specific CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--select` | Interactive service and model selection | Auto-select |
| `--saturn-model` | Specify model name directly | First available |
| `--saturn-needs` | Required capabilities (comma-separated) | None |
| `--saturn-min-context` | Minimum context window size | 0 |
| `--saturn-prefer-free` | Prefer free services over paid | True |
| `--timeout` | Discovery timeout in seconds | 8.0 |
| `--saturn-verbose` | Show discovery details | False |

## How It Supports the Thesis Claims

### Claim 1 — Zero-Config AI Provisioning Is Feasible

**Supports.** `aider-saturn` proves Saturn's discovery protocol extends to existing AI developer tools without modifying them. Aider doesn't know about Saturn — it just receives environment variables pointing to the right endpoint. The wrapper uses the same `_saturn._tcp.local.` discovery as all other Saturn consumers.

**Evidence:**
1. The `saturn-ai` package's `discover()` function uses `zeroconf` to browse `_saturn._tcp.local.` — the same protocol path as the core package, AI SDK, OWUI plugin, and MCP server
2. Ephemeral key pass-through: when a Saturn beacon announces credentials in TXT records, `aider-saturn` extracts them and passes them as `OPENAI_API_KEY` — Aider uses the ephemeral key without knowing it was discovered via mDNS

### Claim 2 — Network-Provisioned AI Reduces Total Configuration Effort

**Supports.** Aider's standard setup requires: install aider, obtain API key from provider, set `OPENAI_API_KEY`, set `OPENAI_BASE_URL`, choose model. With `aider-saturn`: install `saturn-ai` (includes `aider-saturn`), run `aider-saturn`. Discovery, key injection, and model selection are automatic.

**Evidence:**
1. **Zero manual credential management**: The wrapper discovers services and extracts credentials (including ephemeral keys from beacons) automatically — the developer never touches an API key
2. **Automatic model discovery**: Instead of knowing which models are available and typing exact model names, `aider-saturn --select` shows all available models across all Saturn services
3. **Cost optimization without configuration**: `--saturn-prefer-free` (default: true) automatically routes to local Ollama before paid cloud services — policy-based routing via mDNS priority without per-developer configuration

## Thesis Chapter Mapping

| Chapter | Relevance |
|---------|-----------|
| Ch. 1 (Introduction) | Aider integration demonstrates Saturn's applicability to AI pair programming — a key developer workflow |
| Ch. 3 (Design) | The env-var injection pattern is a third integration approach alongside native SDK and proxy: wrapper discovers, sets env, launches unmodified tool |
| Ch. 4 (Implementation) | `aider-saturn` CLI implementation: discovery, interactive selection, capability filtering, env-var injection, argument pass-through |
