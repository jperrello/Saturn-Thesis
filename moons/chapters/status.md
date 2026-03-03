# Chapter Status

| Chapter | Status | Notes |
|---------|--------|-------|
| Abstract | **Written** | 3-paragraph summary covering protocol, contribution, threat models |
| Acknowledgments | **Written** | Short paragraph thanking Adam Smith, Ram Sundara Raman, Peter Biehl |
| Ch 1 Introduction | **Written** | ~5 sections, ~2 pages. Equity argument -> vision -> thesis statement -> 3 claims -> contributions -> organization |
| Ch 2 Background | **Written** | 5 sections, ~10 pages. Service discovery landscape, mDNS/DNS-SD deep dive, AI text completion landscape, DHCP comparison, security/trust |
| Ch 3 Design | **Written** | 5 sections, ~5 pages. Goals, audiences, concepts, protocol spec (TXT schema table), architecture decisions |
| Ch 4 Implementation | **Written** | 4 sections, ~5 pages. Core package, server types, 4 client patterns (SDK/plugin/MCP/subprocess), GL.iNet router |
| Ch 5 Scenarios | **Written** | 3 sections, ~4 pages. Design fiction analysis, VLC case study, 42-target integration analysis |
| Ch 6 Evaluation | **Written** | 4 sections, ~6 pages. Evaluation approach (R1/R2/R3 feasibility), config effort (C2 cognitive walkthrough), security analysis (C3 analytical: protocol leakage surface, STRIDE, exposure windows, AP isolation). Includes 7 tables |
| Ch 7 Discussion | **Written** | 7 sections, ~5 pages. Threat models (4 scenarios), trust/privacy/verification, limitations, relation to prior work, future work, broader implications |
| Ch 8 Conclusion | **Written** | ~1 page. Summarizes all 3 claims with results, equity argument, limitations, future work directions |
| Appendix A | **Written** | Saturn Protocol Specification — formal reference for implementors |
| Appendix B | **Written** | Generative AI in Thesis Development — 4 sections on AI methodology |
| Appendix C | **Written** | Statistical Details — CI computation, variance analysis, sample size |
| Appendix D | **Written** | Scenario Specifications — task descriptions for all 3 evaluation claims |

## Full Thesis Structure (as written in thesis.tex)

```
Abstract (written)
Acknowledgments (written)

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
   1.4 Saturn and This Thesis (3 artifact contributions + organization + AI disclosure)
       - Contribution 1: The Saturn protocol (TXT schema, beacon architecture, _saturn._tcp.local.)
       - Contribution 2: Six reference implementations across 4 languages, scoped for human readability
       - Contribution 3: On-device deployment (Rust on GL.iNet MIPS32 router, full admin stack)
       - Note: artifact contributions (what was built) are distinct from evaluative claims (what was proved)
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

3. Design (WRITTEN)
   3.1 Goals (4 goals)
   3.2 Audiences (4 roles)
   3.3 Concepts (4 abstractions: endpoints, beacons, priorities, ephemeral keys)
   3.4 Protocol Specification (service type, record structure, TXT schema, endpoints, discovery process)
   3.5 Architecture Decisions (4 decisions with justifications)

4. Implementation (WRITTEN)
   4.1 Core Package (Python)
   4.2 Server Types (Ollama, OpenRouter, Fallback)
   4.3 Client Integration Patterns (SDK, plugin, MCP, subprocess)
   4.4 GL.iNet Router Deployment (Rust, OpenWRT, hardware constraints)

5. Scenarios and Applications (WRITTEN)
   5.1 Design Fiction: The Photo Caption Incident
   5.2 VLC Media Player Integration
   5.3 Integration Opportunity Analysis (42 targets)

6. Evaluation (WRITTEN)
   6.1 Evaluation Methodology (agent-based trials, pilot batch design)
   6.2 Discovery Feasibility — C1 (N=5, 100% success, 9.2s mean latency)
   6.3 Configuration Effort — C2 (automated trial: 65% step reduction; walkthrough: 75-88%)
   6.4 Security Analysis — C3 (analytical: 11 fields by protocol design, STRIDE comparison, exposure windows, AP isolation blocker)
   6.5 Threats to Validity

7. Discussion (WRITTEN)
   7.1 Threat Models (corporate exfil, untrusted admin, rogue services, ISP injection)
   7.2 Trust, Privacy, and Verification (broadcast metadata, administrator trust)
   7.3 Limitations and Generalizability (multicast scope, agent vs human, sample size, Docker vs WiFi)
   7.4 Relation to Prior Work (service discovery, AIaaS, security)
   7.5 Future Work (relay, privacy extensions, decentralized, real WiFi, user study, pentesting)
   7.6 Broader Implications (equity, institutional deployment)

8. Conclusion (WRITTEN)
   - Summary of all 3 claims with quantitative results
   - Access equity argument
   - Limitations acknowledgment
   - Four future work categories
   - Closing: "AI as discoverable as printers"

Appendix A: Saturn Protocol Specification (WRITTEN)
Appendix B: Generative AI in Thesis Development (WRITTEN)
Appendix C: Statistical Details (WRITTEN)
Appendix D: Scenario Specifications (WRITTEN)

Bibliography
```

## Figures

| Figure | File | Status |
|--------|------|--------|
| Discovery timeline | `evaluation/figures/discovery-timeline.pdf` | Exists |
| Config comparison | `evaluation/figures/config-comparison.pdf` | Exists |
| Architecture (SVG) | `evaluation/figures/architecture.svg` | Exists but commented out (needs Inkscape) |
| Discovery latency | `evaluation/figures/discovery-latency.pdf` | Exists (not referenced in tex) |
| Exposure spectrum | `evaluation/figures/exposure-spectrum.pdf` | Exists (not referenced in tex) |
