# Core Python Package
**Source**: code/python_package_claims.md
**Claims**: Claim 1 (existence proof), Claim 2 (admin/consumer asymmetry), Claim 3 (ephemeral keys, plaintext trade-off)

## Source Files
- [`saturn/discovery.py`](https://github.com/jperrello/Saturn/blob/main/saturn/discovery.py) — `SaturnAdvertiser`, `discover()`, `select_best_service()`, `SaturnService`
- [`saturn/runner.py`](https://github.com/jperrello/Saturn/blob/main/saturn/runner.py) — `ServiceRunner`, `run_service()`, `run_beacon()`, `CredentialManager`
- [`saturn/config.py`](https://github.com/jperrello/Saturn/blob/main/saturn/config.py) — `ServiceConfig`, `BeaconConfig`, TOML loading
- [`saturn/__init__.py`](https://github.com/jperrello/Saturn/blob/main/saturn/__init__.py) — package exports
- [`saturn/__main__.py`](https://github.com/jperrello/Saturn/blob/main/saturn/__main__.py) — CLI entry point (`saturn run <service>`)
- [`saturn/providers/openrouter.py`](https://github.com/jperrello/Saturn/blob/main/saturn/providers/openrouter.py) — OpenRouter credential management + revocation
- [`saturn/providers/deepinfra.py`](https://github.com/jperrello/Saturn/blob/main/saturn/providers/deepinfra.py) — DeepInfra scoped JWTs
- [`saturn/servers/ollama.py`](https://github.com/jperrello/Saturn/blob/main/saturn/servers/ollama.py) — Ollama API translator
- [`saturn/servers/fallback.py`](https://github.com/jperrello/Saturn/blob/main/saturn/servers/fallback.py) — Fallback mock server
- [`saturn/servers/__init__.py`](https://github.com/jperrello/Saturn/blob/main/saturn/servers/__init__.py) — Shared models (ChatMessage, ChatRequest), SSE helpers
- [`saturn/aider_saturn.py`](https://github.com/jperrello/Saturn/blob/main/saturn/aider_saturn.py) — Aider integration (auto-discover + launch)
- [`saturn/services/`](https://github.com/jperrello/Saturn/tree/main/saturn/services) — Built-in TOML configs (deepinfra, openrouter, orbeacon, ollama, fallback)
- [`saturn/tests/`](https://github.com/jperrello/Saturn/tree/main/saturn/tests) — 9 test files, 75 tests total
- [`clients/simple_chat_client.py`](https://github.com/jperrello/Saturn/blob/main/clients/simple_chat_client.py) — example consumer client
- [`clients/local_proxy_client.py`](https://github.com/jperrello/Saturn/blob/main/clients/local_proxy_client.py) — proxy client example
- [`clients/file_upload_client.py`](https://github.com/jperrello/Saturn/blob/main/clients/file_upload_client.py) — file upload client example

## What It Is

The `saturn` Python package (published as `saturn-ai` on PyPI, v1.0.1) implements the Saturn protocol: mDNS-based service discovery and provisioning of LLM APIs on local networks. The package has three layers: a discovery layer (`discovery.py`) that handles mDNS advertisement and listening via the zeroconf library, a configuration and runtime layer (`config.py`, `runner.py`) that manages TOML-based service definitions and FastAPI proxy servers, and a provider layer (`providers/`) that implements ephemeral credential lifecycle for cloud API backends.

The package exposes two CLI entry points: `saturn` (general CLI) and `aider-saturn` (auto-discover and launch the aider coding assistant). All Saturn services present OpenAI-compatible HTTP endpoints (`/v1/chat/completions`, `/v1/models`, `/v1/health`), regardless of their actual backend.

## Implementation Details

### SaturnService dataclass (`discovery.py`)

The core data model for a discovered service. Fields:

- `name: str`, `host: str`, `port: int` — identity and address
- `version: str = "1.0"` — schema version for forward compatibility
- `deployment: str = "network"` — `"cloud"` or `"network"`
- `api_type: str = "openai"` — `"openai"` or `"ollama"`
- `api_base: str = ""` — base URL for cloud/beacon API calls
- `priority: int = 100` — lower = preferred
- `ephemeral_key: str = ""` — API key for beacon deployments
- `rotation_interval: int = 0` — key rotation interval in seconds
- `features: str = ""` — `"ephemeral_auth"` or `"network_proxy"`
- `models: List[str]` — advertised model names
- `capabilities: List[str]` — e.g. `["chat"]`
- `context: int = 4096` — max context window
- `cost: str = "unknown"` — `"free"`, `"paid"`, or `"unknown"`

Computed properties: `is_beacon` (cloud deployment with ephemeral key), `is_cloud`, `is_network`, `effective_endpoint` (returns `api_base` for cloud services, otherwise `http://{host}:{port}/v1`), `endpoint`, `mcp_endpoint`. Query methods: `has_model(model)`, `has_capability(cap)`, `has_all_capabilities(needs)`.

### SaturnDiscovery class (`discovery.py`)

Implements `zeroconf.ServiceListener`. Listens for `_saturn._tcp.local.` services. On `add_service()`: fetches full service info via `zc.get_service_info()`, extracts IP from `info.addresses[0]` via `socket.inet_ntoa()`, decodes TXT record properties (bytes to str), parses comma-separated `models` and `capabilities`, creates a `SaturnService`, and stores it under a thread lock. Supports an `on_service_change` callback for reactive updates. Falls back from `api_type` to legacy `api` TXT field for backward compatibility. `get_all_services()` returns services sorted by priority ascending. `get_best_service()` returns the minimum-priority service.

### discover() function (`discovery.py`)

```python
def discover(timeout: float = 8.0, settle_time: float = 1.0) -> List[SaturnService]
```

Creates a `SaturnDiscovery` with a callback that tracks `last_discovery_time`. Loops until `timeout`, sleeping 0.25s per iteration. Once services exist and no new service has arrived for `settle_time` seconds, breaks early. Returns all services sorted by priority. The settle-time mechanism prevents premature return while mDNS responses are still trickling in.

### select_best_service() function (`discovery.py`)

```python
def select_best_service(
    services: List[SaturnService],
    needs: Optional[List[str]] = None,
    min_context: int = 0,
    prefer_free: bool = True,
) -> Optional[SaturnService]
```

Filters by capabilities (if `needs` provided), then by minimum context window (if `min_context > 0`). If `prefer_free`, sorts by `(priority, 0 if cost=="free" else 1)` — priority first, free preference as tiebreaker. Returns first candidate or None.

### SaturnAdvertiser class (`discovery.py`)

Registers a service on mDNS for others to discover. Service type: `_saturn._tcp.local.`.

**Priority collision avoidance** (`_find_available_priority`): Runs a quick `discover(timeout=2.0, settle_time=0.5)` to scan existing services, collects used priorities, increments until finding an unused value.

**TXT record size management** (`_properties`): mDNS TXT records have a 255-byte limit per key-value pair. The models list is truncated to fit within `MAX_VALUE_BYTES = 255 - len("models") - 1`. Logs a warning if truncated, noting the full list is available via `/v1/models`.

**register()**: Gets hostname and LAN IP, computes `api_base` if not provided, creates a `ServiceInfo` with addresses and properties, calls `zeroconf.register_service()`. Supports context manager protocol (`__enter__`/`__exit__`) for automatic register/unregister lifecycle.

### Configuration system (`config.py`)

Four nested dataclasses: `UpstreamConfig` (base_url, api_key_env), `BeaconConfig` (enabled, provider, rotation_interval=300, expiration_interval=600), `ServerConfig` (port=0 for auto-assign, module for custom server), and `ServiceConfig` (name, deployment, api_type, priority, upstream, server, beacon).

**Config resolution**: User configs in `~/.saturn/services/{name}.toml` shadow built-in configs in `saturn/services/{name}.toml` (bundled with the package).

**Validation**: name required; deployment must be cloud/local/network; api_type must be openai/anthropic/ollama; priority 0-100; upstream.base_url required unless beacon enabled or custom server module set; beacon.provider required when beacon enabled.

**Interactive wizard** (`cmd_config_new`): Prompts for name, deployment type, base URL, API key env var, mode (proxy vs beacon), priority, port. Writes TOML to `~/.saturn/services/`.

**Built-in configs**: `deepinfra.toml` (network/beacon, priority 10, port 8090), `openrouter.toml` (cloud/proxy, priority 50), `orbeacon.toml` (network/beacon, priority 10, port 8090), `ollama.toml` (local, priority 50, custom server module `saturn.servers.ollama`), `fallback.toml` (network, priority 99, custom server module `saturn.servers.fallback`).

### CredentialManager (`runner.py`)

Manages ephemeral API key lifecycle for beacon mode.

```python
class CredentialManager:
    def __init__(self, provider, api_key, rotation_interval=300, expiration_interval=600)
```

**create()**: POSTs to `provider.endpoint` with the real API key in the auth header. Provider-specific payload includes expiration. Parses response to get credential string and optional handle (for revocation). Stores under lock.

**stale()**: Returns True if `time.time() - last_rotation >= rotation_interval`.

**cleanup(final=False)**: If final, revokes ALL handles via `provider.revoke()`. Otherwise keeps the latest handle, revokes all older ones.

**BeaconAdvertiser** (subclass of `SaturnAdvertiser`): Overrides `_properties()` to include `ephemeral_key` from CredentialManager. `re_register()` unregisters then re-registers the mDNS service to update TXT records with the new credential.

**run_beacon() flow**: Loads API key from environment, loads provider module via `saturn.providers.load()`, creates CredentialManager, creates initial credential, registers BeaconAdvertiser on mDNS, starts rotation thread (every 10s checks staleness, creates new credential, re-registers, cleans up old), runs until SIGINT/SIGTERM.

### Provider modules (`providers/`)

Loaded dynamically via `importlib.import_module(f".{name}", package="saturn.providers")`. Each module exports 5 functions: `endpoint` (URL to create credentials), `api_base` (base URL for API calls), `payload(expiration)` (request body), `parse(data)` (extract credential + handle from response), `revoke(api_key, endpoint, handle)` (delete credential).

**DeepInfra** (`providers/deepinfra.py`): Endpoint `https://api.deepinfra.com/v1/scoped-jwt`. Creates scoped JWTs via `{"api_key_name": "auto", "expires_delta": expiration}`. Returns `(data["token"], None)` — no handle, no revocation needed. JWTs self-expire.

**OpenRouter** (`providers/openrouter.py`): Endpoint `https://openrouter.ai/api/v1/keys`. Creates named keys via `{"name": "saturn-beacon-{timestamp}", "expires_at": "ISO8601"}`. Returns `(data["key"], data["data"]["hash"])` — hash used for revocation via DELETE to `{endpoint}/{handle}`.

### ServiceRunner (`runner.py`)

Creates a FastAPI app that proxies requests to an upstream API.

**Endpoints**: `GET /v1/health` (status, service name, deployment info, `saturn: True`), `GET /v1/models` (fetches from upstream, caches result, handles both `data[]` and `models[]` response formats), `POST /v1/chat/completions` (proxies to upstream, forwards model/messages/stream/temperature/max_tokens/tools/tool_choice, supports SSE streaming via `proxy_sse()`, 120s timeout, upstream errors mapped to 502/504).

**run_service() orchestration**: If beacon enabled, delegates to `run_beacon()`. Checks for duplicate running service. Validates config. Finds available port (auto-increment if busy). If custom `server.module` set, imports that module's `app`; otherwise creates ServiceRunner app. Creates SaturnAdvertiser, registers on mDNS. Writes service info to `~/.saturn/run/{name}.json` (pid, port, mdns_name). Runs uvicorn. Cleanup on exit: unregister mDNS, remove service info.

### Server modules (`servers/`)

**Shared utilities** (`servers/__init__.py`): `ChatMessage(BaseModel)` (role, content, tool_calls, tool_call_id), `ChatRequest(BaseModel)` (model, messages, max_tokens, stream, temperature, tools, tool_choice), `chunk()` (creates SSE chunk dict), `completion()` (creates completion response dict), `proxy_sse()` (re-parses and re-emits upstream SSE as StreamingResponse).

**Ollama proxy** (`servers/ollama.py`): Translates between Ollama's native API and OpenAI-compatible format. Endpoints: `GET /v1/health` (checks `localhost:11434/api/version`), `GET /v1/models` (fetches from `localhost:11434/api/tags`, reformats to OpenAI model list), `POST /v1/chat/completions` (translates request to Ollama `/api/chat` format, handles streaming with chunk-by-chunk translation, maps `max_tokens` to `options.num_predict`, forwards tool calls in OpenAI delta format, sets `finish_reason` to `"tool_calls"` when detected).

**Fallback server** (`servers/fallback.py`): Mock server for testing/demo. Only model: `dont_pick_me`. Returns humorous responses. Supports streaming.

### CLI structure (`__main__.py`)

Entry point: `saturn` command. Commands:

- `saturn discover` — `discovery.main()` (argparse with --timeout, --json). Output via `format_service_tree`: tree-formatted display with unicode box-drawing characters (ASCII fallback), showing deployment type, api_type, models, capabilities, context, cost, priority. For beacons: shows api_base and truncated ephemeral_key instead of models.
- `saturn endpoint` — `discovery.cli_endpoint()` (prints best endpoint URL)
- `saturn run <name>` — `runner.main()` (runs service from config)
- `saturn stop <name>` — `runner.stop_service()` (sends SIGTERM)
- `saturn config list|new|delete` — `config.main()`
- `saturn aider` — `aider_saturn.main()`
- `saturn <name>` — shortcut for `saturn run <name>` (if config exists)

### Aider integration (`aider_saturn.py`)

Entry point: `aider-saturn` command. Discovers Saturn services with configurable timeout. Optionally filters by capabilities, min context, free preference. Interactive mode (`--select`): lets user pick service and model. Auto mode: picks best service, first model. Fetches model list from service endpoint (handles both beacon and network). Sets env vars: `OPENAI_BASE_URL`, `OPENAI_API_KEY` (uses ephemeral key for beacons). Launches `aider --model openai/{selected_model}` as subprocess.

### Test coverage

9 test files in `saturn/tests/`, 75 tests total. Key files: `test_service.py` (17 tests — properties, defaults, endpoint computation, model/capability queries), `test_selection.py` (9 tests — priority, capability, context, free preference filters), `test_config.py` (14 tests — from_dict parsing, validation, builtin loading), `test_discovery.py` (8 tests, marked slow — actual mDNS register/discover roundtrips on loopback), `test_runner.py` (6 tests — port finding, service info CRUD, health endpoint), `test_servers.py` (8 tests — chunk/completion helpers, ChatMessage/ChatRequest), `test_fallback.py` (5 tests — HTTP endpoints via TestClient), `test_providers.py` (5 tests — module loading, payload generation), `test_integration.py` (3 tests, marked slow — end-to-end advertise/discover/select/respond). Tests use real mDNS on loopback (`127.0.0.1`). Slow tests have 15-20s timeouts.

---

## Who uses this package?

Two audiences, both developers:

**Server-side admins** -- the person running `saturn run <service>`. Grounded examples from the thesis:
- University IT departments provisioning AI like WiFi (Costa et al. 2024 on AI democratization; Carmona-Galindo et al. 2025 on infrastructure gaps at under-resourced campuses)
- Teachers setting up AI access for a classroom experiment (Gabriel 2024 on educational inequity and premium vs. free tiers)
- A software engineer sharing their API subscription on a home network (Derek in the design fiction)

**Client-side app developers** -- the developer who integrates Saturn discovery into their application. From the Fall25 report: "Clients, by contrast, are created by application developers who want to use Saturn." Existing implementations:
- Jan proxy client (Fall25 report, footnote 9)
- VLC extension (Fall25 report, footnote 10)
- OpenWebUI function (Fall25 report)
- SnapQuip in the design fiction (fictional but illustrative)

**End users (Mira, Sarah) never touch this package.** They benefit indirectly -- through apps built by client developers, running against servers stood up by admins. The design fiction is explicit: Mira taps "Suggest Caption," gets captions, and doesn't know Saturn exists.

---

## Why this package over alternatives?

### The alternatives (from Fall25 report)
- **LiteLLM** -- application-level LLM routing. Proxies many backends through one interface. Every client must be manually pointed at the LiteLLM URL.
- **Requesty** -- same category, application-level routing.
- **Open WebUI** -- requires running Ollama on the same machine. Single-machine only.
- **Ollama PR #751** -- community request for similar discovery functionality. Never merged.
- **Manual API key distribution** -- each user gets their own key, configures each app individually. The status quo.

From Fall25 report: "Most work related has focused on application-level LLM routing in projects like LiteLLM and Requesty, which direct user prompts to appropriate models to reduce API costs rather than solving the discovery problem."

### What this package does differently
The proxying is not novel (LiteLLM does it). The **mDNS broadcast** is. `saturn run openrouter` does two things:
1. Spins up an OpenAI-compatible proxy (`runner.py:ServiceRunner.create_app()` -- exposes `/v1/health`, `/v1/models`, `/v1/chat/completions`)
2. Registers `_saturn._tcp.local.` via `discovery.py:SaturnAdvertiser.register()` so clients find it without being told anything

### When would an admin need this over LiteLLM?
When they don't want to distribute URLs and credentials to every person and every app. From Fall25 report: "Each app might require its own API key, and larger organizations often need separate keys per department or user just to track costs."

### What's easier
- No credential distribution per-client
- No endpoint configuration per-app
- Apps find the service the way they find a printer

### What's harder
- Admin still needs API keys, still pays the bill, still writes TOML config (`services/*.toml`)
- Admin needs to understand beacon vs proxy distinction
- The complexity hasn't disappeared -- it's been **centralized** in one place instead of scattered across N users

---

## How this maps to Claim 1 (Zero-config is feasible)

The package is the existence proof. Two sides:

**Server side** -- `discovery.py:SaturnAdvertiser` registers services on `_saturn._tcp.local.` using the zeroconf library. One call to `register()` and the service is broadcasting. Service configs are TOML files (`services/ollama.toml`, `services/openrouter.toml`, `services/deepinfra.toml`). Running a service is one command: `saturn run ollama`.

**Client side** -- `discovery.py:discover()` listens for mDNS responses, parses TXT records, returns a list of `discovery.py:SaturnService` objects. `discovery.py:select_best_service()` sorts by priority and filters by capability. No URLs, no keys, no config files needed by the consumer.

**Literature grounding**: Guttman 2001 (zeroconf designed to "enable direct communications between two or more computing devices via IP" with no configuration); Siddiqui et al. 2012 ("allows users to discover services and devices with little end-user intervention"); Siljanovski et al. 2014 (mDNS adapts to new domains -- printers to IoT to AI).

---

## How this maps to Claim 2 (Reduced config burden)

The package embodies the asymmetry: admin complexity is contained in `config.py` + `runner.py` + `providers/`, consumer complexity is zero.

**Admin path**: write a TOML config or use a built-in one -> set environment variable for API key -> run `saturn run <name>`. Relevant code:
- `config.py:ServiceConfig` -- dataclass defining all service configuration
- `config.py:load_service_config()` -- loads TOML files from `services/`
- `runner.py:run_service()` -- launches the server and registers mDNS
- `runner.py:run_beacon()` -- beacon mode with credential rotation
- `providers/openrouter.py`, `providers/deepinfra.py` -- provider-specific credential management

**Consumer path**: call `discover()`, get endpoints. Or use `cli_endpoint` to get a URL pasteable into any OpenAI-compatible app.

**The trade-off is honest** (Claim 2 language): "Saturn reduces the total configuration burden across a network compared to per-user manual setup, at the cost of shifting complexity to a single administrator." Someone still pays. Someone still has the API key. Those things are centralized, not eliminated.

From Fall25 report: "A household, university, or office can set up Saturn servers once, and everyone on that network gets access, managed by network administrators."

---

## How this maps to Claim 3 (Security trade-offs)

### The real security issue: packet sniffing
mDNS is broadcast plaintext on the LAN. Kaiser & Waldvogel 2014a: "every machine in the same network will automatically receive all the announcement traffic." Konings et al. 2013: 59% of mDNS device names contain real names; 32% of users unaware.

For beacon mode specifically, ephemeral API keys are broadcast in **plaintext TXT records** (see `runner.py:BeaconAdvertiser._properties()` which puts the credential directly into the `ephemeral_key` TXT record). Anyone on the same network segment can:
1. Passively receive the mDNS announcement
2. Read the `ephemeral_key` from the TXT record
3. Use that key to call the upstream API directly until it expires

For proxy/server mode (non-beacon), HTTP traffic on the LAN is also sniffable -- prompts and responses to `host:port/v1/chat/completions` are unencrypted.

### Mitigations in the package
- `runner.py:CredentialManager` -- ephemeral keys with configurable expiry (default 10-min lifetime, 5-min rotation via `config.py:BeaconConfig`)
- `providers/openrouter.py:revoke()` -- active deletion of old keys
- `providers/deepinfra.py` -- scoped JWTs (no revocation needed, they just expire)

### The deliberate trade-off
Saturn diverges from zero-trust (Ward & Beyer 2014, BeyondCorp) in favor of zero-config access. The position is that the target environments (campus WiFi, home networks, offices) already have a trust boundary at the network edge. Kaiser & Waldvogel 2014b showed privacy-preserving mDNS-SD is feasible -- cited as future work.

The window is real but bounded. The package reduces blast radius (short-lived keys) without eliminating the fundamental exposure of broadcast-based discovery.

---

## Thesis Chapter Mapping

| Chapter | Relevance |
|---------|-----------|
| Ch. 3 (Design) | Two deployment modes (network proxy vs cloud beacon), priority-based routing, TXT record schema, settle-time discovery algorithm |
| Ch. 4 (Implementation) | Full package walkthrough: SaturnService dataclass, SaturnDiscovery/SaturnAdvertiser, config system, ServiceRunner proxy, CredentialManager, provider plugin pattern, Ollama translator, CLI |
| Ch. 5 (Scenarios) | `saturn run deepinfra` on a campus network -> students discover via `saturn discover` or via apps using `discover()` -> zero-config AI access |
| Ch. 6 (Evaluation) | 75 tests across 9 files; real mDNS roundtrips on loopback; end-to-end integration tests (advertise -> discover -> select -> respond) |
| Ch. 7 (Discussion) | Plaintext TXT record exposure, ephemeral key lifecycle as mitigation, admin/consumer asymmetry as deliberate design, config layering (user overrides built-in) |