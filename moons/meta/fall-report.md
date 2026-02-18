# Fall 2025 Quarterly Report

**Date:** Fall 2025 (submitted Dec 2025)
**Type:** Progress report to committee

## Key Points

- Opens with "too cheap to meter" analogy (Lewis Strauss 1954 / atomic energy) — draws parallel to AI cost optimism today
- Frames the cost problem: $20/mo chatbot subscriptions, o1-pro at $150/M input tokens, per-app API keys
- Open source devs "cannot justify forcing users to bear API costs"

## Saturn Description (as of Fall 2025)

- Zero-configuration service discovery using mDNS + DNS-SD
- Advertises OpenAI-compatible AI backends on LAN under `_saturn._tcp.local`
- Server/client split:
  - **Servers**: encapsulate provider config, query /v1/models, handle chat/completions, register via DNS-SD. IT admin responsibility.
  - **Clients**: discover servers, store routing info. App developer responsibility.
- Bonjour printer analogy used as primary explanation

## Prior Work Noted

- Ollama community requests existed but "none gained traction"
- OpenWebUI has zero-config but requires Ollama on same machine
- LiteLLM and Requesty focus on LLM routing (cost optimization), not discovery
- "I struggled to find any implementation as extensive as Saturn"

## Implementations Mentioned

- Proxy client to Jan (chat UI)
- VLC extension ("roasts user's media taste")
- OpenWebUI function (chat with discovered models on launch)
- Discovery via OS mDNS commands or Python Zeroconf package

## Tone

First-person, accessible, non-academic. More narrative than the thesis itself. Good source for the "voice" of the project motivation.
