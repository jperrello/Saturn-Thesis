# Saturn Python Package — Claims

## Who uses this package?

Two audiences, both developers:

**Server-side admins** — the person running `saturn run <service>`. Grounded examples from the thesis:
- University IT departments provisioning AI like WiFi (Costa et al. 2024 on AI democratization; Carmona-Galindo et al. 2025 on infrastructure gaps at under-resourced campuses)
- Teachers setting up AI access for a classroom experiment (Gabriel 2024 on educational inequity and premium vs. free tiers)
- A software engineer sharing their API subscription on a home network (Derek in the design fiction)

**Client-side app developers** — the developer who integrates Saturn discovery into their application. From the Fall25 report: "Clients, by contrast, are created by application developers who want to use Saturn." Existing implementations:
- Jan proxy client (Fall25 report, footnote 9)
- VLC extension (Fall25 report, footnote 10)
- OpenWebUI function (Fall25 report)
- SnapQuip in the design fiction (fictional but illustrative)

**End users (Mira, Sarah) never touch this package.** They benefit indirectly — through apps built by client developers, running against servers stood up by admins. The design fiction is explicit: Mira taps "Suggest Caption," gets captions, and doesn't know Saturn exists.

---

## Why this package over alternatives?

### The alternatives (from Fall25 report)
- **LiteLLM** — application-level LLM routing. Proxies many backends through one interface. Every client must be manually pointed at the LiteLLM URL.
- **Requesty** — same category, application-level routing.
- **Open WebUI** — requires running Ollama on the same machine. Single-machine only.
- **Ollama PR #751** — community request for similar discovery functionality. Never merged.
- **Manual API key distribution** — each user gets their own key, configures each app individually. The status quo.

From Fall25 report: "Most work related has focused on application-level LLM routing in projects like LiteLLM and Requesty, which direct user prompts to appropriate models to reduce API costs rather than solving the discovery problem."

### What this package does differently
The proxying is not novel (LiteLLM does it). The **mDNS broadcast** is. `saturn run openrouter` does two things:
1. Spins up an OpenAI-compatible proxy (`runner.py:ServiceRunner.create_app()` — exposes `/v1/health`, `/v1/models`, `/v1/chat/completions`)
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
- The complexity hasn't disappeared — it's been **centralized** in one place instead of scattered across N users

---

## How this maps to Claim 1 (Zero-config is feasible)

The package is the existence proof. Two sides:

**Server side** — `discovery.py:SaturnAdvertiser` registers services on `_saturn._tcp.local.` using the zeroconf library. One call to `register()` and the service is broadcasting. Service configs are TOML files (`services/ollama.toml`, `services/openrouter.toml`, `services/deepinfra.toml`). Running a service is one command: `saturn run ollama`.

**Client side** — `discovery.py:discover()` listens for mDNS responses, parses TXT records, returns a list of `discovery.py:SaturnService` objects. `discovery.py:select_best_service()` sorts by priority and filters by capability. No URLs, no keys, no config files needed by the consumer.

**Literature grounding**: Guttman 2001 (zeroconf designed to "enable direct communications between two or more computing devices via IP" with no configuration); Siddiqui et al. 2012 ("allows users to discover services and devices with little end-user intervention"); Siljanovski et al. 2014 (mDNS adapts to new domains — printers to IoT to AI).

---

## How this maps to Claim 2 (Reduced config burden)

The package embodies the asymmetry: admin complexity is contained in `config.py` + `runner.py` + `providers/`, consumer complexity is zero.

**Admin path**: write a TOML config or use a built-in one → set environment variable for API key → run `saturn run <name>`. Relevant code:
- `config.py:ServiceConfig` — dataclass defining all service configuration
- `config.py:load_service_config()` — loads TOML files from `services/`
- `runner.py:run_service()` — launches the server and registers mDNS
- `runner.py:run_beacon()` — beacon mode with credential rotation
- `providers/openrouter.py`, `providers/deepinfra.py` — provider-specific credential management

**Consumer path**: call `discover()`, get endpoints. Or use `cli_endpoint` to get a URL pasteable into any OpenAI-compatible app.

**The trade-off is honest** (Claim 2 language): "Saturn reduces the total configuration burden across a network compared to per-user manual setup, at the cost of shifting complexity to a single administrator." Someone still pays. Someone still has the API key. Those things are centralized, not eliminated.

From Fall25 report: "A household, university, or office can set up Saturn servers once, and everyone on that network gets access, managed by network administrators."

---

## How this maps to Claim 3 (Security trade-offs)

### The real security issue: packet sniffing
mDNS is broadcast plaintext on the LAN. Kaiser & Waldvogel 2014a: "every machine in the same network will automatically receive all the announcement traffic." Könings et al. 2013: 59% of mDNS device names contain real names; 32% of users unaware.

For beacon mode specifically, ephemeral API keys are broadcast in **plaintext TXT records** (see `runner.py:BeaconAdvertiser._properties()` which puts the credential directly into the `ephemeral_key` TXT record). Anyone on the same network segment can:
1. Passively receive the mDNS announcement
2. Read the `ephemeral_key` from the TXT record
3. Use that key to call the upstream API directly until it expires

For proxy/server mode (non-beacon), HTTP traffic on the LAN is also sniffable — prompts and responses to `host:port/v1/chat/completions` are unencrypted.

### Mitigations in the package
- `runner.py:CredentialManager` — ephemeral keys with configurable expiry (default 10-min lifetime, 5-min rotation via `config.py:BeaconConfig`)
- `providers/openrouter.py:revoke()` — active deletion of old keys
- `providers/deepinfra.py` — scoped JWTs (no revocation needed, they just expire)
- `config.py:BeaconConfig.spending_limit` — caps financial exposure

### The deliberate trade-off
Saturn diverges from zero-trust (Ward & Beyer 2014, BeyondCorp) in favor of zero-config access. The position is that the target environments (campus WiFi, home networks, offices) already have a trust boundary at the network edge. Kaiser & Waldvogel 2014b showed privacy-preserving mDNS-SD is feasible — cited as future work.

The window is real but bounded. The package reduces blast radius (short-lived keys, spending limits) without eliminating the fundamental exposure of broadcast-based discovery.
