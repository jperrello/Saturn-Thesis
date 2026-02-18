# Saturn Router
**Source**: code/saturn-router.md
**Claims**: Claim 1 (strongest evidence -- real hardware), Claim 2 (LuCI admin UI), Claim 3 (full ephemeral lifecycle)

## What It Is

A Rust binary and full OpenWRT integration layer that turns a consumer router into a Saturn mDNS/DNS-SD beacon. The binary (`src/main.rs`) announces AI service configurations over the local network using the `_saturn._tcp.local.` service type (`mdns.rs:7`), embedding endpoint URLs, API types, priority rankings, and optionally ephemeral credentials into mDNS TXT records. The OpenWRT integration provides a procd init script (`saturn.init`), UCI configuration schema (`saturn.config`), LuCI web interface (`services.js`), and shell RPC backend (`luci.saturn`) -- the complete stack for managing Saturn services on an embedded Linux router. Cross-compiled to `mipsel-unknown-linux-musl` via Docker (`Dockerfile.mipsel`) and Rust nightly's `build-std`, targeting a GL.iNet GL-MT300N-V2 with ~128MB RAM and ~800KB free flash.

## Why It Exists

Saturn's thesis claim is that AI should be network infrastructure -- like WiFi, DHCP, and DNS. To prove that, the protocol cannot live only on general-purpose workstations. It must run on an actual router, the device that *defines* a network. The Python package demonstrates feasibility on laptops and servers; `saturn-router` demonstrates feasibility on the same class of hardware that runs your home gateway.

**Evidence:**

1. **Siljanovski et al. (2014)** established precedent for adapting mDNS/DNS-SD to new domains: printers evolved into IoT. They argue "when possible it would be better to adopt preexisting Internet protocols." `saturn-router` takes this one step further -- the protocol doesn't just run on IoT devices, it runs *on the router itself*, embedded in the network infrastructure layer rather than sitting on top of it.

2. **The deployment architecture in the code** proves the "network infrastructure" framing is literal, not metaphorical. The binary is deployed to `/tmp/saturn` on an OpenWRT device (`deploy-to-router.ps1:85`). The init script (`saturn.init:204`) launches it via procd -- the same service manager that controls dnsmasq, hostapd, and other core router services. Saturn sits alongside DHCP and WiFi in the router's service table. The LuCI menu entry (`luci-app-saturn.json`) places Saturn under "Services" -- the same menu category as DHCP, DNS, and firewall rules.

3. **Guttman (2001)** articulated the zero-config vision: "enable direct communications between two or more computing devices via IP" with no configuration. Router deployment makes Saturn literally zero-config for consumers -- they join the WiFi and the router's mDNS announcements are already there, in the same multicast traffic that carries printer announcements and Chromecast advertisements.

## Who It Is Designed For

### Primary: Admin

This component is designed entirely for the network administrator persona -- someone who controls router hardware, has SSH access, and manages API keys for AI services. The admin configures Saturn through either the UCI command line or the LuCI web interface.

**Evidence:**

1. **The UCI configuration schema** (`saturn.config`) is the standard OpenWRT admin interface. The config template shows five example service configurations spanning cloud and network deployment types, with detailed inline comments explaining each field. The admin writes commands like `uci set saturn.@service[0].api_key='KEY'` and `uci commit saturn` -- the same workflow they'd use to configure any other router service.

2. **The LuCI web interface** (`services.js:146-400`) provides a form-based GUI for service CRUD, with dynamic field visibility (cloud fields hide when deployment is "network" and vice versa), input validation (`name` regex at line 267, URL format at line 290, expiration > rotation at line 333), and live status badges polling every 10 seconds (`poll.add(updateStatusIndicators, 10)` at line 342). This mirrors the admin interfaces for OpenWRT's firewall rules, wireless settings, and DHCP configuration -- familiar patterns for the target user.

3. **The deployment script** (`deploy-to-router.ps1`) is explicitly an admin tool: it uses SCP and SSH, assumes root access, copies files to system directories, and restarts system services. The "Next steps" output at the end instructs the admin to add their API key and enable the service.

### Secondary: Consumer (Indirectly)

A consumer never interacts with `saturn-router`. They never SSH into a router, never open LuCI, never edit UCI. But the router's mDNS announcements are the mechanism by which consumers discover AI services. Once the admin enables a service, every device on the network automatically receives the `_saturn._tcp.local.` broadcasts.

**Evidence:**

1. **Kim & Reeves (2020)** trace mDNS to its origin as printer discovery. The consumer experience with Saturn on a router is identical to Bonjour printer discovery: the consumer joins the WiFi, and the protocol works. No action required from the consumer. The router-as-beacon pattern means the consumer's "configuration" is just connecting to the network -- the same step they already take.

2. **The `MdnsService.register()` method** (`mdns.rs:29-68`) creates a `ServiceInfo` announcement with TXT records containing all the information a client needs: `api_base`, `api_type`, `priority`, and optionally `ephemeral_key` and `rotation_interval` (built by `provider.rs:241-263`). Clients receive these records via standard multicast DNS -- no out-of-band configuration channel exists. The consumer's device discovers the service the same way it discovers printers.

## How It Supports the Thesis Claims

### Claim 1 -- Zero-Config AI Provisioning Is Feasible

**Supports.** This is the single strongest piece of evidence for Claim 1. The router deployment transforms the feasibility argument from "this works on a developer's laptop" to "this works on actual network infrastructure hardware."

**Evidence:**

1. **Third independent implementation of the Saturn protocol.** `saturn-router` is written in Rust, alongside the core Python package and the TypeScript AI SDK provider. All three use the identical `_saturn._tcp.local.` service type and the same TXT record schema (`version`, `deployment`, `api_type`, `api_base`, `priority`, `ephemeral_key`). The Rust implementation uses the `mdns-sd` crate (`mdns.rs:2`) -- a different mDNS library in a different language -- yet interoperates seamlessly with Python's `zeroconf` and JavaScript's `multicast-dns`. This validates the Session 2 clarification: "Saturn is a protocol, not a language-specific implementation. Any language that can do mDNS can participate."

2. **Deployment on constrained hardware.** The target is a MIPS32 little-endian router with no floating-point unit (`mipsel-unknown-linux-musl` target, soft-float ABI via `mipsel-linux-muslsf` toolchain in `Dockerfile.mipsel:15`). The binary is aggressively size-optimized (`Cargo.toml` release profile: `opt-level = "z"`, LTO, single codegen-unit, `panic = "abort"`, stripped). The `~2MB` TLS-enabled binary runs from RAM because flash is too small (`deploy-to-router.ps1:85` copies to `/tmp/saturn`). This demonstrates Saturn works not just on general-purpose hardware but on the cheapest consumer routers -- the kind of device a hobbyist or small institution would actually deploy.

3. **Siddiqui et al. (2012)** describe zero-config foundations where services require "little end-user intervention." The init script (`saturn.init:204-232`) even auto-downloads the binary from GitHub releases if it's missing (`ensure_binary()` at line 41), meaning an OpenWRT router can bootstrap Saturn with no manual file transfer -- the admin just configures UCI and starts the service.

### Claim 2 -- Network-Provisioned AI Reduces Total Configuration Effort

**Supports.** The router deployment is the clearest embodiment of the "1 admin, N users" trade-off that Claim 2 describes.

**Evidence:**

1. **The configuration shift is explicit in the init script.** `start_service()` (`saturn.init:204`) iterates every `config service` section, validates each (`validate_service()` at line 97), generates a per-service JSON config in `/tmp/saturn.d/` (`generate_config()` at line 134), and launches a separate procd-managed process per service. One admin configures once; every device on the network benefits. The auto-incrementing port allocation for cloud services (`CLOUD_PORT_OFFSET` at line 12, used at line 163) means multiple cloud services can coexist without the admin manually deconflicting ports.

2. **The LuCI interface reduces even the admin's burden.** The `services.js` form handles validation (name format, URL format, port range, expiration > rotation), dynamic field visibility (deployment-type-dependent options via `.depends()`), status monitoring (10-second polling), and test connectivity (`callTestConnection` RPC). Compare this to the manual API setup baseline from **Syed et al. (2025)**: create account on provider website, generate API key, install client software, paste key into config file, configure endpoint URL, select model, test. The LuCI form collapses this to: fill in 4-5 fields, click "Save & Apply," click "Start."

3. **Meli et al. (2019)** found secret leakage "pervasive -- affecting over 100,000 repositories." `saturn-router` keeps API keys confined to the router's UCI store (`/etc/config/saturn`) and runtime JSON files with `chmod 600` permissions (`saturn.init:180`). Keys never enter a developer's repository, a `.env` file, or a CI pipeline. The ephemeral key mode goes further -- the admin's real key is never broadcast; only short-lived generated keys appear in mDNS TXT records.

### Claim 3 -- Security Trade-offs Are Known and Addressable

**Supports.** `saturn-router` implements the full ephemeral credential lifecycle and demonstrates multiple mitigation strategies for the broadcast-based threat model.

**Evidence:**

1. **Ephemeral key rotation in `provider.rs`.** `generate_credential()` (line 175) POSTs to the provider's key generation endpoint, creating a time-limited key with configurable expiry (default 600 seconds, `config.rs:52`) and spending limit. The main loop in `main.rs:131-152` rotates credentials on schedule, re-registers mDNS with updated TXT records, then calls `cleanup()` to delete the previous key via the provider's API. The `Drop` impl on `SaturnProvider` (line 296) ensures keys are deleted even on unexpected termination. **Meli et al. (2019)** found that "81% of leaked secrets were never removed" and static key scanning tools catch only 25%. Saturn's ephemeral keys expire automatically -- even if intercepted, their 10-minute window limits exposure. The "leaked secret that's never removed" class is structurally eliminated.

2. **Kaiser & Waldvogel (2014a)** identified passive eavesdropping as the primary threat for mDNS-SD: "every machine in the same network will automatically receive all the announcement traffic." `saturn-router` operates squarely within this threat model. The `txt_records()` method (`provider.rs:241`) places the `ephemeral_key` directly in the mDNS TXT record -- any device on the LAN can read it. This is a deliberate design choice documented in the README's "Beacon, Not Proxy" section: Saturn trades enterprise-grade verification for zero-config access. The target environments (home networks, campus WiFi, small offices) are the same environments where mDNS printer discovery already operates under this same threat model.

3. **Health-based registration/deregistration** (`main.rs:155-182`) provides automatic failover. When `check_health()` fails, the beacon unregisters from mDNS (`mdns_service.unregister()`), removing the service from client discovery. When health recovers, it re-registers. This prevents clients from discovering and connecting to unhealthy or potentially compromised backends. The RPC backend (`luci.saturn:26-55`) independently health-checks services with 5-second curl timeouts, giving the admin real-time visibility. Combined with the LuCI status badges, the admin can identify and respond to anomalous service behavior.

## Thesis Chapter Mapping

| Chapter | Relevance |
|---------|-----------|
| Ch. 1 (Introduction) | The router deployment is the most vivid embodiment of the "AI as network infrastructure" thesis statement. It transforms the printer metaphor from analogy to architecture -- Saturn literally runs on the same device as the network's DHCP and DNS services. |
| Ch. 3 (Design) | Demonstrates the beacon architecture on real hardware. The two deployment types (cloud with ephemeral keys vs. network with health monitoring) map to the design's credential and discovery subsystems. UCI config schema defines the admin's configuration surface. |
| Ch. 4 (Implementation) | Cross-compilation toolchain (Rust nightly, `build-std`, MIPS32 musl, Docker). Procd integration. LuCI web interface. PowerShell deployment script. Auto-download from GitHub releases. This is the most technically complex implementation chapter content. |
| Ch. 5 (Scenarios) | GL.iNet GL-MT300N-V2 deployment is a real-world scenario: constrained hardware, RAM-only binary, actual network serving actual clients. The LuCI interface demonstrates the admin experience. |
| Ch. 6 (Evaluation) | Admin setup step count via LuCI vs. manual API configuration baselines. Binary size constraints as a measure of deployment feasibility on embedded hardware. Health monitoring behavior under failure conditions. |
| Ch. 7 (Discussion) | Broadcast credential trade-off (Kaiser & Waldvogel 2014a). Ephemeral key lifecycle as mitigation (Meli et al. 2019). RAM-only deployment limitation (binary lost on reboot). The honest position: Saturn on a $20 router with no persistent storage is a real constraint that institutional deployments would need to address. |
