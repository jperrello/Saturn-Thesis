# vlc-extension

## What It Is

A two-layer integration that brings Saturn-discovered AI services into VLC media player. The outer layer is a pair of VLC Lua extensions (`saturn_chat.lua` and `saturn_roast.lua`) that provide in-player GUI dialogs for chatting with AI about currently playing media. The inner layer is a Python/FastAPI bridge (`vlc_discovery_bridge.py`) that performs mDNS service discovery via `dns-sd` subprocesses, health-monitors discovered `_saturn._tcp.local.` services, aggregates their models, and exposes an OpenAI-compatible REST API on localhost. The Lua extensions launch the bridge as a background process on activation, communicate with it over HTTP, and shut it down on deactivation. The bridge is packaged into a standalone executable via PyInstaller (`vlc_discovery_bridge.spec`) so end users need no Python installation. Cross-platform: Windows (`start /B`), macOS, and Linux backgrounding are all handled.

## Why It Exists

Saturn's thesis claim is that AI can be provisioned at the network level like printers. To prove that claim is useful — not just technically possible — Saturn needs to show up inside applications that real people already use. VLC is one of the most widely installed desktop applications in the world. If Saturn can bring AI capabilities into VLC without the user configuring an API key, endpoint URL, or model name, it demonstrates that zero-config AI discovery has practical value beyond developer tools and CLI scripts.

**Evidence:**

1. **Siljanovski et al. (2014)** argued that mDNS/DNS-SD adapts to new domains: printers evolved into IoT. The VLC extension extends this lineage further — from IoT into desktop media applications. The bridge's `_run_dns_sd_discovery()` method (`vlc_discovery_bridge.py:112-219`) uses the same `dns-sd -B _saturn._tcp local` browse and `dns-sd -L` lookup pattern as the core Saturn `simple_chat_client.py`, proving the protocol works identically regardless of the host application.

2. **The architecture solves a real integration constraint.** VLC's extension system is Lua-only with no native mDNS support and limited HTTP capabilities (only `vlc.stream()` for GET requests — no POST). The bridge pattern (`saturn_chat.lua:828-920` launches the bridge, reads a port file, connects via HTTP GET with URL-encoded JSON payloads) works around these limitations without modifying VLC itself. This is the "proxy client" pattern described in the Session 2 interview notes: "necessary because most apps will never add native Saturn discovery."

3. **Costa et al. (2024)** frame AI democratization as requiring accessibility and usability. The VLC integration targets a consumer application — media players are used by people who will never touch an API key. The bridge executable is bundled (`bridge/vlc_discovery_bridge.exe`), eliminating the Python dependency. Installation is copying a directory; activation is a menu click (View → Extensions → Saturn Chat).

## Who It Is Designed For

### Primary: Consumer

The VLC extension is the most consumer-facing component in the Saturn codebase. The end user interacts with a VLC dialog window — service/model dropdowns, a chat input, styled HTML output — and never sees a terminal, configuration file, or API key.

**Evidence:**

1. **The installation and activation flow requires zero technical knowledge.** The README instructs: copy the `vlc_extension/` directory to VLC's extensions folder, restart VLC, click View → Extensions → Saturn Chat. No environment variables, no `pip install`, no editing config files. The bridge executable is pre-built and bundled in `bridge/`. The user's interaction surface is a standard VLC dialog created by `create_dialog()` (`saturn_chat.lua:65-99`): dropdowns, text inputs, and buttons. This matches the "printer test" from the advisor notes: "can grandma use it?"

2. **Media context is extracted automatically.** `update_media_context()` (`saturn_chat.lua:333-395`) reads title, artist, album, genre, duration, and current timestamp from VLC's input item metadata via `vlc.input.item()` and `item:metas()`. The user doesn't type what they're watching — the extension already knows. `build_context_string()` (line 397) formats this into the system prompt. The roast extension (`saturn_roast.lua:389-411`) does the same for its comedic prompt. The consumer gets media-aware AI with no effort.

3. **Kim & Reeves (2020)** trace mDNS to its origin as printer discovery — something consumers use without understanding the protocol. The VLC extension replicates this pattern: the consumer opens VLC, plays media, clicks "Saturn Chat," and talks to AI. The discovery protocol is invisible.

### Secondary: Admin (Indirectly)

An admin never interacts with the VLC extension directly, but the extension only works because an admin has deployed Saturn servers somewhere on the network. The bridge discovers those servers via mDNS. The admin's work is upstream — they run `openrouter_server.py` or deploy `saturn-router` on a GL.iNet device. The VLC extension is the payoff for that admin effort.

**Evidence:**

1. **The bridge's `ServiceDiscovery` class** (`vlc_discovery_bridge.py:49-248`) discovers services that admins have registered. The `_discover_services()` method (line 69) runs the same `dns-sd -B _saturn._tcp local` browse that all Saturn components use. Without an admin having registered at least one `_saturn._tcp.local.` service, the bridge finds nothing, and the Lua extension displays "No Saturn services discovered."

2. **Priority-based routing** (`vlc_discovery_bridge.py:309-314`, `BridgeManager.get_best_service()`) respects the priority values that admins set when registering services. The consumer sees "Auto (Best Available)" in the dropdown (`saturn_chat.lua:180`); the admin controls which service that resolves to by setting lower priority numbers on preferred backends.

## How It Supports the Thesis Claims

### Claim 1 — Zero-Config AI Provisioning Is Feasible

**Supports.** The VLC extension is an existence proof that zero-config AI discovery works inside a mainstream consumer application — not just in developer tools or CLI scripts.

**Evidence:**

1. **The bridge uses the identical `_saturn._tcp.local.` discovery protocol** as all other Saturn components. `_run_dns_sd_discovery()` (`vlc_discovery_bridge.py:112`) browses `dns-sd -B _saturn._tcp local`, looks up each service with `dns-sd -L`, parses hostname/port/priority, resolves hostnames to IPs, and deduplicates (preferring non-loopback addresses at line 203-218). The service discovery pattern is byte-for-byte consistent with the Python package's `simple_chat_client.py` and interoperates with the Rust router's mDNS announcements. **Guttman (2001)** defined zero-config as enabling "direct communications between two or more computing devices via IP" with no configuration — the VLC extension achieves this for AI within a media player.

2. **The Lua extension requires zero user configuration to discover and use AI.** `activate()` (`saturn_chat.lua:35-44`) calls `launch_bridge()` which auto-detects the OS (line 784-800), locates the bundled executable (line 837-841), launches it in the background with automatic port assignment (`vlc_discovery_bridge.py:530-542`, `find_port_number()`), and discovers the bridge's address via a port file (line 888-909). The bridge then discovers Saturn services automatically. The user's only action is clicking a menu item. **Siddiqui et al. (2012)** describe zero-config as requiring "little end-user intervention" — this is *no* end-user intervention beyond activation.

### Claim 2 — Network-Provisioned AI Reduces Total Configuration Effort

**Supports.** The VLC extension is the consumer-side evidence that the "1 admin, N users" trade-off works.

**Evidence:**

1. **The consumer's configuration step count is effectively zero.** Compare to the manual baseline from **Syed et al. (2025)** — the AIaaS status quo requires: create provider account, generate API key, install client, paste key, configure endpoint, select model, test. With Saturn + VLC extension: install extension (copy directory), open VLC, click menu item. Service discovery, model enumeration, and routing are all automatic. The `pipes()`/`refresh_services()` functions enumerate available models from all healthy services without user input.

2. **The bridge aggregates multiple services transparently.** `get_models()` (`vlc_discovery_bridge.py:399-417`) iterates all healthy services and returns a unified model list. `chat_completions_core()` (line 455-528) routes to the best service by priority or to a user-specified service. If the admin adds a second Saturn server to the network, the VLC user sees its models appear automatically on the next refresh — no reconfiguration. **Meli et al. (2019)** documented that static API key management "affects over 100,000 repositories"; the VLC user handles zero keys.

### Claim 3 — Security Trade-offs Are Known and Addressable

**Partially supports / complicates.** The VLC extension operates within the same broadcast-based threat model as all Saturn components, but it introduces a new attack surface: the localhost bridge.

**Evidence:**

1. **Kaiser & Waldvogel (2014a)** identified that "every machine in the same network will automatically receive all the announcement traffic." The bridge's discovery mechanism is subject to this: a rogue service broadcasting `_saturn._tcp.local.` on the same LAN would be discovered and potentially selected (if it has the lowest priority). The bridge performs health checks (`HealthMonitor._check_health()` at line 279) but only verifies HTTP 200 on `/v1/health` — it does not validate service identity or authenticity.

2. **The localhost bridge introduces a local attack surface.** The bridge binds to `127.0.0.1` (`vlc_discovery_bridge.py:579`, default host), which limits exposure to the local machine. However, the `/shutdown` endpoint (line 419-431) has no authentication — any process on the machine can terminate the bridge. The GET-based chat endpoint (line 434-449) accepts URL-encoded payloads, which could be triggered by any local process that can issue HTTP GET requests. These are known trade-offs: the bridge is a user's own process on their own machine (as noted in the Session 2 interview: "Not a security concern since it's the user's own process"), but the thesis should acknowledge the localhost binding and unauthenticated shutdown as deliberate design choices.

## Thesis Chapter Mapping

| Chapter | Relevance |
|---------|-----------|
| Ch. 1 (Introduction) | The VLC integration makes the "AI as network infrastructure" vision tangible for a non-technical audience. The printer metaphor is most compelling when demonstrated in a consumer application — "open VLC, get AI" parallels "connect to WiFi, get the printer." |
| Ch. 3 (Design) | The bridge pattern is a key design contribution: how Saturn works with applications that cannot do native mDNS discovery. The Lua→bridge→Saturn service chain demonstrates the "proxy client" architecture described in Session 2 as architecturally distinct from Saturn itself. |
| Ch. 4 (Implementation) | The two-layer Lua/Python architecture, PyInstaller bundling, cross-platform OS detection and backgrounding, port-file IPC, GET-with-URL-encoded-JSON workaround for VLC Lua's HTTP limitations, and race condition fixes (v1.5.1) are all implementation details. |
| Ch. 5 (Scenarios) | The VLC integration is a first-class scenario: a consumer watches a movie, opens Saturn Chat, and asks "what's the name of this song?" with zero configuration. The Saturn Roast extension adds a playful, entertainment-focused use case that demonstrates AI as casual consumer technology. |
| Ch. 7 (Discussion) | The localhost bridge's unauthenticated endpoints, the rogue-service discovery risk, and the GET-encoded-payload workaround are honest limitations to discuss. The bridge pattern's necessity ("most apps will never add native Saturn discovery") is a discussion-worthy architectural trade-off. |
