# Jan AI Client Integration
**Source**: code/jan-integration.md
**Claims**: Claim 1 (proxy pattern extends Saturn to unmodified apps), Claim 2 (one proxy replaces per-app config)

## Source Files
- [`clients/local_proxy_client.py`](https://github.com/jperrello/Saturn/blob/main/clients/local_proxy_client.py) — local proxy that discovers Saturn services and exposes them as an OpenAI-compatible endpoint
- No Jan-side source code — Jan is unmodified

## What It Is

Jan is an open-source desktop application providing a privacy-focused alternative to ChatGPT. It runs LLMs offline and supports cloud integrations via configurable endpoints. Saturn integrates with Jan through `local_proxy_client.py` — a bridge that discovers Saturn services via mDNS and exposes them at `http://127.0.0.1:8080/v1` as an OpenAI-compatible API. Jan thinks it's talking to an OpenAI endpoint. The proxy discovers Saturn services and routes requests to the best available backend based on priority.

Jan has NO native Saturn code. This is a pure proxy integration: the user points Jan at the proxy's address, and the proxy handles all discovery, routing, and failover transparently.

## Architecture

```
Jan Desktop App
    |
    v
Local Proxy (127.0.0.1:8080)
    |  - discovers _saturn._tcp.local. services via mDNS
    |  - aggregates models from all discovered backends
    |  - routes requests by model to correct backend
    |  - automatic failover when services go offline
    v
Saturn Services (discovered via mDNS)
    - Ollama (local, priority 10)
    - OpenRouter (cloud, priority 50)
    - etc.
```

## Setup

**Prerequisites:**
- At least one Saturn server running on the network
- Jan desktop application installed (from jan.ai)
- Python 3.10+

**Steps:**
1. Start a Saturn server: `saturn run openrouter` (or `saturn run ollama`)
2. Start the local proxy: `python clients/local_proxy_client.py` (defaults to `http://127.0.0.1:8080`)
3. In Jan: Settings > Model Providers / Remote Models
4. Add OpenAI-Compatible endpoint with Base URL: `http://127.0.0.1:8080/v1`
5. API Key: leave empty or use any placeholder value

**How routing works:**
1. Jan sends request to local proxy at `http://127.0.0.1:8080/v1`
2. Proxy identifies which Saturn service hosts the selected model
3. Proxy forwards request to the appropriate Saturn service
4. Response flows back through proxy to Jan

## Implementation Details

The proxy is the sole integration point — Jan requires zero modification:

- **Discovery**: `local_proxy_client.py` uses mDNS to browse `_saturn._tcp.local.` and maintains a live service list with health monitoring
- **Model aggregation**: The proxy's model listing endpoint combines models from all discovered Saturn services into a single unified list, which Jan fetches and displays
- **Priority-based routing**: When multiple services offer the same model, the proxy routes to the highest-priority (lowest number) healthy service
- **Automatic failover**: The proxy provides failover when services go offline, combining models from all discovered backends and routing requests to the best available service based on priority
- **No Jan-side code**: Jan is configured once with the proxy address. Adding or removing Saturn servers on the network requires zero changes to Jan — the proxy handles it transparently

The proxy pattern is significant because it proves Saturn can extend to any application that supports "custom OpenAI endpoint" configuration. Jan is one example; Continue, LM Studio, and dozens of other apps support the same pattern.

## How It Supports the Thesis Claims

### Claim 1 — Zero-Config AI Provisioning Is Feasible

**Supports.** Jan demonstrates that Saturn's mDNS discovery extends to completely unmodified third-party applications through the proxy pattern. No Saturn code runs inside Jan — the integration is purely at the network/API level.

**Evidence:**
1. The proxy uses the identical `_saturn._tcp.local.` discovery protocol as all other Saturn components, proving protocol interoperability extends beyond native Saturn consumers
2. Jan's OpenAI-compatible endpoint support is a pre-existing feature designed for manual configuration. Saturn's proxy repurposes it for automatic service discovery — the app doesn't know or care that services were discovered via mDNS

### Claim 2 — Network-Provisioned AI Reduces Total Configuration Effort

**Supports.** One proxy instance replaces per-app, per-provider configuration. Without Saturn, each Jan user would need to independently obtain API keys, configure endpoint URLs, and manage credentials for each AI provider. With Saturn: start proxy, point Jan at `127.0.0.1:8080`, done.

**Evidence:**
1. **Family network use case from docs**: Run one Saturn OpenRouter server on home network. Every family member installs Jan, starts the proxy, and gets access to the same AI models without individual API keys or provider accounts
2. **Zero reconfiguration on service changes**: When the admin adds a new Saturn server to the network, Jan users see its models appear automatically on the next proxy refresh — no reconfiguration of Jan needed
3. **One proxy replaces N provider configs**: Instead of configuring Jan separately for Ollama, OpenRouter, DeepInfra, etc., one proxy aggregates all Saturn-discovered services behind a single address

## Thesis Chapter Mapping

| Chapter | Relevance |
|---------|-----------|
| Ch. 1 (Introduction) | Jan demonstrates the "AI as network infrastructure" vision for consumer desktop apps — install app, start proxy, use AI |
| Ch. 3 (Design) | The proxy pattern is a key design contribution: how Saturn works with applications that have no native mDNS support but do support OpenAI-compatible endpoints |
| Ch. 4 (Implementation) | `local_proxy_client.py` implementation details: mDNS discovery, model aggregation, priority routing, failover |
| Ch. 5 (Scenarios) | Jan + proxy is a first-class scenario: family/household network where one Saturn server provides AI to all Jan clients via proxy |
