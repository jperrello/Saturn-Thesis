# Chapter Status

| Chapter | Status | Notes |
|---------|--------|-------|
| Abstract | **Written** | 3-paragraph summary covering protocol, contribution, threat models |
| Acknowledgments | **Stub** | Empty |
| Ch 1 Introduction | **Written** | ~5 sections, ~2 pages. Equity argument -> vision -> thesis statement -> 3 claims -> contributions -> organization |
| Ch 2 Background | **Written** | 5 sections, ~10 pages. Service discovery landscape, mDNS/DNS-SD deep dive, AI text completion landscape, DHCP comparison, security/trust |
| Ch 3 Design | **Written** | 5 sections, ~5 pages. Goals, audiences, concepts, protocol spec (TXT schema table), architecture decisions |
| Ch 4 Implementation | **Written** | 4 sections, ~5 pages. Core package, server types, 4 client patterns (SDK/plugin/MCP/subprocess), GL.iNet router |
| Ch 5 Scenarios | **Written** | 3 sections, ~4 pages. Design fiction analysis, VLC case study, 42-target integration analysis |
| Ch 6 Evaluation | **Stub** | 3 empty section headers: Router Deployment Case Study, Application Integration, Configuration Time Comparison |
| Ch 7 Discussion | **Partial** | Threat Models written (4 subsections: corporate exfil, untrusted admin, rogue services, ISP injection). Trust/Verification, Privacy, Limitations, Future Work are empty section headers |
| Ch 8 Conclusion | **Stub** | Empty |
| Appendix A | **Stub** | Saturn Protocol Specification (empty) |
| Appendix B | **Stub** | Code Listings (empty) |

## Full Thesis Structure (as written in thesis.tex)

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
       - Adaptation to new domains (printers -> IoT -> AI) [Siljanovski 2014]
       - Privacy considerations [Kaiser & Waldvogel 2014a, Konings 2013]
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

3. Design (WRITTEN — freshly drafted 2026-02-17)
   3.1 Goals (4 goals)
       - Zero config for consumers
       - Backend agnosticism (any OpenAI-compatible endpoint)
       - Administrative centralization (IT person absorbs all config)
       - Credential transience (keys expire before useful theft)
   3.2 Audiences (4 roles)
       - LLM inference providers (distribution incentive)
       - IT administrators (primary user, does all setup)
       - End users (invisible, AirPlay analogy)
       - Application developers (economic motivation: AI without API costs)
   3.3 Concepts (4 abstractions)
       - Endpoints (OpenAI-compatible REST API, de facto standard)
       - Beacons (mDNS announcements, NOT proxies, cloud vs local types)
       - Priorities (lower = preferred, admin policy mechanism, mirrors DNS SRV)
       - Ephemeral keys (10-min lifetime, 5-min rotation, Kerberos parallel)
   3.4 Protocol Specification
       - Service type: _saturn._tcp.local. [RFC 6763 naming]
       - Record structure (PTR -> SRV -> TXT chain)
       - TXT record schema TABLE: 6 required (version, deployment, api_type, api_base, priority, features) + 2 beacon (ephemeral_key, rotation_interval) + optional extensions (models, capabilities, context, cost)
       - Deployment types: cloud (remote API) vs local (on-network inference)
       - Endpoint expectations TABLE: GET /v1/health, GET /v1/models, POST /v1/chat/completions
       - Discovery process: Browse -> Resolve -> Sort -> Select (with health check and failover)
   3.5 Architecture Decisions (4 decisions, each justified against alternative)
       - Beacon not proxy (rejects: single point of failure, prompt visibility, throughput burden)
       - No central registry (rejects: infrastructure dependency; accepts: single-segment limitation)
       - Protocol not implementation (enables multi-language interop)
       - Text completion scope (proves concept on most deployed modality)

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
       - Subprocess bridge (VLC extension, Lua->FastAPI->mDNS, PyInstaller)
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
       - Technical architecture (Lua->FastAPI bridge, PyInstaller)
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
       - Untrusted local administrator (beacon != proxy, HTTPS direct, logging risk)
       - Rogue services (anyone can register _saturn._tcp.local., priority mitigation)
       - ISP-level injection (firmware updates, design fiction scenario)
   7.2 Trust and Verification (STUB -- empty section header)
   7.3 Privacy Implications (STUB -- empty section header)
   7.4 Limitations (STUB -- empty section header)
   7.5 Future Work (STUB -- empty section header)

8. Conclusion (STUB -- empty)

Appendix A: Saturn Protocol Specification (STUB -- empty)
Appendix B: Code Listings (STUB -- empty)
```
