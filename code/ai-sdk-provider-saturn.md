# ai-sdk-provider-saturn

## What It Is

An npm package that implements Vercel's AI SDK `ProviderV3` interface, resolving endpoint configuration, authentication, and model routing entirely at runtime from mDNS broadcasts. A developer writes:

```typescript
import { saturn } from 'ai-sdk-provider-saturn';
const result = await generateText({ model: saturn('gpt-4o'), prompt: '...' });
```

No API key. No endpoint URL. No environment variable. The import itself starts mDNS discovery (`index.ts:107`), and by the time the first request fires, the provider has already resolved which services on the network advertise that model, sorted them by priority, and selected the best one.

Includes a self-contained Eliza chatbot mock server (`mock-server.ts`) that announces via mDNS, rotates ephemeral keys, and serves OpenAI-compatible endpoints — a complete Saturn loop in one package.

## Why It Exists

The core Saturn protocol solves service *discovery*, but discovery alone is insufficient if applications cannot consume what is discovered. Most AI-enabled applications in the JavaScript/TypeScript ecosystem build on Vercel's AI SDK, which abstracts model providers behind a standard interface. Today, every AI SDK provider (OpenAI, Anthropic, Google, etc.) requires the developer to hardcode an API key and endpoint URL.

`ai-sdk-provider-saturn` eliminates both requirements by resolving all provider configuration from the network at runtime.

**Evidence:**

1. **Syed et al. (2025)** document the AIaaS status quo: each application must independently manage API keys, accounts, and endpoint configuration. This package collapses that per-application burden to a single network-level concern — the admin runs a beacon, and every application on the network inherits AI capabilities.

2. **The code itself** demonstrates the zero-config property. The entire public API is a single factory export:
   ```typescript
   // index.ts:107
   export const saturn = createSaturn();
   ```
   `createSaturn()` instantiates `SaturnDiscovery`, which immediately begins sending PTR queries for `_saturn._tcp.local` via the `multicast-dns` npm library (`discovery.ts:4`). No constructor arguments are required. The developer's only action is `import`.

3. **Guttman (2001)** articulated the zero-config vision: "enable direct communications between two or more computing devices via IP" with no configuration. This package extends that vision from device-level pairing to SDK-level AI integration — a developer adds one dependency, and their application communicates with whatever AI services the network provides.

## Who It Is Designed For

### Primary: Admins Who Are App Developers

These are people building applications that consume AI — a chat interface, a code assistant, an internal tool. Today they must choose a provider, obtain an API key, manage that key's lifecycle, and hardcode the endpoint. With `ai-sdk-provider-saturn`, the developer delegates all of that to the network. Their app works on any network that has Saturn services, with whatever models those services provide.

**Evidence:**

1. **The open-source developer problem** is the direct motivation. The thesis context states: "Open source developers struggle with this; they might want to add AI features to their applications but cannot justify forcing users to bear API costs or subscription complications." This package is the technical answer: an open-source app can ship with `ai-sdk-provider-saturn` as a dependency and gain AI features on any Saturn-enabled network without bundling API keys.

2. **Meli et al. (2019)** found that static API key leakage is "pervasive — affecting over 100,000 repositories," with 81% of leaked secrets never removed. Apps built on this provider never write a key to source code — keys are discovered at runtime from mDNS TXT records and rotated automatically. The entire leakage class is eliminated by design, not by developer discipline.

### Secondary: Consumers (Indirectly)

A consumer never touches this package. But they benefit because the applications they use — built by the admins above — discover AI services without the consumer needing an account, a credit card, or an API key.

**Evidence:**

1. **Kim & Reeves (2020)** trace mDNS back to its origin as printer discovery. The consumer experience with Saturn mirrors Bonjour: the user opens an app, the app finds AI on the network, and the user gets results. They never knew mDNS was involved. This is the "printer test."

2. **The mock server example** (`mock-server.ts`) demonstrates the full consumer-facing loop: a Saturn service announces itself, rotates keys every 60 seconds, and serves chat completions. The `basic.ts` example connects and gets responses. At no point does the example configure an endpoint, paste a key, or select a provider. The consumer path is: open app, get AI.

## How It Supports the Thesis Claims

### Claim 1 — Zero-Config AI Provisioning Is Feasible

This package is a working implementation of Saturn discovery in a second language ecosystem (TypeScript), alongside the core Python package. It uses the `multicast-dns` npm library to query `_saturn._tcp.local` (`discovery.ts:4`), parse TXT record metadata, and maintain a live service registry — the exact same protocol the Python implementation uses.

**Evidence:**

1. **Siljanovski et al. (2014)** established that mDNS/DNS-SD adapts to new domains: printers, then IoT, now AI. This package is concrete proof of that extensibility — the same `_saturn._tcp.local` service type works identically whether queried from Python's `zeroconf` library or JavaScript's `multicast-dns` package.

2. **Cross-language interoperability in the code.** The `SaturnDiscovery` class (`discovery.ts`) handles PTR, SRV, TXT, and A/AAAA records in the same sequence as the Python implementation. A Python-based Saturn beacon and a TypeScript-based Saturn provider interoperate without any bridging layer. This validates the Session 2 clarification: "Saturn is a protocol, not a language-specific implementation. Any language that can do mDNS can participate."

3. **Siddiqui et al. (2012)** describe zero-config foundations where services are discovered "with little end-user intervention." The `SaturnDiscovery` class embodies this: it sends periodic PTR queries (`discovery.ts:69-73`), follows up with SRV+TXT queries for each instance, resolves hostnames via A records, and maintains a live registry — all without a single configuration parameter.

### Claim 2 — Network-Provisioned AI Reduces Total Configuration Effort

**Evidence:**

1. **Step-count comparison from the code.** Traditional AI SDK setup: create account, generate API key, store in `.env`, install SDK, configure provider with key + endpoint, select model, handle key rotation. Saturn: `npm install ai-sdk-provider-saturn`, `import { saturn }`, use. The developer's configuration effort drops to zero; the admin's one-time beacon setup serves N developers.

2. **Meli et al. (2019)** found that the best secret-scanning tools catch only 25% of leaked keys, and "all mitigations act too late." Saturn eliminates the need for secret scanning entirely — there are no secrets in the developer's codebase. The `SaturnChatLanguageModel` (`model.ts:131`) reads the ephemeral key from the discovery registry at request time. The key was never in a file, never in an environment variable, never in a repository.

3. **Guttman (2001)**, quoting RFC 1122: "It would be ideal if a host implementation of the Internet protocol suite could be entirely self-configuring." This package achieves that for AI: the provider self-configures from network announcements without any host-side configuration files.

### Claim 3 — Security Trade-offs Are Known and Addressable

**Evidence:**

1. **Ephemeral key rotation in the code.** When the model layer receives a 401 (expired key), it calls `discovery.waitForKeyRefresh()` (`model.ts:137-142`), which sends a targeted TXT query to fetch the latest rotated key, then retries the request. Applications automatically participate in Saturn's credential rotation without developer intervention. The mock server demonstrates this with configurable rotation intervals (default 60 seconds, `mock-server.ts:20`).

2. **Kaiser & Waldvogel (2014a)** identified passive eavesdropping as the primary threat model for mDNS-SD: "every machine in the same network will automatically receive all the announcement traffic." The `ai-sdk-provider-saturn` package operates within this known threat boundary — ephemeral keys are broadcast in TXT records, which means any device on the network can read them. This is a deliberate trade-off for the target environment (campus WiFi, homes, offices), not an oversight.

3. **The circuit breaker pattern** (`retry.ts`) implements Martin Fowler's Circuit Breaker: after 3 consecutive failures to a service, the circuit trips open and requests route to the next-priority service. After a 30-second cooldown, one probe request tests recovery. Combined with priority-based failover across all discovered services (`model.ts:208-230`), this provides resilience against both service failures and potentially compromised endpoints — a service that consistently returns errors is automatically deprioritized.

## Thesis Chapter Mapping

| Chapter | Relevance |
|---------|-----------|
| Ch. 3 (Design) | Demonstrates Saturn's beacon protocol consumed from the client side. The provider only *reads* mDNS announcements — no API traffic flows through the announcer. Validates the beacon vs. proxy distinction. |
| Ch. 4 (Implementation) | Client-side integration pattern showing how unmodified AI SDK applications gain Saturn capabilities through a provider swap. Cross-platform mDNS via `multicast-dns` npm package. |
| Ch. 5 (Scenarios) | The Eliza mock server is a self-contained scenario: mDNS announcement, key rotation, OpenAI-compatible API, discovery, authenticated request, response. |
| Ch. 6 (Evaluation) | Step-count comparison: traditional provider setup vs. Saturn provider setup. Measurable reduction in configuration effort. |
| Ch. 7 (Discussion) | Ephemeral key broadcast trade-off. Circuit breaker as mitigation for unreliable/hostile services. Open-source developer access implications. |
