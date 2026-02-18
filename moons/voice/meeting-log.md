# Meeting Log and Design Decisions

Condensed from "General Notes for Saturn.md" (Oct 2025 - Jan 2026).
Content already in thesis_context.md or thesis.tex is omitted.

## Oct 9, 2025 - Project Inception
- OpenAI launches connected apps in ChatGPT; Joey sees this as validation of Saturn's opposite approach: "Instead of connecting apps to models, we are bringing AI to the apps."
- Karpathy tweet referenced as alignment with vision.

## Oct 15, 2025
- GitHub repo created: https://github.com/jperrello/Zeroconf-AI
- Adam pushes Joey to think about multi-provider, multi-service, service-down scenarios.
- Led to singleton service discovery design: one process maintains registry, handles add/remove/update.

## Oct 22, 2025 - Protocol Definition Meeting
Key protocol decisions made:
1. Lookup: `_zeroconfai._tcp._local` returns IP:port pairs with priority
2. Health: `http://$IP:$PORT/health`
3. Models: `http://$IP:$PORT/v1/models`
4. Chat: `http://$IP:$PORT/v1/chat/completions`
5. Monitor health periodically; re-discover via mDNS periodically.

Cross-language requirement: any language with mDNS + HTTP can participate.

Server specialization decided:
- gemini_proxy_server.py (Gemini API)
- ollama_proxy_server.py (local models)
- fallback_server.py ("dont_pick_me" model)

Client specialization decided:
- simple_chat_client.py (fewest lines, auto-select first model)
- local_proxy_client.py (for apps that don't know Saturn — route through localhost)
- playlist_generator_client.py (non-chat use case)

## Oct 29, 2025
- Started work on priorities for servers.
- TODO: Install 5ire or Jan, get it to use ollama directly.
- Update local_proxy to aggregate models across all local services.

## Nov 5, 2025
- Links shared: Jan GitHub issues, OpenRouter API docs.

## Nov 19, 2025 - Naming and VLC Demo
- Project renamed to **Saturn**.
- VLC plugin demonstrated: "Chat with Saturn" menu option, launches bridge Python script.
- VLC demo goal: demonstrate something only possible by combining VLC data with AI (e.g., "roast my personality" based on open files).
- Idea: pitch fellow CSE MS students on integrating Saturn into another app.

Integration targets identified:
- IDEs: Cline/Roo, Cursor/Windsurf, GitHub Copilot
- Open WebUI, Jan.ai, LM Studio, GPT4ALL, AnythingLLM
- Note apps: Obsidian, Logseq, Joplin
- Home Assistant, N8n, OBS, Blender, Krita

## Nov 26, 2025
- OWUI integration working with zeroconf library.
- VLC roast extension created.
- Community posts: r/RASPBERRY_PI_PROJECTS, r/OpenWebUI.
  - Feedback pointed to LiteLLM and Requesty (routing-focused, not discovery-focused).
- Ollama integration discussion: https://github.com/ollama/ollama/issues/10283
- Eduroam interest but no contact found; campus deployment may be best path.
- Working on MiniStS integration (class project using OpenAI API calls).

## Dec 3, 2025
- Remove failover claim from OWUI function's valves.
- Reading committee discussion: need someone interested in networking + GenAI.

## Dec 12, 2025
- Report polishing: added footnotes, removed vague language, anchored in others' opinions.
- **Beacon concept formalized**: servers that periodically announce and provide ephemeral API keys. Keys valid while on network, expire when user leaves.
- DeepInfra scoped JWT reference: https://deepinfra.com/docs/advanced/scoped_jwt
  - Keys expire in minutes, broadcast via mDNS TXT records.
  - mDNS string limit: ~250 chars before truncation.
- "Ephemeral credential distribution" = formal name for beacons.

## Jan 6, 2026 - Quarter Planning
Joey's courses: CMPM 280G, CMPM 297 (independent study), CSE 247b, CSE 240.

Independent study objectives:
- Prepare MS thesis draft on Saturn AI service discovery protocol.
- Develop app integrations for breadth/depth of impact.
- Run on-campus connectivity experiments.

Architecture taxonomy decided:
- **Clients**: discover servers
- **Servers**: announce endpoints they offer
- **Beacons**: announce temporary access to third-party services (mDNS only, no HTTP)

Hardware targets for embedded deployment:
- Raspberry Pi 5
- Low-end WiFi router (Adam's Ubiquiti EdgeRouter X, GL.iNet routers)

Web admin interface spec: set name, priority, backends, API keys, hours, prompt injection, rate limits, beacon mode.

OSI layer analysis (from Claude conversation):
- Saturn technically at Layer 7 (mDNS, HTTP) but semantically provides Layer 5 (session coordination).
- Beacon pattern parallels Kerberos: distribute time-limited credentials for session establishment.
- "Saturn provides Session-layer service discovery using Application-layer protocols."

## Jan 13, 2026 - Router Progress
- Router has 580MHz MIPS processor; cross-compile on laptop, deploy binary via SCP.
- dns-sd clients found beacon; zeroconf library clients had issues (fixed by passing hostname).
- Key properly rotates on router.

Links shared:
- ANS (Agent Name System): https://www.agentnameregistry.org/
- A2A (Agent-to-Agent): https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/
- UCSC IoT wireless: https://its.ucsc.edu/services/network-and-infrastructure/network-and-connectivity-management/ucsc-devices-wireless-service/
- Room E2-256 for experiments.

TODOs: on-campus mDNS reachability experiment, learn OpenWRT packaging (LuCI UI), OpenRouter beacon with auto key rotation. A2A put on back burner.

## Jan 20, 2026 - On-Campus Experiment Results
Key findings:
1. **Eduroam and UCSC-guest block multicast traffic** (AP isolation). Ping and HTTP work, but mDNS name/service resolution fails. Non-IT users cannot provision Saturn; IT-level deployment needed.
2. **Mango router serves LAN side only** (not WAN side) — expected behavior for current Go code.
3. **OpenRouter beacon worked**: Adam on Mango's network discovered Saturn services, found temporary API key, used it for HTTPS request directly to OpenRouter (Mango couldn't decode traffic).
4. **LuCI confusion**: "openrouter" referred to both local proxy and key distribution. Roles need disambiguation.

## Jan 25, 2026 - Soft-Float Fix
Hard-float vs soft-float ABI mismatch on GL-MT300N-V2 (Mango router):
- Router uses soft-float MIPS (`ld-musl-mipsel-sf.so.1`)
- Original toolchain produced hard-float binaries
- Fix: changed cross-compile toolchain from `mipsel-linux-musl-cross.tgz` to `mipsel-linux-muslsf-cross.tgz`
- Result: 2.3MB statically-linked binary, correct interpreter

## Jan 27, 2026 - LuCI Complete
- LuCI UI and Saturn beacon on router complete.
- Beacon vs HTTP confusion resolved: all router services need HTTP for health endpoint, but beacon mode distributes keys instead of proxying requests.
- AP isolation research ongoing; looked into Bonjour gateway things.

## Jan 31, 2026 - Open Code Integration
- Testing Saturn with Open Code (coding agent).
- Models list doesn't update when new providers join while Open Code is running.
- Multiple servers only show one provider if Open Code started after them.
- Bug: after first response, messages queue instead of sending.

## External Links Worth Preserving
- RouteLLM: https://github.com/lm-sys/RouteLLM
- mDNS Options (Homebridge): https://github.com/homebridge/homebridge/wiki/mDNS-Options
- OpenRouter: https://openrouter.ai/
- 5ire app: https://github.com/nanbingxyz/5ire
- Jan.ai: https://www.jan.ai/
- Krita plugin docs: https://docs.krita.org/en/user_manual/python_scripting/install_custom_python_plugin.html
- Clad Labs: https://www.cladlabs.ai/blog/introducing-clad-labs
- DeepInfra scoped JWT: https://deepinfra.com/docs/advanced/scoped_jwt
- UCSC academic calendar: https://registrar.ucsc.edu/calendars-resources/academic-calendar/
- Cross-compile Rust for MIPS: https://kauruus.github.io/posts/2023/10/09-cross-compile-rust-program-for-mipsel/
- Rust soft-float issue: https://github.com/rust-lang/rust/issues/34922
- InCommon: https://incommon.org/solutions/
