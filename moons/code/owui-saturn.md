# Open WebUI Saturn Plugin
**Source**: code/owui-saturn.md
**Claims**: Claim 1 (4th protocol consumer), Claim 2 (replaces N backend configs), Claim 3 (honest gap -- no auth logic)

## What It Is

An Open WebUI "Pipe" plugin (`owui_saturn.py`) that integrates Saturn's mDNS/DNS-SD service discovery directly into Open WebUI -- a popular self-hosted ChatGPT-style web interface. The plugin uses the Python `zeroconf` library to browse for `_saturn._tcp.local.` services on the local network, fetches available models from each discovered service's `/v1/models` endpoint, and presents them as selectable models in Open WebUI's model picker (prefixed with `SATURN/`). Chat requests are routed to the appropriate Saturn service via the OpenAI-compatible `/v1/chat/completions` endpoint, with priority-based automatic failover across services offering the same model. Configuration is exposed through Open WebUI's "Valves" system -- five user-adjustable settings (name prefix, discovery timeout, failover toggle, cache TTL, request timeout) that can be modified from the web UI without touching code or files.

## Why It Exists

Open WebUI is one of the most popular open-source ChatGPT alternatives, designed for self-hosted AI access. It already supports connecting to Ollama and OpenAI-compatible APIs, but each connection requires manual endpoint configuration. The Saturn plugin eliminates that configuration: install the plugin, and every Saturn service on the network appears as a selectable model. This transforms Open WebUI from a tool that requires per-backend setup into one that automatically discovers all available AI services.

**Evidence:**

1. **Syed et al. (2025)** document the AIaaS status quo: API keys, accounts, and platform lock-in. Open WebUI without Saturn requires the admin to manually configure each backend connection (Ollama URL, OpenAI API key, etc.). The Saturn plugin replaces this with automatic discovery -- `_ensure_discovery_started()` (`owui_saturn.py:158-162`) initializes a `Zeroconf` browser for `_saturn._tcp.local.`, waits for services, and `_get_services()` (line 164-178) returns all discovered services with TTL-based caching. No URL or key entry required.

2. **The plugin leverages Open WebUI's native extension architecture.** Open WebUI's "Pipe" interface expects a class with `pipes()` (return available models) and `pipe()` (handle a chat request). `owui_saturn.py` implements exactly this contract: `pipes()` (line 207-261) discovers services, fetches models from each, and returns them in Open WebUI's expected format. `pipe()` (line 332-368) routes requests to the appropriate Saturn service. The plugin fits into the existing admin workflow -- upload a Python file in the Open WebUI admin panel -- rather than requiring a fork or custom build.

3. **Guttman (2001)** articulated the zero-config vision of enabling IP communication without configuration. The Saturn plugin extends this into a web application context: the admin installs one plugin, and all Saturn services on the network become available to every Open WebUI user.

## Who It Is Designed For

### Primary: Admin

The plugin is installed and configured by someone managing an Open WebUI instance. This person is comfortable with self-hosted web applications and understands concepts like "Valves" (configurable parameters). They are the same persona as the Saturn server deployer -- or someone who works alongside that person in an organizational context.

### Secondary: Consumer

Open WebUI users who interact with the chat interface are consumers. They see Saturn models in the model picker alongside any other configured models and use them identically -- type a message, get a response. They do not know or care that the model was discovered via mDNS.

## How It Supports the Thesis Claims

### Claim 1 -- Zero-Config AI Provisioning Is Feasible

**Supports.** The plugin demonstrates Saturn's protocol working inside a real, popular web application -- not a custom demo or CLI tool.

**Evidence:**

1. **The plugin uses the standard `_saturn._tcp.local.` service type** via the Python `zeroconf` library. `SaturnDiscovery.__init__()` (line 82-89) creates a `Zeroconf` instance and `ServiceBrowser` for `SATURN = "_saturn._tcp.local."` (line 13). `SaturnServiceListener.add_service()` (line 39-66) parses addresses, ports, and priority from TXT records -- the same fields that the Rust router, Python servers, and VLC bridge all use. This is the fourth independent consumer of the Saturn protocol. **Siddiqui et al. (2012)** describe zero-config as requiring "little end-user intervention"; the plugin requires none from the end user and minimal (plugin upload) from the admin.

2. **Model discovery is fully automatic.** `_fetch_models_from_service()` (line 180-202) queries each discovered service's `/v1/models` endpoint -- the same OpenAI-compatible endpoint exposed by every Saturn server. The response is parsed identically regardless of whether the backend is Ollama, OpenRouter, or any other Saturn-compatible service.

### Claim 2 -- Network-Provisioned AI Reduces Total Configuration Effort

**Supports.** The plugin is the clearest demonstration of configuration reduction for a web-based AI interface.

**Evidence:**

1. **Compare the baselines.** Without Saturn, an Open WebUI admin configures each backend individually: Ollama requires setting the API URL; OpenAI requires an API key and optional base URL; LiteLLM requires a proxy URL and model mappings. Each backend is a separate configuration step. With the Saturn plugin, the admin uploads one file. Every Saturn service on the network -- regardless of backend type -- appears automatically. Adding a new Saturn server to the network requires zero changes in Open WebUI.

2. **Priority-based failover reduces ongoing maintenance.** `_get_fallback_services()` (line 284-297) builds a list of alternative services for a given model, sorted by priority. `pipe()` (line 332-368) tries the primary service first, then iterates fallbacks on failure. The admin does not configure failover rules -- they emerge automatically from the priority system.

### Claim 3 -- Security Trade-offs Are Known and Addressable

**Does not directly support.** The plugin contains no authentication logic, no ephemeral key handling, and no security features beyond what Open WebUI and the Saturn servers independently provide. It connects to discovered services over plain HTTP using `service.base_url` (line 305) and forwards requests without adding credentials.

The security boundary is upstream. The plugin inherits whatever security the Open WebUI instance provides (user authentication, session management) and whatever the Saturn servers provide (ephemeral keys in TXT records, health checks). The plugin itself is a transparent pass-through. This is not a weakness per se -- it is a clear separation of concerns -- but it means `owui_saturn.py` does not contribute evidence to Claim 3.

## Thesis Chapter Mapping

| Chapter | Relevance |
|---------|-----------|
| Ch. 1 (Introduction) | Open WebUI integration demonstrates the thesis vision concretely: a self-hosted ChatGPT alternative where AI backends are discovered automatically rather than configured manually. |
| Ch. 3 (Design) | The Pipe/Valves architecture demonstrates Saturn's protocol integrating into an existing plugin system without protocol modifications. |
| Ch. 4 (Implementation) | Single-file plugin implementation. Zeroconf library usage, TTL-based caching, priority-sorted model aggregation, OpenAI-compatible request forwarding, streaming response passthrough, failover logic. |
| Ch. 5 (Scenarios) | An admin at a university deploys Open WebUI for students. They install the Saturn plugin. Every Saturn server on the campus network appears as available models. Students use the familiar ChatGPT-style interface with no API keys and no per-student configuration. |
| Ch. 6 (Evaluation) | Setup step comparison: Open WebUI with manual Ollama/OpenAI config vs. Open WebUI with Saturn plugin. |
