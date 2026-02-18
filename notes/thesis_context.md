# Saturn Thesis - Working Notes

## Project Summary
**Saturn**: Zero-configuration AI service discovery platform using mDNS/DNS-SD

**Core Innovation**: Eliminates manual configuration for AI service integration by leveraging network service discovery protocols (same tech as finding printers/smart speakers)

**Key Technical Elements**:
- mDNS/DNS-SD broadcasts under `_saturn._tcp.local.`
- OpenAI-compatible REST API layer
- Priority-based routing with automatic failover
- Rich metadata (capabilities, context windows, models, cost)
- Cross-platform (macOS, Windows, Linux)

**Repository**: https://github.com/jperrello/Saturn
**Demo Site**: https://jperrello.github.io/Saturn/

---

## Interview Notes
*Session 1 - 2026-01-27*

### Advisors

**Primary Advisor**: Adam Smith (amsmith@ucsc.edu)
- Associate Professor of Computational Media, UCSC
- Research: design automation, computational creativity, game AI, answer set programming
- Labs: Design Reasoning Lab, Expressive Intelligence Studio, Center for Games and Playable Media
- Note: Joey says they've "had fun" working together

**Co-Advisor**: Ram Sundara Raman (ram@ucsc.edu)
- Assistant Professor, Computer Science & Engineering, UCSC
- Research: Internet measurement, censorship detection, network security, DPI fingerprinting
- Lab: RANDLab (Research on Attacks on Networks and Defenses)

### Timeline
- **Target**: Winter 2026 (this quarter)
- **Format**: UCSC thesis template (LaTeX)

### Framing
Joey wants this positioned as **both computer networks AND HCI research**:
- **Networks**: Protocol design, service discovery mechanics, mDNS/DNS-SD
- **HCI**: Usability, reducing configuration burden, accessibility for non-technical users

---

## Core Thesis Direction

### The Problem
Individual subscription models for GenAI create access inequity. $20-100/month gatekeeps capabilities from people who can't afford it.

### The Vision
**"GenAI access ought to be like printer access"** - if you get on the WiFi, you get the AI too.

AI should be network infrastructure - like WiFi, printers, eduroam. Join the network, gain AI capabilities. No account, no credit card, no API key needed.

### The Contribution
Saturn demonstrates this is technically feasible using existing zero-config protocols (mDNS/DNS-SD), while surfacing new questions about trust and control.

### Joey's Motivation
Started paying $100/month for AI services, realized less well-off people can't afford that. Why not provide AI at the network level (like eduroam) rather than individual subscriptions?

### Working Thesis Statement
> "We can and should provision generative AI at the network level. Saturn demonstrates this is technically achievable using existing zero-configuration protocols, enabling shared access models where joining a network means gaining AI capabilities."

---

## Thesis Claims

**Framing**: Tech-first. Saturn is primarily a systems contribution. The equity argument motivates it (Introduction) and contextualizes its impact (Discussion), but the thesis stands on technical merit. The thesis statement retains "can **and should**" — the normative claim is backed by documented access gaps.

### Claim 1 — Zero-Config AI Provisioning is Feasible
> Zero-configuration network protocols (mDNS/DNS-SD) can provision AI services without end-user configuration.

This is the core technical contribution. Saturn is the existence proof.

**Literature grounding:**
- Guttman (2001) — Zeroconf was designed to "enable direct communications between two or more computing devices via IP" with no configuration; Saturn applies this to AI
- Siddiqui et al. (2012) — Zeroconf foundations; "allows users to discover services and devices with little end-user intervention"
- Siljanovski et al. (2014) — mDNS/DNS-SD adapts to new domains (printers → IoT → AI); "when possible it would be better to adopt preexisting Internet protocols"
- Kim & Reeves (2020) — mDNS literally originated as printer discovery; Saturn extends the lineage to AI

**What Saturn demonstrates:** A working protocol (`_saturn._tcp.local.`), cross-platform implementation, real hardware deployment (GL.iNet router), and client integrations.

### Claim 2 — Network-Provisioned AI Reduces Total Configuration Effort
> Saturn reduces the total configuration burden across a network compared to per-user manual setup, at the cost of shifting complexity to a single administrator.

This claim is comparative and honest about the trade-off: N users do zero work, 1 admin does more work. Net effort decreases.

**Comparison baselines (evaluation planned):**
1. Manual API setup (get key → install client → paste key → configure endpoint → select model)
2. Existing aggregators (LiteLLM, Requesty, OpenRouter direct)
3. Saturn-aware integrations (Jan.ai, OpenCode — zero config vs. their current setup flows)

**Literature grounding:**
- Syed et al. (2025) — Documents the AIaaS status quo: API keys, accounts, platform lock-in
- Costa et al. (2024) — Accessibility and usability as dimensions of AI democratization
- Guttman (2001) — Quoting RFC 1122: "It would be ideal if a host implementation of the Internet protocol suite could be entirely self-configuring"
- Meli et al. (2019) — Static API key management fails at scale; "secret leakage pervasive — affecting over 100,000 repositories"; Saturn eliminates per-user key handling entirely
- Qazi (2023) — "Most of the corporations, unfortunately, do not know the number of APIs they have or how to secure them"; Saturn's ephemeral beacon removes the inventory problem

**Evaluation gap:** No existing literature covers AI service discovery comparison methodology. This is novel territory — Saturn defines the benchmark. Formal evaluation is planned (setup step counts and/or timing across tools).

### Claim 3 — Security Trade-offs are Known and Addressable
> The security and privacy trade-offs of broadcast-based AI discovery are documented in existing literature and can be mitigated without destroying the zero-config property.

**Literature grounding:**
- Kaiser & Waldvogel (2014a) — Passive eavesdropping threat model for mDNS-SD; "every machine in the same network will automatically receive all the announcement traffic"
- Kaiser & Waldvogel (2014b) — Privacy-preserving mDNS-SD is feasible; privacy sockets + pairing maintain backward compatibility
- Könings et al. (2013) — Empirical measurement: 59% of mDNS device names contain real names; 32% of users unaware
- Ward & Beyer (2014) — BeyondCorp zero-trust as the opposing philosophy; Saturn deliberately diverges for consumer/educational access
- Meli et al. (2019) — The static API key model is fundamentally broken: 81% of leaked secrets never removed, best scanning tools only 25% effective, "all mitigations act too late"; Saturn's ephemeral keys (10-min expiry) sidestep the entire leakage class
- Qazi (2023) — Organizations can't track their own API keys; users default to trusting network-level security — aligns with Saturn's model

**Saturn's current mitigations:** Beacon credentials (ephemeral JWTs, 10-min expiry, 5-min rotation). Future work could add Kaiser & Waldvogel's privacy sockets for sensitive deployments, Osborn et al.'s (2016) tiered trust model for granular access control.

**The honest position:** Saturn trades enterprise-grade verification for zero-config access. This is a deliberate design choice for the target environment (campus WiFi, coffee shops, homes), not an oversight.

### Design Decision (supporting detail, not a claim)
Saturn's discovery protocol is backend-agnostic — it works equally with local models (Ollama), cloud aggregators (OpenRouter), or any OpenAI-compatible API. The protocol doesn't prescribe who runs the server. This enables both institutional deployment (university provisions AI like WiFi) and community sharing (individual runs Ollama on a Pi).

---

## Literature Map

How papers from `papersOrg/` map to thesis chapters:

| Paper | Ch.1 Intro | Ch.2 Related Work | Ch.3 Design | Ch.6 Eval | Ch.7 Discussion |
|-------|-----------|-------------------|-------------|-----------|----------------|
| Costa et al. 2024 (AI Democratization) | Motivation | 2.1 | | | Implications |
| Bassignana et al. 2025 (AI Gap) | Motivation | 2.1 | | | Implications |
| Gabriel 2024 (Educational Inequity) | Motivation | 2.1 | | | Implications |
| Carmona-Galindo et al. 2025 (HSI) | | 2.1 | | | |
| Syed et al. 2025 (AIaaS) | Status quo | 2.1 | | Baseline | |
| Guttman 2001 (Zeroconf Origins) | | 2.2 | Justification | | |
| Siddiqui et al. 2012 (Zeroconf Foundations) | | 2.2 | Avahi choice | | |
| Siljanovski et al. 2014 (mDNS for IoT) | | 2.2 | New-domain precedent | | |
| Kim & Reeves 2020 (DNS Vulnerabilities) | Printer metaphor | 2.2 | | | Threat model |
| He et al. 2013 (Chord4S) | | 2.3 | | | |
| Kaiser & Waldvogel 2014a (Privacy) | | 2.3 | | | Threat model |
| Kaiser & Waldvogel 2014b (Efficient Privacy) | | 2.3 | | | Future work |
| Ward & Beyer 2014 (BeyondCorp) | | 2.4 | | | Counterargument |
| Könings et al. 2013 (Device Names) | | 2.4 | | | Privacy data |
| Meli et al. 2019 (Secret Leakage) | Config burden | 2.4 | Ephemeral keys | | Static keys fail |
| Qazi 2023 (API Security) | | 2.4 | JWT choice | | |
| Osborn et al. 2016 (BeyondCorp v2) | | | | | Future work |

---

## Existing Artifacts

### Code (github.com/jperrello/Saturn)
- Core package: discovery, servers (Ollama, OpenRouter, fallback), CLI
- Clients: simple chat, file upload, local proxy with failover
- Beacons: ephemeral JWT credential distribution (10-min expiry, 5-min rotation)
- VLC extension: media player integration
- Open WebUI integration
- **GL.iNet router deployment** - real network infrastructure implementation

### Documentation
- [Design Fiction: The Photo Caption Incident](https://github.com/jperrello/Saturn/blob/main/fiction/design_fiction.md)
  - Narrative illustrating shared AI access, ISP threat model, priority-based failover
  - Legitimate HCI research method
  - Features: Mira (photographer), Derek's Pi proxy, MegaLink ISP ad injection
- [Integration Opportunities Analysis](https://github.com/jperrello/Saturn/blob/main/research/saturn-integration-opportunities.md)
  - 42 potential integration targets analyzed
  - Top 5: Zed Editor, Joplin, Neovim, Raycast, Bruno
  - Complexity estimates, value propositions
- **[Fall25 Saturn Report](../Fall25%20Saturn%20Report.md)** - Quarterly report with polished content:
  - "Too cheap to meter" hook (Lewis Strauss, 1954)
  - Cost analysis: $20/mo subscriptions, $150/M tokens (o1-pro)
  - Printer/Bonjour analogy for zero-config AI
  - Related work: Ollama PR #751, Open WebUI, LiteLLM, Requesty
  - Architecture overview: servers vs clients
  - Integrations: Jan proxy, VLC extension, OpenWebUI function
  - 10 footnote citations ready to convert to BibTeX
- Transcripts (first_pod.txt, second_pod.txt, no_ide.txt) - nature TBD

### Research Explorations
- A2A_MCP - agent-to-agent protocol research
- rings - unknown purpose

### Code Analysis Documents (`code/`)
Six component-level analyses mapping implementation evidence to thesis claims:
- `python_package_claims.md` — Core Python package (server + client discovery)
- `saturn-router.md` — Rust/OpenWRT router deployment
- `ai-sdk-provider-saturn.md` — TypeScript AI SDK integration
- `owui-saturn.md` — Open WebUI plugin
- `saturn-mcp.md` — MCP server for AI coding assistants
- `vlc-extension.md` — VLC media player extension

---

## Claims Evidence Matrix

Cross-reference of all Saturn components against the three thesis claims. Each cell summarizes the evidence type and key citation.

| Component | Language | Claim 1: Feasibility | Claim 2: Reduced Config | Claim 3: Security |
|-----------|----------|---------------------|------------------------|-------------------|
| Core Python Package | Python | Existence proof: `discover()` finds `_saturn._tcp.local.` with zero client config. One `saturn run` command on server side. | Admin: TOML + env var. Consumer: `discover()` returns endpoints. Complexity centralized, not eliminated. | Ephemeral keys (10-min expiry, 5-min rotation). Plaintext TXT records — deliberate trade-off. |
| saturn-router | Rust | 3rd protocol implementation. Runs on GL.iNet MIPS32 router (~128MB RAM). Saturn in the infrastructure layer alongside DHCP/DNS. | LuCI web UI: 4-5 fields + Save. UCI config with `chmod 600`. Auto-download binary from GitHub. | Full ephemeral lifecycle: generate → broadcast → rotate → delete. Health-based auto-deregistration. |
| ai-sdk-provider-saturn | TypeScript | Cross-language interop. `multicast-dns` npm queries same `_saturn._tcp.local.` as Python `zeroconf`. No bridging layer needed. | Developer: `npm install` + `import`. Zero keys, zero env vars, zero URLs. | Circuit breaker (3 failures → trip → 30s cooldown). Auto key refresh on 401. |
| owui-saturn | Python | 4th protocol consumer. Real web app with native plugin architecture. Standard `Zeroconf` + `ServiceBrowser`. | Admin: upload one file. Replaces N per-backend configs. New servers appear automatically. | Honest gap: no auth logic. Security boundary is upstream. |
| saturn-mcp | Python | 5th protocol consumer. MCP ecosystem — dominant AI assistant extension protocol. | One JSON entry replaces per-provider key management. `list_available_models` aggregates all services. | Ephemeral headers correct. New surface: AI assistant acts on user behalf. |
| VLC Extension | Lua/Python | Consumer app proof. Bridge pattern: Lua → FastAPI → mDNS → Saturn. PyInstaller exe, no Python needed. | Consumer: copy dir, click menu. Zero keys, zero accounts. Auto-detects OS, auto-finds port. | Localhost bridge (127.0.0.1). Unauthenticated `/shutdown`. Rogue service risk via mDNS. |

### Key Observations

**Protocol interoperability**: Five independent mDNS libraries (Python `zeroconf`, Rust `mdns-sd`, TypeScript `multicast-dns`, Python `dns-sd` subprocess, Python `Zeroconf` in OWUI) all consume `_saturn._tcp.local.`. Validates Claim 1 beyond a single-language demo.

**Consumer path convergence**: Every component achieves zero consumer config through different patterns — native SDK, web plugin, MCP tool, subprocess bridge. The protocol is the constant; the integration is the variable.

**Security honesty gradient**: Components range from full ephemeral lifecycle (saturn-router) to no security features (owui-saturn). Different contexts warrant different postures; Saturn's modular architecture allows this.

**For Adam**: The matrix shows that the code IS the research — six independent artifacts, each grounded in literature, each backing the same three claims from different angles. The code docs in `code/` contain the detailed evidence with line-number citations.

---

## Chapter Status

| Chapter | Status | Notes |
|---------|--------|-------|
| Abstract | **Written** | 3-paragraph summary covering protocol, contribution, threat models |
| Acknowledgments | **Stub** | Empty |
| Ch 1 Introduction | **Written** | ~5 sections, ~2 pages. Equity argument → vision → thesis statement → 3 claims → contributions → organization |
| Ch 2 Background | **Written** | 5 sections, ~10 pages. Service discovery landscape, mDNS/DNS-SD deep dive, AI text completion landscape, DHCP comparison, security/trust |
| Ch 3 Design | **Written** | 5 sections, ~5 pages. Goals, audiences, concepts, protocol spec (TXT schema table), architecture decisions |
| Ch 4 Implementation | **Written** | 4 sections, ~5 pages. Core package, server types, 4 client patterns (SDK/plugin/MCP/subprocess), GL.iNet router |
| Ch 5 Scenarios | **Written** | 3 sections, ~4 pages. Design fiction analysis, VLC case study, 42-target integration analysis |
| Ch 6 Evaluation | **Stub** | 3 empty section headers: Router Deployment Case Study, Application Integration, Configuration Time Comparison |
| Ch 7 Discussion | **Partial** | Threat Models written (4 subsections: corporate exfil, untrusted admin, rogue services, ISP injection). Trust/Verification, Privacy, Limitations, Future Work are empty section headers |
| Ch 8 Conclusion | **Stub** | Empty |
| Appendix A | **Stub** | Saturn Protocol Specification (empty) |
| Appendix B | **Stub** | Code Listings (empty) |

---

## Actual Thesis Structure (as written in thesis.tex)

```
Abstract (written)
Acknowledgments (stub)

1. Introduction (WRITTEN)
   1.1 The Problem: AI Access Inequity
       - Subscription paywalls ($20-100/mo) [Costa 2024, Bassignana 2025, Capraro 2024]
       - Educational inequity [Gabriel 2024, Carmona-Galindo 2025]
       - AIaaS config burden [Syed 2025]
   1.2 The Vision: AI as Network Infrastructure
       - Printer analogy, zero-config [Guttman 2001, RFC 1122]
   1.3 Thesis Statement
       - "We can and should provision generative AI at the network level"
       - 3 claims: feasibility, reduced config, manageable trade-offs
   1.4 Contributions
       - Protocol design, implementation, evaluation, analysis
   1.5 Thesis Organization

2. Background (WRITTEN)
   2.1 Service Discovery Protocols
       - NetBIOS (name resolution, Windows-centric)
       - WS-Discovery (SOAP/XML overhead)
       - UPnP/SSDP (too much: device control, security history)
       - DLNA (media-only, defunct)
       - Why mDNS/DNS-SD (cross-platform, mature, right fit)
   2.2 mDNS and DNS-SD
       - How mDNS works (multicast 224.0.0.251:5353)
       - DNS-SD and service types (PTR/SRV/TXT)
       - TXT records (key-value metadata, 255-byte limit)
       - Implementations: Bonjour and Avahi
       - Adaptation to new domains (printers → IoT → AI) [Siljanovski 2014]
       - Privacy considerations [Kaiser & Waldvogel 2014a, Könings 2013]
   2.3 The AI Text Completion Landscape
       - Hosted chat apps (Open WebUI, LibreChat)
       - Coding agents and assistants (Cursor, Continue)
       - VS Code mDNS precedent
       - Voice typing and transcription
   2.4 Network Configuration: DHCP and Saturn
       - How DHCP works (RFC 2131)
       - Why not DHCP for service discovery (temporal, multiplicity, privilege)
       - Saturn and DHCP are complementary
   2.5 Security and Trust
       - Zero-trust architecture (BeyondCorp) [Ward & Beyer 2014]
       - Static key leakage [Meli 2019]
       - Saturn's ephemeral credentials as alternative

3. Design (WRITTEN)
   3.1 Goals
       - Zero config for consumers, backend agnosticism, admin centralization, beacon architecture
   3.2 Audiences
       - LLM inference providers, IT administrators, end users, application developers
   3.3 Concepts
       - Endpoints (OpenAI-compatible REST API)
       - Beacons (mDNS announcements, not proxies)
       - Priorities (lower = preferred, admin control mechanism)
       - Ephemeral keys (10-min lifetime, 5-min rotation)
   3.4 Protocol Specification
       - Service type: _saturn._tcp.local.
       - Record structure (PTR/SRV/TXT)
       - TXT record schema (table: version, deployment, api_type, api_base, priority, ephemeral_key, rotation_interval, features)
       - Endpoint expectations (/health, /v1/models, /v1/chat/completions)
       - Discovery process (4-step PTR → SRV/TXT → sort → select)
   3.5 Architecture Decisions
       - Beacon not proxy (no single point of failure, user privacy, simple deployment)
       - No central registry (fully decentralized, link-local scope)
       - Protocol not implementation (4 languages, 5 mDNS libraries)

4. Implementation (WRITTEN)
   4.1 Core Package (Python)
       - Server architecture (saturn run, TOML config, zeroconf library)
       - Client discovery (discover(), one-shot vs persistent modes)
   4.2 Server Types
       - Ollama (local, deployment=network)
       - OpenRouter (cloud, ephemeral key lifecycle)
       - Fallback (failover chain)
   4.3 Client Integration Patterns
       - Native SDK (ai-sdk-provider-saturn, TypeScript, Vercel AI SDK)
       - Application plugin (Open WebUI, Pipe interface, Valves config)
       - Tool protocol bridge (saturn-mcp, FastMCP, stdio transport)
       - Subprocess bridge (VLC extension, Lua→FastAPI→mDNS, PyInstaller)
   4.4 GL.iNet Router Deployment
       - Hardware constraints (MIPS32, 128MB RAM, 800KB flash, Rust)
       - OpenWRT integration (procd, UCI, LuCI, shell RPC)
       - Significance (3rd protocol implementation, runs alongside DHCP/DNS)
       - Limitations (RAM-only, must redeploy after restart)

5. Scenarios and Applications (WRITTEN)
   5.1 Design Fiction: The Photo Caption Incident
       - Scenario summary (Mira, Derek's Pi, MegaLink ISP injection)
       - Design implications:
         * Invisible integration problem
         * Priority as policy
         * "Everyone needs a Derek" problem
   5.2 VLC Media Player Integration
       - User experience (copy dir, menu click, zero config)
       - Technical architecture (Lua→FastAPI bridge, PyInstaller)
       - Significance (consumer-facing, media context, "printer test")
   5.3 Integration Opportunity Analysis
       - 3 integration patterns (native SDK, plugin/extension, OpenAI-compatible endpoint)
       - Top 5 targets (Zed, Joplin, Neovim, Raycast, Bruno)
       - 42 total targets evaluated

6. Evaluation (STUB)
   6.1 Router Deployment Case Study (empty)
   6.2 Application Integration (empty)
   6.3 Configuration Time Comparison (empty)

7. Discussion (PARTIAL)
   7.1 Threat Models (WRITTEN)
       - Corporate data exfiltration (cloud vs local deployment, admin trust)
       - Untrusted local administrator (beacon ≠ proxy, HTTPS direct, logging risk)
       - Rogue services (anyone can register _saturn._tcp.local., priority mitigation)
       - ISP-level injection (firmware updates, design fiction scenario)
   7.2 Trust and Verification (STUB — empty section header)
   7.3 Privacy Implications (STUB — empty section header)
   7.4 Limitations (STUB — empty section header)
   7.5 Future Work (STUB — empty section header)

8. Conclusion (STUB — empty)

Appendix A: Saturn Protocol Specification (STUB — empty)
Appendix B: Code Listings (STUB — empty)
```

---

## Key Connections to Advisors

### For Adam (Computational Media / HCI)
- Design fiction as research method
- Democratizing creative tools
- Reducing friction for non-technical users
- The "printer test" - can grandma use it?

### For Ram (Networks / Security)
- mDNS/DNS-SD protocol mechanics
- Threat model: ISP-injected AI services (from design fiction)
- Network measurement angle - who's broadcasting what?
- Trust/verification in discovered services

---

## Interview Notes — Session 2 (2026-02-07)

### Key Architectural Clarifications

**Saturn is a protocol, not a language-specific implementation.** Implementations exist in Python (general use) and Rust (router hardware constraints). Any language that can do mDNS can participate. The thesis should not frame any one language as "the" implementation.

**Beacon vs. Proxy — resolved framing:**
- **Beacon** = what Saturn *is*. Announces credentials/endpoints via mDNS TXT records. No API traffic flows through the announcer. This is a deliberate security decision.
- **Proxy client** = a *client-side* convenience pattern. Runs on the user's machine, discovers Saturn beacons, presents a stable `localhost` endpoint to apps that can't do mDNS discovery (Jan, etc.). Architecturally distinct from Saturn itself. Not a security concern since it's the user's own process.
- The proxy pattern is necessary because most apps will never add native Saturn discovery. It's how Saturn works with unmodified software.
- **In the thesis**: Ch.3 (Design) defines Saturn as beacon-only. Ch.4 (Implementation) describes proxy as a client pattern.

### Router Deployment Details (from saturn-router README)

- **Hardware**: GL.iNet GL-MT300N-V2, mipsel_24kc, ~128MB RAM, ~800KB available flash
- **Language**: Rust (binary size constraints — TLS alone is ~2MB)
- **Deploys to RAM** (not persistent storage) — must redeploy after router restart
- **Build**: Rust nightly, `build-std` for MIPS32 little-endian + musl libc, Docker cross-compilation
- **Config flow**: UCI (`/etc/config/saturn`) → init script → per-service JSON in `/tmp/saturn.d/` → individual beacon processes
- **Two deployment types**: cloud (ephemeral key rotation) and network (health monitoring)
- **LuCI web interface** for router-based configuration
- **Deployment**: PowerShell script (`deploy-to-router.ps1`) via SCP

### Beacon Credential System (from openrouter_beacon.py)

- `KeyManager` creates ephemeral API keys via OpenRouter's provisioning API (`POST /api/v1/keys`)
- **10-minute key lifetime**, **5-minute rotation interval** (overlap for zero-downtime transitions)
- Keys broadcast in mDNS TXT records as `ephemeral_key` property
- Previous keys deleted after 5-second grace period post-rotation
- Thread-safe (locks), graceful shutdown (deletes current key)
- TXT record properties: `version`, `deployment`, `api_type`, `api_base`, `priority`, `ephemeral_key`, `rotation_interval`, `features`
- Warns if key exceeds 240 chars (mDNS TXT record 255-byte limit)

### Evaluation Decision
- **No user study.** Config-step comparison only (counting steps for manual setup vs. Saturn).
- Baselines TBD but likely: manual API setup, existing aggregators, Saturn.

### Target Deployers
- **Both** institutions and hobbyists. University IT provisions Saturn like WiFi; hobbyist runs Ollama on a Pi. The protocol doesn't prescribe who runs the server.

### Outstanding
- **Significant changes since Fall25 report** (Dec 2025). Joey needs to catch me up — affects Implementation and Evaluation chapters.
- Advisor expectations (Adam, Ram) — not yet discussed.
- Figures/diagrams — not yet discussed.

---

## TODO
- [x] Review Fall25 report contents → polished writing ready to integrate
- [x] Start outlining related work section → detailed Ch.2 outline with paper citations
- [x] Get UCSC LaTeX template set up → `thesis.tex` created with all formatting requirements
- [x] Formalize thesis claims → 3 claims with literature grounding in Thesis Claims section
- [x] Create literature map → papers mapped to thesis chapters
- [x] Write Chapter 1 (Introduction)
- [x] Write Chapter 2 (Background)
- [x] Write Chapter 3 (Design)
- [x] Write Chapter 4 (Implementation)
- [x] Write Chapter 5 (Scenarios and Applications)
- [x] Write Ch 7 Threat Models (4 subsections)
- [ ] Write Ch 6 Evaluation (router case study, app integration, config comparison)
- [ ] Write Ch 7.2 Trust and Verification
- [ ] Write Ch 7.3 Privacy Implications
- [ ] Write Ch 7.4 Limitations
- [ ] Write Ch 7.5 Future Work
- [ ] Write Ch 8 Conclusion
- [ ] Write Acknowledgments
- [ ] Write Appendix A: Protocol Specification
- [ ] Write Appendix B: Code Listings
- [ ] Discuss advisor expectations (Adam, Ram)
- [ ] Plan figures/diagrams

---

## Formatting Requirements

**LaTeX Template**: [`../thesis.tex`](../thesis.tex)

Source: Email from UCSC Graduate Division (`Common requests for formatting revisions.docx`)

### Title Page
- Margins: 1.5" left, 1.25" other sides
- Must say "thesis" (Master's degree)
- Correct graduation month required
- Peter Biehl listed without "Dean" prefix (title on line below)
- ProQuest submission: unsigned
- Signed version: email to vlarkin@ucsc.edu

### Abstract
Format required:
```
Abstract
[Thesis Title]
[Your Name]
```

### Page Numbering (three sections)
| Section | Pages | Numbering |
|---------|-------|-----------|
| Title + Copyright | 1-2 | None |
| Preliminary (TOC, Abstract, etc.) | 3+ | Roman numerals (iii, iv, v...) |
| Main text (Introduction onward) | 1+ | Arabic numerals (1, 2, 3...) |

- All page numbers: centered, bottom, ≥0.75" from edge
- Landscape pages: page number still in portrait orientation at bottom

### Margins (all pages)
- Left: 1.5" minimum
- Top/Right/Bottom: 1.25" minimum
- Applies to figures, tables, formulas
- No headers allowed

### Spacing
- TOC, List of Figures, List of Tables, References: double-spaced (or double-spaced between entries)

---

## Resources & References

### Advisor Links
- [Adam Smith's site](https://adamsmith.as/)
- [Adam Smith - Google Scholar](https://scholar.google.com/citations?user=78OLNd4AAAAJ)
- [Ram Sundara Raman's site](https://ramakrishnansr.com/)
- [Ram Sundara Raman - Google Scholar](https://scholar.google.com/citations?user=1gyokIMAAAAJ)

### Potential Integration Targets
- [Jan.ai](https://jan.ai/) - 40k+ stars, OpenAI-compatible local AI
- [OpenCode](https://opencode.ai/) - 81k+ stars, open-source CLI coding agent

### Protocol References
- mDNS: RFC 6762
- DNS-SD: RFC 6763
