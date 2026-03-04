# Saturn Project History

Chronological record of Saturn's development, drawn from Joey's development notes.

## Fall 2025 — Independent Study (CMPM 297)

**Pre-Oct 2025:** Joey is spending ~$100/month on AI services. Realizes most people can't afford that. Initial idea: demonstrate "Zeroconf AI" — a locally discoverable server implementing the OpenAI API, announced via mDNS. Course: CMPM 297 independent study under Adam Smith. 14 hours solo + 1 hour weekly with advisor.

**Oct 9, 2025 — Inception.** OpenAI launches "connected apps" (ChatGPT plugins v2). Joey sees the contrast: OpenAI connects apps to models, Saturn brings models to apps. Early references: RouteLLM, OpenRouter, FastAPI.

**Oct 15, 2025:** First GitHub repo created: `jperrello/Zeroconf-AI`.

**Oct 22, 2025 — Protocol defined.** Meeting with Adam crystallizes the protocol:
- Lookup mDNS: `_zeroconfai._tcp._local`
- For each result: `GET /health`, `GET /v1/models`, `POST /v1/chat/completions`
- Any language with mDNS + HTTP can participate
- Decided on multiple specialized servers (gemini, ollama, fallback) and clients (simple_chat, local_proxy, playlist_generator)
- At least one non-Python example required

**Oct 28, 2025:** Built three servers (gemini_proxy, ollama_proxy, fallback with "dont_pick_me" model). Client discovers multiple servers with multiple models. Started simple_chat.py — most barebones implementation.

**Oct 29, 2025:** Started work on server priorities. Tasks: get Jan/5ire using ollama, update local_proxy_client to aggregate models.

**Nov 5, 2025:** Meeting. Explored Jan.ai issues, OpenRouter API docs.

**Nov 19, 2025 — Named "Saturn."** Project renamed from ZeroconfAI to Saturn. Service type becomes `_saturn._tcp.local`. VLC "Chat with Saturn" extension demoed — roasts your media taste using discovered AI. Brainstormed integrations: IDEs (Cline, Cursor, Copilot), Open WebUI, note-taking apps, Home Assistant, desktop AI chat apps, workflow automation, content creation tools.

**Nov 26, 2025 — Open WebUI integration.** Saturn function for OWUI uses zeroconf library, discovers models on launch. Reddit posts on r/RASPBERRY_PI_PROJECTS and r/OpenWebUI. Community replies point to LiteLLM and Requesty — routing-focused, not discovery-focused. Also working on MiniStS integration for another class.

**Dec 3, 2025:** Removed failover claim from OWUI function. Started looking for reading committee member. Requirements: interested in networking + GenAI.

**Dec 11, 2025:** Ram is on board as reading committee member. Will meet at start of next quarter. No fixed requirements for the paper — at discretion of reading committee.

**Dec 12, 2025 — Beacons formalized.** Saturn "beacons" — periodic mDNS announcements with ephemeral API keys. Inspired by DeepInfra's scoped JWT system. Keys distributed via mDNS TXT records, expire after minutes, rotate continuously. Like Kerberos tickets for AI access. Note: mDNS strings can't exceed ~250 characters.

**Dec 15, 2025:** Formal term adopted: "ephemeral credential distribution."

## Winter 2026 — Thesis Quarter (CMPM 297 + CSE courses)

**Jan 6, 2026:** New quarter. Courses: CMPM 280G, CMPM 297 (5u independent study), CSE 247b, CSE 240 (AI). Objective: prepare MS thesis draft, develop app integrations, run on-campus experiments. Framing discussion: Saturn operates at Layer 7 technically but provides Layer 5 (Session) functionality semantically — "Layer 5.5."

**Jan 13, 2026 — Router running.** Saturn on GL-MT300N-V2 (Mango): 580MHz MIPS processor. Cross-compiled Go binary. Key rotation working on router. Initial issues: dns-sd clients couldn't find beacon, zeroconf library clients found it but wouldn't start. Fix: passed hostname instead of inet_ntoa. Meeting: discussed ANS (GoDaddy agent naming), Google A2A protocol, UCSC eduroam IoT device registration.

**Jan 20, 2026 — Campus experiment.** Tested on UCSC networks. Eduroam and UCSC-guest block multicast (AP isolation) — mDNS name resolution fails. Non-IT users can't provision Saturn on institutional networks; IT-level deployment needed. Mango router's LAN side works. OpenRouter beacon successful: Adam on Mango network discovered Saturn service, got temporary API key, made LLM request directly to OpenRouter via HTTPS.

**Jan 25, 2026 — Soft-float fix.** Hard-float vs soft-float ABI mismatch on Mango router. Changed toolchain from `mipsel-linux-musl-cross` to `mipsel-linux-muslsf-cross`. Result: ELF 32-bit LSB, MIPS32 rel2, interpreter `/lib/ld-musl-mipsel-sf.so.1`. Final binary: 2.3MB.

**Jan 27, 2026 — LuCI Web UI complete.** Router admin interface done: configure name, priority, backends, API keys, beacon mode. Beacon vs HTTP confusion resolved — all router services need HTTP for health endpoint, but beacon mode distributes ephemeral keys instead of proxying requests.

**Jan 31, 2026 — Open Code integration.** Forked Open Code (coding agent) to discover AI via Saturn. Spotted that almost all bundled providers use AI SDK npm packages. Created `ai-sdk-provider-saturn`. Struggled with model list refresh and streaming [DONE] signal. Discovered that true integration requires upstream AI SDK support, not per-app plugins.

**Feb 1-2, 2026:** Continued Open Code debugging. Saturn Python package: API keys stored in `~/.saturn/.env`. Irony noted: beacon mode is more secure than stored keys, but provisioning key still needed.

**Feb 10, 2026:** Meeting. Outlined thesis structure: Background (service discovery alternatives, mDNS, Bonjour/Avahi, TXT records, DHCP comparison), Design (goals, audiences, concepts, protocol specs, architecture decisions), Security (threat models: anti-corporate data collection vs. anti-sysadmin trust). Four audience types: inference provider, IT person, end user, app developer.

**Feb 16, 2026:** Built academic-writing skill for Claude Code. Two-part system: general principles (evaluable rules) + section-specific reference files. Wrote general principles with CC assistance.

**Feb 17, 2026:** Meeting. Showed skill, moons, draft. Discussed argumentation theory, keystroke-level model for evaluation. Post-meeting: found only 217 edges in knowledge graph. Launched agent team to propose new edges. Result: 329 edges.

**Feb 19, 2026:** Bloom-inspired blind evaluation strategy. Prevent evaluating agent from gamifying results by making it blind to Saturn's identity and evaluation metrics. Decided: traditional systems evaluation (latency, interop, cognitive walkthroughs, STRIDE) doesn't need Bloom; agent evaluation does.

**Feb 24, 2026:** Meeting. Major topics: Nielsen's usability heuristics, cognitive walkthrough with three audience levels (sysadmin, app dev, end user), AI writing acknowledgment requirements (prominent human-written explanation + appendix details). Claims refinement: C1 is the most important; others are subclaims. Evidence matters more than initial strength.

**Mar 3, 2026:** Meeting. Draft acknowledgment written (100% by Joey). Style decisions: use "I" not "the author," active voice, explain "we." Create llms.txt for docs site. Cognitive walkthrough complete for all three audiences. Claim 1 has three requirements: (1) service can be found with no config, (2) discovery info is enough for a working API call, (3) independent implementations consume the same protocol. Ralph loop discussed — OK if text sounds AI-generated as long as it's worth reading.

**Mar 3, 2026 — RALPH loop v2.** AI detection loop (runs 1–8) abandoned. Detection scores were noisy and the strategy produced no reliable signal — chasing detector scores led to arbitrary rewrites. Useful writing principles distilled from those eight runs (see `rewrite_notes.md` Run 0). Replaced with RALPH v2: rubric-based structural revision using a six-criterion academic rubric (structural completeness, contribution vs. claim, ordering, design intent, trade-off honesty, value density). Architecture: `ralph.sh` runs Claude in a headless loop with `--dangerously-skip-permissions`. Each invocation is a fresh session — reads state from `rewrite_notes.md`, spawns a read-only grader subagent (`.claude/agents/grader.md`), revises the worst-scoring section, logs results, exits. Filesystem is the only persistence between runs. One grade→revise cycle per invocation.
