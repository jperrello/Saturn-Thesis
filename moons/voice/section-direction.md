# Section Direction (Author's Intent)
**Source**: Joey's per-section topic guidance document

## Abstract
General overview of each section. Explain the protocol, our integration approach, evaluation results. Acknowledge security flaws and how we address them.

## Introduction
- Open with "too cheap to meter" analogy -- originally from energy, repurposed for AI services
- Joey's origin story: wanted to provision AI access to everyone on campus
- Primary argument for why the paper needs to exist
- Restate contributions (different framing than abstract)

## Background
**Service discovery landscape** (why not these?):
- NetBIOS -- Windows emphasis
- WS-Discovery -- seems modern, maybe Windows emphasis
- UPnP -- complicated, somewhat old (Adam's assessment)
- DLNA -- possibly proprietary

**mDNS coverage** (most space here):
- Mention Avahi and Bonjour
- Explain TXT records and their contents

**AI consumption points** (where text completions are used):
- Hosted chat apps: LibreChat, Open WebUI
- Coding agents with configurable endpoints
- VS Code uses mDNS for discovering debugging targets (precedent)
- Voice typing/transcription: on-device voice model + off-device cleanup model

**DHCP**: Explain how DHCP operates differently on the network stack than Saturn

**Key requirement**: Explain why Saturn was chosen over all these methods

## Design
Topics to cover (not hardcoded sections):
- Goals: what Saturn's architecture achieves
- Audiences: who uses Saturn
- Concepts: Endpoints, Beacons, Priorities, Ephemeral Keys
- Protocol specs: `_saturn._tcp.local`, TXT record details, expected endpoints (`/health`, `/v1/models/list`, `/v1/chat/completions`)
- Architecture decisions

**Security section within design**:
- Two threat models: (1) don't want big corporations getting data, (2) don't trust the sysadmin of office/house

## Implementation
- Explain project progression -- we had a deadline
- **VLC extension**: prove AI can be integrated into non-AI-native apps. VLC plays media; Saturn adds AI services to something that never had them
- **Router**: prove AI provisioning at network level. Everyone on the network gets Saturn services
- **Open Code**: prove Saturn works with coding agents (tool calling, back-and-forth conversation, file editing, codebase knowledge)
- Acknowledge Open Code is natively AI-based; remind reader that VLC shows Saturn isn't just for AI apps

## Evaluation
- Three claims and how we prove them
- Connect claims back to motivations from introduction
- Claims prove Saturn works, benefits society, is worth deploying at scale

## Discussion
- "What happens now" section
- Universities could let students connect to endpoints, charged per-token instead of enterprise subscriptions
- Apps wouldn't need API key setup if Saturn is widely adopted
- Saturn lowers barrier to entry for AI experimentation
- Users may discover AI passively through apps that integrated it via Saturn

## Conclusion
- Only about what the reader has read
- Restate Saturn's contributions, what we proved, why it exists, why it matters
- Future directions
- Primary motivation of the authors one last time
- Probably one short paragraph
