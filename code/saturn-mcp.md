# saturn-mcp

## What It Is

A Python MCP (Model Context Protocol) server that exposes Saturn's mDNS service discovery as a set of tools consumable by AI coding assistants. Built on Anthropic's `FastMCP` framework (`server.py:8,14`), it wraps the core `saturn` package's `discover()` and `select_best_service()` functions into six MCP tools and one MCP resource, all served over stdio transport. An AI assistant like Claude Code, Cursor, or Windsurf installs this server once, and from that point forward, it can discover Saturn services, enumerate available models, route to the best service by priority, and send chat completions — all without the user ever providing an API key, endpoint URL, or model name. The server is read-only for discovery; it cannot start, stop, or configure Saturn services.

## Why It Exists

Saturn's integration story has two tiers: applications that embed Saturn discovery directly (the AI SDK provider, the VLC extension) and applications that cannot be modified but support a plugin/extension protocol. MCP is Anthropic's open standard for giving AI assistants access to external tools — the dominant extension mechanism for AI coding assistants. Without saturn-mcp, a user of Claude Code or Cursor wanting Saturn services would need to manually configure API keys and endpoints for each provider. With it, the assistant itself performs service discovery.

**Evidence:**

1. **Syed et al. (2025)** document the AIaaS status quo: each application requires its own API key, account, and endpoint configuration. Saturn-mcp eliminates this for the entire class of MCP-compatible AI assistants. A single `mcpServers` entry in the client config (README.md:28-35) replaces per-provider API key management across Claude Code, Cursor, Windsurf, and any future MCP client.

2. **The code delegates entirely to the core discovery protocol.** Every tool begins with the same call: `await _async_discover(timeout, settle_time)` (`server.py:17-18`), which runs the core `saturn.discovery.discover()` function in a thread. The `discover()` function (`discovery.py:186-212`) creates a `SaturnDiscovery` listener, browses `_saturn._tcp.local.`, waits for services to settle, and returns them sorted by priority. Saturn-mcp adds no custom discovery logic — it is a pure protocol bridge from Saturn's mDNS world to MCP's tool-calling world.

3. **The Session 2 interview notes** identify the "proxy client" as "necessary because most apps will never add native Saturn discovery." MCP servers are the AI assistant equivalent of this pattern: the assistant cannot do mDNS natively, so saturn-mcp performs discovery on its behalf and exposes results as structured tool responses.

## Who It Is Designed For

### Primary: Admin (Developer / Power User)

The person who installs saturn-mcp is someone who configures AI coding tools — a developer, a system administrator provisioning developer workstations, or a tech-savvy hobbyist setting up their coding environment. They edit MCP config JSON, run `uv` commands, and understand what a "server" entry means.

**Evidence:**

1. **The installation flow is developer-oriented.** The README offers two paths: ask your AI assistant to install it (README.md:7-9), or manually run `uv venv && uv pip install -e .` and edit the MCP config JSON (README.md:15-35). Both paths require understanding of package managers and config files. The config file locations table (README.md:44-49) references `.mcp.json`, `settings.json`, and `claude_desktop_config.json` — artifacts that consumers never touch.

2. **Meli et al. (2019)** found that static API key leakage is "pervasive — affecting over 100,000 repositories." Developers using AI coding assistants today must paste API keys into config files or environment variables for each provider. Saturn-mcp eliminates this: the `chat_completion` tool (`server.py:140-225`) reads ephemeral keys from discovered beacon TXT records at request time (`server.py:197-198`). No key is ever stored in a config file, a `.env`, or a repository. The developer's security posture improves by removing an entire class of secret from their workflow.

### Secondary: Consumer (Indirectly)

A consumer never configures an MCP server. But if a developer or admin has set up saturn-mcp on a machine, anyone sitting at that machine can ask the AI assistant "what models are on the network?" or "summarize this file using llama3" without knowing Saturn exists. The assistant handles discovery transparently.

**Evidence:**

1. **The example prompts in the README** (README.md:92-98) are phrased in natural language: "Discover Saturn services on my network," "What models are available on my local network?", "Send 'Hello, how are you?' to the deepinfra beacon." These are things a non-technical person could say to their AI assistant. The MCP tool layer translates these natural language requests into mDNS discovery and API calls.

2. **Kim & Reeves (2020)** trace mDNS to its origin as printer discovery — technology consumers use without understanding. Saturn-mcp applies the same pattern one layer up: the consumer asks their AI assistant a question, and the assistant uses MCP tools to discover Saturn services via mDNS. The consumer never sees a protocol, a port number, or a TXT record.

## How It Supports the Thesis Claims

### Claim 1 — Zero-Config AI Provisioning Is Feasible

**Supports.** Saturn-mcp is an existence proof that zero-config AI discovery works within the MCP ecosystem — the dominant extension protocol for AI coding assistants.

**Evidence:**

1. **Guttman (2001)** defined zero-config as enabling "direct communications between two or more computing devices via IP" with no configuration. Saturn-mcp achieves this for AI assistants: after a one-time MCP server registration, the assistant discovers all Saturn services automatically. The `discover_saturn_services` tool (`server.py:31-50`) takes optional timeout parameters but requires no endpoint URLs, API keys, or service names. The `service_to_dict` helper (`server.py:21-28`) serializes the full `SaturnService` metadata — including `effective_endpoint`, `is_beacon`, `is_cloud`, `is_network`, and `ephemeral_key` — so the assistant has everything it needs to interact with any discovered service.

2. **The `find_service_for_model` tool** (`server.py:102-118`) demonstrates end-to-end zero-config model routing. An AI assistant calls `find_service_for_model("llama3.2")`, which discovers all services via mDNS, filters to those advertising the model (`SaturnService.has_model()`, `discovery.py:69-70`), and returns the best one by priority (`select_best_service()`, `discovery.py:215-237`). No configuration was needed beyond the model name. **Siddiqui et al. (2012)** describe zero-config as requiring "little end-user intervention" — here the only intervention is the natural-language question the user asks their assistant.

3. **Saturn-mcp uses the identical `_saturn._tcp.local.` protocol** as the Python package, the TypeScript AI SDK provider, the VLC bridge, and the Rust router. The `_async_discover` wrapper (`server.py:17-18`) calls `saturn.discovery.discover()` directly, which browses `_saturn._tcp.local.` via zeroconf. This confirms the Session 2 clarification: "Saturn is a protocol, not a language-specific implementation." Saturn-mcp is yet another client consuming the same protocol — this time from inside an AI assistant.

### Claim 2 — Network-Provisioned AI Reduces Total Configuration Effort

**Supports.** Saturn-mcp reduces the configuration effort for AI coding assistant users from per-provider key management to a one-time MCP server installation.

**Evidence:**

1. **Step-count comparison.** Traditional setup for an AI coding assistant to use a new provider: create account on provider website, generate API key, store key in environment variable or config file, configure endpoint URL, select model, test connection. Saturn-mcp setup: add one JSON entry to MCP config (README.md:28-35), done. The `chat_completion` tool (`server.py:140-225`) handles service selection, model routing, endpoint resolution, and ephemeral key authentication automatically. **Syed et al. (2025)** document this per-provider burden as the AIaaS status quo. Saturn-mcp collapses N provider configurations into one MCP server entry.

2. **The `list_available_models` tool** (`server.py:53-99`) demonstrates aggregation across multiple Saturn services. It discovers all services, queries each one's `/v1/models` endpoint (using ephemeral keys from beacon TXT records for authentication, lines 73-74), and returns a unified model catalog keyed by service name. If an admin adds a new Saturn server to the network, the AI assistant's next `list_available_models` call returns its models automatically — zero reconfiguration on the client side. **Meli et al. (2019)** found that even the best secret-scanning tools catch only 25% of leaked keys. Saturn-mcp sidesteps the problem entirely: keys are discovered from mDNS at runtime and never written to disk.

### Claim 3 — Security Trade-offs Are Known and Addressable

**Partially supports / complicates.** Saturn-mcp operates within the known mDNS broadcast threat model and correctly uses ephemeral credentials, but the MCP tool layer introduces a new trust surface: the AI assistant acts on the user's behalf when sending chat completions to discovered services.

**Evidence:**

1. **Kaiser & Waldvogel (2014a)** identified that "every machine in the same network will automatically receive all the announcement traffic." Saturn-mcp inherits this: the `discover_saturn_services` tool discovers all `_saturn._tcp.local.` services on the LAN, including potentially rogue ones. There is no service identity verification — any device broadcasting the correct service type will appear in results. The `chat_completion` tool (`server.py:140-225`) will route requests to whatever `select_best_service()` returns, which selects by priority alone. A malicious service advertising priority 1 would be selected over legitimate services at higher priority numbers.

2. **Ephemeral key handling is correct.** When a service is a beacon with an ephemeral key, both `list_available_models` (`server.py:73-74`) and `chat_completion` (`server.py:197-198`) add `Authorization: Bearer {ephemeral_key}` headers. This aligns with Saturn's credential rotation design: keys have 10-minute lifetimes and 5-minute rotation intervals (thesis_context.md:322-324). **Meli et al. (2019)** documented that "81% of leaked secrets [are] never removed" — Saturn's ephemeral keys self-expire, and saturn-mcp never persists them. However, the keys are broadcast in mDNS TXT records visible to all devices on the network, which is the deliberate trade-off for the target environment documented in Claim 3 of the thesis.

3. **The MCP layer adds an agent trust dimension.** The `chat_completion` tool allows the AI assistant to send arbitrary prompts to discovered services on the user's behalf. The user controls this through MCP client permission systems (e.g., Claude Code's tool approval prompts), but the saturn-mcp server itself has no access controls. This is consistent with the thesis's honest position: "Saturn trades enterprise-grade verification for zero-config access." The MCP server is the user's own process (Session 2: "Not a security concern since it's the user's own process"), but the thesis should note that MCP tool approval is the user's defense against unintended service interaction.

## Thesis Chapter Mapping

| Chapter | Relevance |
|---------|-----------|
| Ch. 3 (Design) | Saturn-mcp demonstrates the beacon protocol consumed from inside an AI assistant. The MCP server is a pure read-only client: it discovers services and reads their metadata but never acts as a beacon or proxy. This validates the beacon vs. client distinction from Session 2. |
| Ch. 4 (Implementation) | The `FastMCP` framework integration, `asyncio.to_thread` wrapper for the synchronous discovery function, `httpx`-based model enumeration with ephemeral key auth, and stdio transport are all implementation details. The dependency on the core `saturn` package via path reference (`pyproject.toml:14`) shows the modular package architecture. |
| Ch. 5 (Scenarios) | An AI coding assistant discovering Saturn services is a compelling scenario: a developer asks "what models are on my network?" and the assistant answers without any prior configuration. This scenario targets the developer audience specifically and complements the consumer-facing VLC scenario. |
| Ch. 7 (Discussion) | MCP as an integration pattern: most AI applications will not add native Saturn discovery, but many AI assistants already support MCP. Saturn-mcp demonstrates that Saturn can reach AI assistants through their native extension mechanism. The agent trust surface (AI acting on behalf of user via discovered services) is worth discussing alongside the rogue-service and eavesdropping threat models from Kaiser & Waldvogel (2014a). The thesis_context.md lists MCP under "Future work" (Ch. 7) — saturn-mcp partially realizes this, shifting it from speculative to implemented. |
