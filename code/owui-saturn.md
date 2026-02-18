# owui_saturn

## What It Is

An Open WebUI "Pipe" plugin (`owui_saturn.py`) that integrates Saturn's mDNS/DNS-SD service discovery directly into Open WebUI — a popular self-hosted ChatGPT-style web interface. The plugin uses the Python `zeroconf` library to browse for `_saturn._tcp.local.` services on the local network, fetches available models from each discovered service's `/v1/models` endpoint, and presents them as selectable models in Open WebUI's model picker (prefixed with `SATURN/`). Chat requests are routed to the appropriate Saturn service via the OpenAI-compatible `/v1/chat/completions` endpoint, with priority-based automatic failover across services offering the same model. Configuration is exposed through Open WebUI's "Valves" system — five user-adjustable settings (name prefix, discovery timeout, failover toggle, cache TTL, request timeout) that can be modified from the web UI without touching code or files.

## Why It Exists

Open WebUI is one of the most popular open-source ChatGPT alternatives, designed for self-hosted AI access. It already supports connecting to Ollama and OpenAI-compatible APIs, but each connection requires manual endpoint configuration. The Saturn plugin eliminates that configuration: install the plugin, and every Saturn service on the network appears as a selectable model. This transforms Open WebUI from a tool that requires per-backend setup into one that automatically discovers all available AI services.

**Evidence:**

1. **Syed et al. (2025)** document the AIaaS status quo: API keys, accounts, and platform lock-in. Open WebUI without Saturn requires the admin to manually configure each backend connection (Ollama URL, OpenAI API key, etc.). The Saturn plugin replaces this with automatic discovery — `_ensure_discovery_started()` (`owui_saturn.py:158-162`) initializes a `Zeroconf` browser for `_saturn._tcp.local.`, waits for services, and `_get_services()` (line 164-178) returns all discovered services with TTL-based caching. No URL or key entry required.

2. **The plugin leverages Open WebUI's native extension architecture.** Open WebUI's "Pipe" interface expects a class with `pipes()` (return available models) and `pipe()` (handle a chat request). `owui_saturn.py` implements exactly this contract: `pipes()` (line 207-261) discovers services, fetches models from each, and returns them in Open WebUI's expected format. `pipe()` (line 332-368) routes requests to the appropriate Saturn service. The plugin fits into the existing admin workflow — upload a Python file in the Open WebUI admin panel — rather than requiring a fork or custom build.

3. **Guttman (2001)** articulated the zero-config vision of enabling IP communication without configuration. The Saturn plugin extends this into a web application context: the admin installs one plugin, and all Saturn services on the network become available to every Open WebUI user.

## Who It Is Designed For

### Primary: Admin

The plugin is installed and configured by someone managing an Open WebUI instance. This person is comfortable with self-hosted web applications and understands concepts like "Valves" (configurable parameters). They are the same persona as the Saturn server deployer — or someone who works alongside that person in an organizational context.

**Evidence:**

1. **Installation requires admin access to Open WebUI.** The admin uploads `owui_saturn.py` through Open WebUI's plugin management interface. The `Valves` class (line 127-147) exposes five configuration knobs — `NAME_PREFIX`, `DISCOVERY_TIMEOUT`, `ENABLE_FAILOVER`, `CACHE_TTL`, `REQUEST_TIMEOUT` — each with descriptive strings and sensible defaults. These appear in Open WebUI's admin settings panel, matching the same pattern used by other Open WebUI pipes. The admin can tune behavior without editing source code.

2. **The admin decides how Saturn models appear in the UI.** The `NAME_PREFIX` valve (default `"SATURN/"`, line 128-131) controls the prefix prepended to all discovered model names. In `_fetch_models_from_service()` (line 180-202), each model's display name is formatted as `{NAME_PREFIX}{service_name}:{model_name}`. This means the admin controls namespace organization — they can change the prefix to distinguish Saturn models from manually configured ones, or to reflect the network's organizational context.

3. **Meli et al. (2019)** documented pervasive secret leakage from static API keys. The Saturn plugin keeps API keys off the Open WebUI instance entirely. The Open WebUI admin does not enter any API keys for Saturn services — the keys live on the Saturn server side (or in ephemeral mDNS TXT records). The plugin connects to discovered services by URL alone (`service.base_url` at line 305-311). The admin's configuration burden for adding AI backends to Open WebUI drops from "get key, paste key, configure URL, test" to "install plugin."

### Secondary: Consumer

Open WebUI users who interact with the chat interface are consumers. They see Saturn models in the model picker alongside any other configured models and use them identically — type a message, get a response. They do not know or care that the model was discovered via mDNS.

**Evidence:**

1. **Saturn models appear in the standard model dropdown.** `pipes()` (line 207-261) returns a list of `{"id": ..., "name": ...}` dicts that Open WebUI renders as selectable models. The consumer sees entries like "SATURN/OpenRouter:gpt-4o" in the same dropdown as any other model. No separate UI, no special workflow. The consumer's experience is identical to using a manually configured backend.

2. **Costa et al. (2024)** define usability as a dimension of AI democratization. The Saturn plugin achieves invisible integration — the consumer doesn't learn a new tool or navigate a new interface. They use Open WebUI exactly as before; Saturn services simply appear as additional options. If no Saturn services are available, the plugin returns a descriptive placeholder ("No Saturn services discovered" at line 212-217) rather than failing silently.

## How It Supports the Thesis Claims

### Claim 1 — Zero-Config AI Provisioning Is Feasible

**Supports.** The plugin demonstrates Saturn's protocol working inside a real, popular web application — not a custom demo or CLI tool.

**Evidence:**

1. **The plugin uses the standard `_saturn._tcp.local.` service type** via the Python `zeroconf` library. `SaturnDiscovery.__init__()` (line 82-89) creates a `Zeroconf` instance and `ServiceBrowser` for `SATURN = "_saturn._tcp.local."` (line 13). `SaturnServiceListener.add_service()` (line 39-66) parses addresses, ports, and priority from TXT records — the same fields that the Rust router, Python servers, and VLC bridge all use. This is the fourth independent consumer of the Saturn protocol (after the CLI clients, the TypeScript AI SDK provider, and the VLC bridge), further validating protocol interoperability. **Siddiqui et al. (2012)** describe zero-config as requiring "little end-user intervention"; the plugin requires none from the end user and minimal (plugin upload) from the admin.

2. **Model discovery is fully automatic.** `_fetch_models_from_service()` (line 180-202) queries each discovered service's `/v1/models` endpoint — the same OpenAI-compatible endpoint exposed by every Saturn server. The response is parsed identically regardless of whether the backend is Ollama, OpenRouter, or any other Saturn-compatible service. **Guttman (2001)** described zero-config as enabling direct IP communication without configuration; the plugin extends this to model enumeration — the admin doesn't even specify which models exist.

### Claim 2 — Network-Provisioned AI Reduces Total Configuration Effort

**Supports.** The plugin is the clearest demonstration of configuration reduction for a web-based AI interface.

**Evidence:**

1. **Compare the baselines.** Without Saturn, an Open WebUI admin configures each backend individually: Ollama requires setting the API URL; OpenAI requires an API key and optional base URL; LiteLLM requires a proxy URL and model mappings. Each backend is a separate configuration step. With the Saturn plugin, the admin uploads one file. Every Saturn service on the network — regardless of backend type — appears automatically. Adding a new Saturn server to the network requires zero changes in Open WebUI. **Syed et al. (2025)** describe the AIaaS status quo of per-provider configuration; the Saturn plugin collapses N provider configurations into one plugin install.

2. **Priority-based failover reduces ongoing maintenance.** `_get_fallback_services()` (line 284-297) builds a list of alternative services for a given model, sorted by priority. `pipe()` (line 332-368) tries the primary service first, then iterates fallbacks on failure. The admin does not configure failover rules — they emerge automatically from the priority system. If a Saturn server goes down, requests route to the next-priority service offering the same model. **Meli et al. (2019)** documented that "all mitigations act too late" for static key management; Saturn's automatic routing also means the admin doesn't need to manually reconfigure Open WebUI when a backend changes — the plugin adapts via live discovery.

### Claim 3 — Security Trade-offs Are Known and Addressable

**Does not directly support.** The plugin contains no authentication logic, no ephemeral key handling, and no security features beyond what Open WebUI and the Saturn servers independently provide. It connects to discovered services over plain HTTP using `service.base_url` (line 305) and forwards requests without adding credentials.

**Evidence:**

1. **The plugin trusts discovered services implicitly.** `_make_request()` (line 299-318) POSTs to `{service.base_url}/v1/chat/completions` with no authentication headers. It does not verify service identity, check TLS certificates, or validate mDNS announcements. This is consistent with Saturn's deliberate design choice — **Kaiser & Waldvogel (2014a)** note that mDNS traffic is visible to all machines on the network, and Saturn operates within this threat model rather than against it.

2. **The security boundary is upstream.** The plugin inherits whatever security the Open WebUI instance provides (user authentication, session management) and whatever the Saturn servers provide (ephemeral keys in TXT records, health checks). The plugin itself is a transparent pass-through. This is not a weakness per se — it is a clear separation of concerns — but it means `owui_saturn.py` does not contribute evidence to Claim 3. The thesis should note that the plugin trusts the network, which is the expected behavior for zero-config discovery in the target environments (campus WiFi, home networks) described by **Ward & Beyer (2014)** as environments where Saturn deliberately diverges from zero-trust.

## Thesis Chapter Mapping

| Chapter | Relevance |
|---------|-----------|
| Ch. 1 (Introduction) | Open WebUI integration demonstrates the thesis vision concretely: a self-hosted ChatGPT alternative where AI backends are discovered automatically rather than configured manually. Strong hook for the "AI as network infrastructure" narrative. |
| Ch. 3 (Design) | The Pipe/Valves architecture demonstrates Saturn's protocol integrating into an existing plugin system without protocol modifications. The Zeroconf-based discovery (vs. the VLC bridge's subprocess-based discovery) shows two valid client-side implementation strategies for the same protocol. |
| Ch. 4 (Implementation) | Single-file plugin implementation. Zeroconf library usage, TTL-based caching, priority-sorted model aggregation, OpenAI-compatible request forwarding, streaming response passthrough, failover logic. |
| Ch. 5 (Scenarios) | An admin at a university deploys Open WebUI for students. They install the Saturn plugin. Every Saturn server on the campus network appears as available models. Students use the familiar ChatGPT-style interface with no API keys and no per-student configuration. |
| Ch. 6 (Evaluation) | Setup step comparison: Open WebUI with manual Ollama/OpenAI config vs. Open WebUI with Saturn plugin. The plugin reduces backend configuration to a single install step regardless of the number of Saturn services on the network. |
