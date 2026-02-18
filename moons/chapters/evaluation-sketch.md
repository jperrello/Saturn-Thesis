# Chapter 6 Evaluation — Sketch

Draft plan for all evaluation experiments. Each section maps to a claim.

---

## 6.1 Claim 1: Feasibility Experiments

### 6.1.1 Discovery Latency Benchmark

**Hypothesis**: A Saturn client discovers and connects to an advertised service in under 2 seconds on a typical LAN.

**Setup**:
- Single-segment LAN (home router or campus WiFi)
- Saturn server advertising 1, 5, and 20 services via `_saturn._tcp.local.`
- Client runs `discover()` from cold start (no cached records)
- Measure wall-clock time from `discover()` call to first usable `SaturnService` object
- 100 trials per service count
- Hardware: commodity laptop + GL.iNet router (for router variant)

**Measurements**:
- Time to first service (ms) — median, p95, p99
- Time to full enumeration (ms)
- Compare: 1 service vs 5 vs 20 (does mDNS scale linearly?)

**Baseline**: Manual configuration time (even just pasting a URL is ~5 seconds of human action). Also compare against mDNS discovery of other service types (e.g. `_http._tcp.local.`) to show Saturn doesn't add overhead beyond standard mDNS.

**Implementation**: Python script using `time.perf_counter()` around `discover()`. Output CSV. Plot latency distribution as box plot.

### 6.1.2 Cross-Platform Interoperability Matrix

**Hypothesis**: All five Saturn mDNS library implementations can discover services advertised by any other implementation.

**Setup**:
- 5 implementations: Python `zeroconf`, Rust `mdns-sd`, TypeScript `multicast-dns`, Python `dns-sd` subprocess, Python `Zeroconf` (OWUI variant)
- Each advertises a test service
- Each attempts to discover all others
- 5x5 matrix of pass/fail

**Measurements**:
- Binary pass/fail per cell
- TXT record fidelity: do all parsed fields match what was advertised?
- Record any quirks (e.g. encoding differences, case sensitivity)

**Output**: Table in thesis. Any failures are documented and explained.

**Implementation**: Script that spins up each advertiser in sequence, queries with each client, logs results.

### 6.1.3 Failure Recovery Timing

**Hypothesis**: Saturn clients detect a downed service and failover to the next-priority service within one mDNS TTL cycle.

**Setup**:
- 2 Saturn servers, priority 10 and priority 20
- Client connected to priority-10 server
- Kill priority-10 server
- Measure time until client discovers the loss and switches to priority 20

**Measurements**:
- Detection time (ms) — from server kill to client awareness
- Failover time (ms) — from detection to successful request on backup
- Compare persistent discovery mode vs one-shot re-query

**Implementation**: Python script. Kill server process, poll client state.

---

## 6.2 Claim 2: Reduced Configuration Effort

### 6.2.1 Cognitive Walkthrough (Automated with Playwright)

**Hypothesis**: Saturn-aware applications require fewer cognitive steps, fewer error-prone decisions, and less domain knowledge than manual AI service setup.

**Method**: Cognitive walkthrough (Wharton et al. 1994) — systematic expert evaluation. For each action in a task sequence, answer four questions:
1. Will the user try to achieve the right effect?
2. Will the user notice the correct action is available?
3. Will the user associate the correct action with the desired effect?
4. Will the user see progress toward their goal?

**Playwright automation idea**: Script browser-based setup flows to capture exact step sequences, screenshots at each decision point, and timing. This creates reproducible evidence without needing human participants.

**Walkthroughs to script**:

| Tool | Setup Flow | Expected Steps |
|------|-----------|----------------|
| OpenRouter (manual) | Sign up → verify email → add payment → generate API key → copy key → open app → paste key → configure endpoint URL → select model → test | ~12-15 steps |
| LiteLLM | Install → create config YAML → add API keys → start proxy → configure client to use proxy URL → test | ~8-10 steps |
| Ollama (local, manual) | Download → install → pull model → note port → open app → enter localhost URL → test | ~7-8 steps |
| Saturn + Ollama | `saturn run ollama` (admin, once) → user opens app → it works | 1 admin step, 0 user steps |
| Saturn + OpenRouter | Admin: `saturn run openrouter --key=X` → user opens app → it works | 1 admin step, 0 user steps |

**Playwright scripts capture**:
- Screenshot at each page/state
- Count of form fields filled
- Count of copy-paste actions
- Count of external context switches (go to docs, go to dashboard, etc.)
- Total page loads
- Any error recovery loops (wrong key format, endpoint typo, etc.)

**Output**: Walkthrough comparison table + annotated screenshot sequences as appendix figures.

### 6.2.2 Step-Count Comparison Table

**Hypothesis**: Saturn reduces discrete configuration actions by >80% compared to manual setup.

**Method**: Enumerate every atomic user action for each setup path. An "action" is one of:
- Navigate to URL
- Fill form field
- Click button
- Copy value
- Paste value
- Open terminal
- Type command
- Read/comprehend documentation
- Make a decision (choose plan, select model, pick region)

**Baselines**:
1. **Raw API setup** (OpenAI, Anthropic, or OpenRouter): account creation → API key → client configuration
2. **Aggregator setup** (LiteLLM proxy): install → configure → run → point clients
3. **Local model** (Ollama direct): install → pull model → configure each client
4. **Saturn**: admin runs one command; users do nothing

**Output**: Table with columns: Tool | Navigate | Fill | Click | Copy/Paste | Terminal | Decision | Total

### 6.2.3 Configuration Artifact Count

**Hypothesis**: Saturn eliminates per-user configuration artifacts entirely.

**Method**: For each setup path, count:
- Config files created or modified
- Environment variables set
- API keys managed
- URLs memorized or stored
- Accounts created
- Dependencies installed (by end user, not admin)

**Output**: Table. Saturn row should be zeros for end users, nonzero only for admin.

---

## 6.3 Claim 3: Security Trade-offs

### 6.3.1 STRIDE Threat Model Comparison

**Hypothesis**: Saturn's threat surface is comparable to or smaller than static API key management for the target environment (campus, home, coffee shop).

**Method**: Apply STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) to three configurations:
1. Static API keys (status quo)
2. OAuth/SSO (enterprise alternative)
3. Saturn ephemeral beacons

**For each threat category**: document whether the attack vector exists, its severity, and what mitigation (if any) applies.

**Output**: 6×3 STRIDE matrix table with severity ratings and notes.

### 6.3.2 Ephemeral Key Exposure Window Analysis

**Hypothesis**: Saturn's ephemeral key lifecycle bounds maximum exposure to 10 minutes, compared to unbounded exposure for static keys.

**Method**: Quantitative comparison:
- Saturn: key lifetime = 10 min, rotation interval = 5 min → max exposure = 10 min, expected exposure = 7.5 min
- Static API key: Meli et al. (2019) found 81% of leaked keys never revoked → exposure = ∞
- OAuth token: typically 1 hour, but refresh tokens can be long-lived

**Additional analysis**:
- What can an attacker do with a captured Saturn key in 10 minutes?
- What can they do with a static OpenAI key indefinitely?
- Cost exposure: Saturn can set spending caps; static keys often have none by default

**Output**: Timeline diagram showing key lifecycle. Comparison table of exposure windows.

### 6.3.3 Attack Surface Enumeration

**Hypothesis**: Saturn's attack surface varies by deployment mode but is documented and bounded for each.

**Method**: For each deployment type (local, network, cloud), enumerate:
- Network attack vectors (eavesdropping, spoofing, injection)
- Authentication attack vectors (key theft, replay, brute force)
- Application-level attacks (prompt injection via rogue service, model substitution)
- What mitigations exist in Saturn today
- What mitigations are possible as future work (Kaiser & Waldvogel privacy sockets, Osborn tiered trust)

**Output**: Three-column table (Local | Network | Cloud) with attack vectors and mitigations.

---

## Playwright Walkthrough — Technical Plan

### What to build

A Node.js + Playwright test suite that walks through real service setup flows and captures evidence.

```
evaluation/
├── playwright.config.ts
├── walkthroughs/
│   ├── openrouter-signup.spec.ts    # Full OpenRouter setup
│   ├── litellm-setup.spec.ts       # LiteLLM proxy config
│   ├── ollama-manual.spec.ts       # Manual Ollama client config
│   ├── openwebui-manual.spec.ts    # OWUI manual backend config
│   └── openwebui-saturn.spec.ts    # OWUI with Saturn (zero config)
├── metrics/
│   └── collector.ts                 # Counts steps, screenshots, timing
└── output/
    ├── screenshots/                 # Auto-captured at each step
    ├── step-logs/                   # JSON: action type, timestamp, element
    └── comparison-table.md          # Generated summary
```

### What each spec does

1. **openrouter-signup.spec.ts**: Navigate to openrouter.ai → sign up → verify → dashboard → create key → copy key. Record every click, form fill, page navigation.

2. **litellm-setup.spec.ts**: This one is terminal-based, not browser. Document the steps with shell commands instead. Playwright captures the docs pages for reference.

3. **ollama-manual.spec.ts**: Download page → install steps → then open a client app (e.g. Open WebUI) → manually enter `http://localhost:11434` → select model.

4. **openwebui-manual.spec.ts**: Open WebUI settings → Admin Panel → add connection → fill in URL + API key → save → verify model appears.

5. **openwebui-saturn.spec.ts**: Open WebUI with Saturn plugin installed → open chat → models are already there. Screenshot. Done. The contrast is the point.

### Metrics collector

Each walkthrough calls `collector.record()` at each step:

```ts
type Step = {
  action: 'navigate' | 'click' | 'fill' | 'copy' | 'paste' | 'read' | 'decide' | 'terminal'
  target: string      // button label, field name, URL
  timestamp: number
  screenshot: string  // path to screenshot
  notes?: string      // e.g. "user must know what API key format looks like"
}
```

After all walkthroughs, generate the comparison table automatically.

### Important caveats

- Playwright can't actually create real accounts (CAPTCHA, email verification). For those steps, the walkthrough documents them as manual steps with timing estimates.
- The value is in the *structure* — showing the exact sequence, capturing the UI states, counting the actions. Not in full automation.
- Screenshots become thesis figures (Appendix B or inline in Chapter 6).

---

## Threats to Validity

Must address in evaluation chapter:

- **Internal**: Latency measurements affected by network conditions, mDNS cache state, OS mDNS daemon behavior. Mitigate with high trial counts and cold-start resets.
- **External**: Single-segment LAN only. Saturn doesn't claim to work across subnets (mDNS limitation). State this explicitly.
- **Construct**: Step counts and cognitive walkthrough are expert analysis, not user study. Acknowledge this limits generalizability but note that KLM/CW are accepted HCI methods that don't require IRB.
- **Ecological**: GL.iNet router is one hardware target. Results may differ on other embedded platforms.

---

## Mapping to Existing Section Headers

The thesis currently has these Ch 6 stubs:
- 6.1 Router Deployment Case Study
- 6.2 Application Integration
- 6.3 Configuration Time Comparison

**Proposed restructure**:
- 6.1 Discovery Performance (latency + interop + failover) — maps to Claim 1
- 6.2 Configuration Effort Analysis (cognitive walkthrough + step count + artifact count) — maps to Claim 2
- 6.3 Security Analysis (STRIDE + exposure window + attack surface) — maps to Claim 3
- 6.4 Threats to Validity

This aligns evaluation sections 1:1 with claims, which is cleaner and follows the evaluation.md rubric (every experiment maps to a hypothesis).
