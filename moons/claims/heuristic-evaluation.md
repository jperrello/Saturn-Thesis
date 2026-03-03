# Heuristic Evaluation — Nielsen's Ten Usability Heuristics Applied to Saturn

## Framework

Jakob Nielsen's ten usability heuristics (Nielsen 1994, updated 2024) are broad rules of thumb for interaction design. Unlike the cognitive walkthrough (Wharton 1994), which traces step-by-step task completion, heuristic evaluation assesses how well an interface communicates across ten recognized dimensions. The walkthrough measured *how many steps*; the heuristic evaluation assesses *how well the interface communicates*.

Applied to Saturn's three-persona model (sysadmin, developer, end user), the evaluation surfaces three categories: strengths, honest trade-offs, and acknowledged limitations.

## Strengths (supports V1, V2)

### H1 — Visibility of System Status
Servers appear on the network via mDNS advertisement. Logs show registration of addresses, ports, and service names when creating Saturn services. For end users, visibility is invisible by design — the system works without needing to be seen. The sysadmin and developer see status through `dns-sd -B` or the router dashboard.

### H5 — Error Prevention
Saturn auto-assigns host address, port number, priority, and failover behavior. Defaults to other available services on failure before erroring. This is a mix of failover (preventing the error from reaching the user) and error message (when no fallback exists). Slips (unconscious errors from inattention) are prevented because there are no URLs or keys to mistype.

### H6 — Recognition Rather Than Recall
`discover()` presents available services — no URLs, keys, or model strings to recall. The router dashboard shows advertised services to administrators. This is the usability counterpart to Claim 2's step-count reduction: Saturn eliminates the recall burden that drives traditional setup complexity. Instead of remembering `https://openrouter.ai/api/v1` and `sk-or-v1-abc123...`, users call one function and get a list.

### H7 — Flexibility and Efficiency of Use
Python package for power users who want programmatic control. Traditional API key bypass still available — Saturn doesn't lock anyone in. Clean opt-out path: stop using `discover()` and plug in your own key. See cognitive walkthrough opt-out scenarios.

## Trade-offs (supports V2, V3 framing)

### H2 — Match Between System and Real World
"Beacon" and "proxy" are confusing for sysadmins. They come from Saturn's internal architecture rather than terms sysadmins already use. Developer and end-user audiences are less affected — developers see `discover()` and standard OpenAI-compatible endpoints; end users see nothing. Sysadmin terminology is the weakest point in Saturn's real-world matching.

### H3 — User Control and Freedom
Developers can pick specific servers by name when calling `discover()`. Sysadmins stop services with ctrl-c or one click in the router dashboard. End users on the network have no control over which service they get (priority-based routing). Control exists but is role-dependent — strongest for sysadmins, weakest for end users.

### H4 — Consistency and Standards
TXT record schema drifts across implementations:
- **Core 4 fields** (universal across all implementations): `version`, `deployment`, `api_type`, `priority`
- **TypeScript-only field**: `auth` — present in ai-sdk-provider-saturn but absent from Python core and Rust router
- **Missing from Rust**: `capabilities`, `cost`, `context` — fields defined in the Python core but not implemented in saturn-router
- Developer-facing APIs need cross-implementation consistency verification

This is a concrete interoperability concern that qualifies Claim 1's R3 (cross-implementation interoperability). See A8 (TXT schema completeness).

## Limitations (future work)

### H8 — Aesthetic and Minimalist Design
TXT record schema inconsistency is both an aesthetic issue (different implementations advertise different fields) and a protocol-reliability issue (clients can't depend on optional fields being present). The `_saturn._tcp.local.` service type itself is specialist-facing — meaningful to developers but opaque to anyone else. Not a user-facing problem since end users never see it.

### H9 — Help Users Recognize, Diagnose, and Recover from Errors
Weak. Saturn currently says "service not available" and "check network." No debugging guidance for why discovery failed. No guide for discovering a server when one should be present. Error recovery is the clearest usability gap. Future work: diagnostic mode that checks multicast reachability, lists nearby services, and suggests fixes.

### H10 — Help and Documentation
Documentation site (jperrello.github.io/Saturn/) and PyPI package cover sysadmin, developer, and end-user audiences. Mainly aimed at the first two. End-user documentation is thin because end users aren't expected to interact with Saturn directly — but when something goes wrong, they have nowhere to turn.

## Cross-references

- **A3**: Consumer path is zero-config → H6 (recognition) confirms why
- **A8**: TXT schema completeness → H4 (consistency) identifies drift
- **A11**: Cognitive walkthrough step counts → H6 provides qualitative complement
- **A12**: 79% app developer reduction → H5 (error prevention) + H6 (recognition) explain mechanism
- **B5**: AP isolation → not a heuristic finding, but H9 (error recovery) would need to handle this failure case
- **B6**: TXT schema drift → H4/H8 finding, new barrier

## Connection to Claims

- **V1** (feasibility): H1 visibility and H6 recognition confirm that the zero-config property is not just technically present but usably accessible
- **V2** (reduced configuration): H5 error prevention and H6 recognition explain *why* step counts drop — Saturn eliminates recall-dependent steps and prevents configuration errors
- **V3** (security honesty): The three-bucket pattern (strengths / trade-offs / limitations) mirrors Claim 3's framing. Saturn's usability strengths are real, its trade-offs are known, and its limitations are documented
