# AI SDK Provider Saturn
**Source**: code/ai-sdk-provider-saturn.md
**Claims**: Claim 1 (cross-language interop), Claim 2 (zero developer config), Claim 3 (circuit breaker, auto key refresh)

## Source Files
- [`src/index.ts`](https://github.com/jperrello/Saturn/blob/main/ai-sdk-provider-saturn/src/index.ts) — provider factory export, mDNS discovery init
- [`src/discovery.ts`](https://github.com/jperrello/Saturn/blob/main/ai-sdk-provider-saturn/src/discovery.ts) — PTR/SRV/TXT query logic, service registry
- [`src/model.ts`](https://github.com/jperrello/Saturn/blob/main/ai-sdk-provider-saturn/src/model.ts) — chat language model, ephemeral key refresh, priority failover
- [`src/retry.ts`](https://github.com/jperrello/Saturn/blob/main/ai-sdk-provider-saturn/src/retry.ts) — circuit breaker pattern
- [`src/types.ts`](https://github.com/jperrello/Saturn/blob/main/ai-sdk-provider-saturn/src/types.ts) — shared type definitions
- [`src/helpers.ts`](https://github.com/jperrello/Saturn/blob/main/ai-sdk-provider-saturn/src/helpers.ts) — endpoint routing, provider extraction, IP detection
- [`src/logger.ts`](https://github.com/jperrello/Saturn/blob/main/ai-sdk-provider-saturn/src/logger.ts) — logging interface and factories
- [`src/mock-server.ts`](https://github.com/jperrello/Saturn/blob/main/ai-sdk-provider-saturn/src/mock-server.ts) — ELIZA mock with mDNS + key rotation
- [`test/index.test.ts`](https://github.com/jperrello/Saturn/blob/main/ai-sdk-provider-saturn/test/index.test.ts) — unit tests (node:test)
- [`test/failover-test.ts`](https://github.com/jperrello/Saturn/blob/main/ai-sdk-provider-saturn/test/failover-test.ts) — manual failover scenario test
- [`test/restart-scenario.ts`](https://github.com/jperrello/Saturn/blob/main/ai-sdk-provider-saturn/test/restart-scenario.ts) — automated 3-phase restart/re-discovery test
- [`examples/basic.ts`](https://github.com/jperrello/Saturn/blob/main/ai-sdk-provider-saturn/examples/basic.ts) — generateText + streamText usage
- [`examples/discovery.ts`](https://github.com/jperrello/Saturn/blob/main/ai-sdk-provider-saturn/examples/discovery.ts) — service inspection and routing order

## What It Is

An npm package (v0.1.4, MIT) implementing Vercel's AI SDK `ProviderV3` interface. It resolves endpoint configuration, authentication, and model routing entirely at runtime from mDNS broadcasts. The package contains 8 source files, depends on `@ai-sdk/provider` ^3.0.7, `@ai-sdk/provider-utils` ^3.0.0, and `multicast-dns` ^7.2.5 (a pure JavaScript mDNS implementation with no native dependencies). Built with tsup targeting Node 18+ ESM output.

A developer writes:

```typescript
import { saturn } from 'ai-sdk-provider-saturn';
const result = await generateText({ model: saturn('gpt-4o'), prompt: '...' });
```

No API key. No endpoint URL. No environment variable. The default export `export const saturn = createSaturn()` starts mDNS discovery on import. By the time the first request fires, the provider has resolved which services advertise that model, sorted them by priority, and selected the best one.

The package also includes a self-contained ELIZA chatbot mock server (`mock-server.ts`) that announces via mDNS, rotates ephemeral keys on a configurable interval, and serves OpenAI-compatible endpoints -- a complete Saturn loop in one package, runnable via `npx saturn-mock-server`.

## Implementation Details

### Provider Factory: `createSaturn()`

`createSaturn()` accepts `SaturnProviderSettings` and returns a `SaturnProvider` (extends `ProviderV3`):

```typescript
interface SaturnProviderSettings {
  discoveryTimeout?: number;          // ms to wait for initial discovery (default: 3000)
  logger?: SaturnLogger;
  logLevel?: LogLevel;
  maxRetries?: number;                // per-endpoint retry attempts
  retryDelay?: number;                // ms between retries
  circuitBreakerThreshold?: number;   // failures before tripping (default: 3)
  circuitBreakerResetTimeout?: number; // ms cooldown before half-open probe (default: 30000)
  enableHealthChecks?: boolean;       // pre-flight /v1/health checks
  healthCheckTimeout?: number;
  activeHealthCheckInterval?: number; // periodic background health checks
  onServiceDiscovered?: (service: DiscoveredService) => void;
  onServiceRemoved?: (serviceName: string) => void;
  onServiceUnhealthy?: (service: DiscoveredService) => void;
  // Direct mode: bypass discovery, connect to a known endpoint
  serviceEndpoint?: string;
  serviceName?: string;
  serviceEphemeralKey?: string;
}
```

**Behavior:**
1. Creates a `SaturnDiscovery` instance and a `ServiceCircuitBreaker`
2. Normal mode (no `serviceEndpoint`): calls `discovery.start()` to begin mDNS listening
3. Direct mode (`serviceEndpoint` set): skips discovery, constructs a synthetic `DiscoveredService`
4. Returns a callable provider: `saturn('model-id')` returns a `LanguageModelV3`
5. Implements `ProviderV3`: `provider.languageModel()` works; `provider.embeddingModel()` and `provider.imageModel()` throw
6. `provider.getDiscovery()` exposes the underlying `SaturnDiscovery` instance
7. `provider.destroy()` stops the mDNS listener

### mDNS Discovery: `SaturnDiscovery`

**Library:** `multicast-dns` ^7.2.5 — pure JS, no native dependencies
**Service type:** `_saturn._tcp.local`

**Internal state:**
- `services: Map<string, DiscoveredService>` keyed by service name
- `mdns` socket instance
- Intervals: `queryInterval` (5s re-query), `cleanupInterval` (15s staleness sweep), optional `healthCheckInterval`

**Discovery chain:**

| Record | Purpose | Data Extracted |
|--------|---------|----------------|
| PTR | Browse: "what services exist?" | Instance name; triggers SRV+TXT follow-up queries |
| SRV | Location: "where is this service?" | `host` (target), `port`; constructs `endpoint = http://{host}:{port}/v1` |
| TXT | Metadata: "what does this service have?" | See TXT fields below |
| A/AAAA | IP resolution | Replaces hostname with IP address, re-fires `onServiceDiscovered` |

**TXT record fields (`parseTxtRecords()`):**

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `priority` | number | 50 | Routing priority (lower = preferred) |
| `ephemeral_key` | string | '' | Current authentication key |
| `auth` | 'none' \| 'psk' \| 'bearer' | 'none' | Authentication type |
| `capabilities` | string[] | [] | Comma-separated: chat, code, vision |
| `cost` | 'free' \| 'paid' \| 'unknown' | 'unknown' | Cost tier |
| `deployment` | 'cloud' \| 'network' | 'network' | Where the AI runs |
| `api_type` | 'openai' \| 'ollama' | 'openai' | API compatibility |
| `api_base` | string | '' | Override URL for cloud deployments |
| `features` | string | '' | Additional features |

**Lifecycle:**
1. `start()` creates socket, sends immediate PTR query for `_saturn._tcp.local`
2. Re-queries every 5 seconds to find new services
3. Stale services (not seen for 20 seconds) are cleaned every 15 seconds
4. Goodbye packets (TTL=0) trigger immediate removal via `onServiceRemoved`

**Model fetching:** `fetchModelsForService()` does HTTP GET to `{endpoint}/models`. Handles both `{ data: [{id}] }` (OpenAI) and `{ models: [{id}] }` (Ollama) response formats. 10s timeout, 2s retry on failure, 30s cooldown between attempts per service. Models are fetched lazily on first need.

**Key refresh:** `requestKeyRefresh(serviceName)` sends a TXT query for the specific instance. `waitForKeyRefresh(serviceName, timeout=2000)` polls until the key changes or times out.

### DiscoveredService Type

```typescript
interface DiscoveredService {
  name: string;           // Instance name (from PTR)
  host: string;           // Resolved hostname or IP
  port: number;           // From SRV record
  endpoint: string;       // http://{host}:{port}/v1
  priority: number;       // Lower = preferred (default 50)
  ephemeralKey: string;    // Rotating API key from TXT
  authType: 'none' | 'psk' | 'bearer';
  capabilities: string[];
  cost: 'free' | 'paid' | 'unknown';
  models: string[];       // Fetched from /v1/models
  modelsLastFetched: number | null;
  modelsLastAttempted: number | null;
  deployment: DeploymentType;   // 'cloud' | 'network'
  apiType: ApiType;             // 'openai' | 'ollama'
  apiBase: string;              // Override endpoint for cloud
  features: string;
  provider: string;             // Extracted hostname from apiBase
  lastSeen: number;             // Timestamp of last mDNS response
}
```

### Language Model: `SaturnChatLanguageModel`

Implements `LanguageModelV3` (spec version `'v3'`, provider string `'saturn'`).

**Endpoint resolution (`resolveEndpoints()`):**
1. Direct mode: returns synthetic service object
2. Normal mode: waits for initial discovery timeout
3. If health checks enabled: `getHealthyEndpointsForModel()`, falls back to unhealthy if all fail
4. Otherwise: `getEndpointsForModel()` — filters by model, sorts by priority
5. No endpoints + services exist: throws `NoSuchModelError` with diagnostic
6. No services at all: throws error suggesting Saturn router troubleshooting

**Request flow (`doGenerate()`):**
1. Resolve endpoints, filter to circuit-breaker-available ones (fall back to all if none available)
2. For each endpoint in priority order: `withRetry(() => callEndpoint(...))`
3. On success: `circuitBreaker.recordSuccess()`, parse response, return
4. On failure: `circuitBreaker.recordFailure()`, log failover, try next
5. All fail: throw aggregate error listing each endpoint's failure

**Streaming (`doStream()`):**
- Same resolution and failover as `doGenerate()`
- Returns `ReadableStream<LanguageModelV3StreamPart>` via `createFailoverStream()`
- Mid-stream failover: if stream errors before any content is emitted, tries next endpoint
- Once content has been emitted (`hasEmittedContent = true`), failover is disabled to prevent duplicate output

**Prompt conversion (`convertPrompt()`):**
- Converts `LanguageModelV3Prompt` to OpenAI-compatible messages
- System messages: pass through
- User messages: concatenates text parts with `\n`
- Assistant messages: handles text and tool-call parts
- Tool results: handles object, string, and `{text}` output formats

**Ephemeral key handling (`callEndpoint()`):**
- Before each request: looks up fresh key from discovery registry
- On 401 response (if key exists and not already retried):
  1. `discovery.waitForKeyRefresh(serviceName, 2000)` — sends TXT query, polls for new key
  2. New key arrives: retry with new key
  3. Timeout: fall through to normal error handling

**Tool calling:**
- Converts `options.tools` (type='function') to OpenAI format
- `toolChoice`: auto, none, required, or specific tool
- Streaming tool calls: emits `tool-input-start`, `tool-input-delta`, `tool-input-end`, `tool-call` parts
- Finish reason mapping: `tool_calls` -> `tool-calls`

### Circuit Breaker: `ServiceCircuitBreaker`

Implements Martin Fowler's Circuit Breaker pattern (cited in source comments). Per-service isolation — each service name has its own independent circuit state.

```typescript
class ServiceCircuitBreaker {
  constructor(threshold = 3, resetTimeout = 30000);
  recordFailure(serviceName: string): void;
  recordSuccess(serviceName: string): void;
  isAvailable(serviceName: string): boolean;
}
```

**States:** closed (default, healthy) → open (after `threshold` consecutive failures, stop sending) → half-open (after `resetTimeout` ms cooldown, allow one probe) → closed (on probe success).

### Retry Logic

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  options: { maxAttempts: number; delay: number },
  logger?: SaturnLogger
): Promise<T>;
```

Executes `fn` up to `maxAttempts` times with `delay` ms between attempts. Returns on first success, throws last error after exhaustion.

### Helper Functions

```typescript
// Route to correct endpoint based on deployment type
function endpoint(service: DiscoveredService): string {
  if (service.deployment === 'cloud') return service.apiBase;
  return service.endpoint;
}

function extractProvider(apiBase: string): string;  // hostname from API base URL
function isIPAddress(host: string): boolean;
```

The `endpoint()` function is the key routing decision: cloud deployments use `apiBase` (e.g., `https://openrouter.ai/api/v1`), network deployments use the local `endpoint` (e.g., `http://192.168.1.100:8080/v1`).

### Mock Server

Standalone test server (`mock-server.ts`, CLI: `npx saturn-mock-server [--port N] [--name NAME] [--priority N] [--rotation N]`) that:
1. Runs HTTP with OpenAI-compatible `/v1/chat/completions`, `/v1/models`, `/v1/health` endpoints
2. Serves an ELIZA chatbot as the `eliza` model
3. Announces via mDNS as `{name}._saturn._tcp.local`
4. Rotates ephemeral API keys on a configurable interval (default 60s)
5. Validates Bearer tokens against current key; returns 401 on expired keys

### Test Suite

**Unit tests** (`test/index.test.ts`, node:test + assert): `endpoint()` cloud vs network routing, TXT record parsing (all fields, edge cases, case insensitivity), prompt conversion (system/user/assistant/tool-result), finish reason mapping, priority sorting, circuit breaker state transitions, stream chunk transformation (SSE parsing, text deltas, tool call streaming).

**Integration test** (`test/restart-scenario.ts`): Three-phase test using mock server — Phase 1: initial discovery and inference; Phase 2: server restart on new port, re-discovery, inference; Phase 3: late start (SDK first, no services), server starts later, discover, infer.

## Why It Exists

The core Saturn protocol solves service *discovery*, but discovery alone is insufficient if applications cannot consume what is discovered. Most AI-enabled applications in the JavaScript/TypeScript ecosystem build on Vercel's AI SDK, which abstracts model providers behind a standard interface. Today, every AI SDK provider (OpenAI, Anthropic, Google, etc.) requires the developer to hardcode an API key and endpoint URL.

`ai-sdk-provider-saturn` eliminates both requirements by resolving all provider configuration from the network at runtime.

**Evidence:**

1. **Syed et al. (2025)** document the AIaaS status quo: each application must independently manage API keys, accounts, and endpoint configuration. This package collapses that per-application burden to a single network-level concern -- the admin runs a beacon, and every application on the network inherits AI capabilities.

2. **The code itself** demonstrates the zero-config property. The entire public API is a single factory export:
   ```typescript
   export const saturn = createSaturn();
   ```
   `createSaturn()` instantiates `SaturnDiscovery`, which immediately begins sending PTR queries for `_saturn._tcp.local` via the `multicast-dns` npm library. No constructor arguments are required. The developer's only action is `import`.

3. **Guttman (2001)** articulated the zero-config vision: "enable direct communications between two or more computing devices via IP" with no configuration. This package extends that vision from device-level pairing to SDK-level AI integration -- a developer adds one dependency, and their application communicates with whatever AI services the network provides.

## Who It Is Designed For

### Primary: Admins Who Are App Developers

These are people building applications that consume AI -- a chat interface, a code assistant, an internal tool. Today they must choose a provider, obtain an API key, manage that key's lifecycle, and hardcode the endpoint. With `ai-sdk-provider-saturn`, the developer delegates all of that to the network. Their app works on any network that has Saturn services, with whatever models those services provide.

**Evidence:**

1. **The open-source developer problem** is the direct motivation. The thesis context states: "Open source developers struggle with this; they might want to add AI features to their applications but cannot justify forcing users to bear API costs or subscription complications." This package is the technical answer: an open-source app can ship with `ai-sdk-provider-saturn` as a dependency and gain AI features on any Saturn-enabled network without bundling API keys.

2. **Meli et al. (2019)** found that static API key leakage is "pervasive -- affecting over 100,000 repositories," with 81% of leaked secrets never removed. Apps built on this provider never write a key to source code -- keys are discovered at runtime from mDNS TXT records and rotated automatically. The entire leakage class is eliminated by design, not by developer discipline.

### Secondary: Consumers (Indirectly)

A consumer never touches this package. But they benefit because the applications they use -- built by the admins above -- discover AI services without the consumer needing an account, a credit card, or an API key.

## How It Supports the Thesis Claims

### Claim 1 -- Zero-Config AI Provisioning Is Feasible

This package is a working implementation of Saturn discovery in a second language ecosystem (TypeScript), alongside the core Python package. It uses the `multicast-dns` npm library to query `_saturn._tcp.local`, parse TXT record metadata, and maintain a live service registry -- the exact same protocol the Python implementation uses.

**Evidence:**

1. **Siljanovski et al. (2014)** established that mDNS/DNS-SD adapts to new domains: printers, then IoT, now AI. This package is concrete proof of that extensibility -- the same `_saturn._tcp.local` service type works identically whether queried from Python's `zeroconf` library or JavaScript's `multicast-dns` package.

2. **Cross-language interoperability in the code.** The `SaturnDiscovery` class handles PTR, SRV, TXT, and A/AAAA records in the same sequence as the Python implementation. A Python-based Saturn beacon and a TypeScript-based Saturn provider interoperate without any bridging layer. This validates the Session 2 clarification: "Saturn is a protocol, not a language-specific implementation. Any language that can do mDNS can participate."

3. **Siddiqui et al. (2012)** describe zero-config foundations where services are discovered "with little end-user intervention." The `SaturnDiscovery` class embodies this: it sends periodic PTR queries (5s interval), follows up with SRV+TXT queries for each instance, resolves hostnames via A records, and maintains a live registry -- all without a single configuration parameter.

### Claim 2 -- Network-Provisioned AI Reduces Total Configuration Effort

**Evidence:**

1. **Step-count comparison from the code.** Traditional AI SDK setup: create account, generate API key, store in `.env`, install SDK, configure provider with key + endpoint, select model, handle key rotation. Saturn: `npm install ai-sdk-provider-saturn`, `import { saturn }`, use. The developer's configuration effort drops to zero; the admin's one-time beacon setup serves N developers.

2. **Meli et al. (2019)** found that the best secret-scanning tools catch only 25% of leaked keys, and "all mitigations act too late." Saturn eliminates the need for secret scanning entirely -- there are no secrets in the developer's codebase. The `SaturnChatLanguageModel` reads the ephemeral key from the discovery registry at request time. The key was never in a file, never in an environment variable, never in a repository.

3. **Guttman (2001)**, quoting RFC 1122: "It would be ideal if a host implementation of the Internet protocol suite could be entirely self-configuring." This package achieves that for AI: the provider self-configures from network announcements without any host-side configuration files.

### Claim 3 -- Security Trade-offs Are Known and Addressable

**Evidence:**

1. **Ephemeral key rotation in the code.** When the model layer receives a 401 (expired key), it calls `discovery.waitForKeyRefresh()`, which sends a targeted TXT query to fetch the latest rotated key, then retries the request. Applications automatically participate in Saturn's credential rotation without developer intervention. The mock server demonstrates this with configurable rotation intervals (default 60 seconds).

2. **Kaiser & Waldvogel (2014a)** identified passive eavesdropping as the primary threat model for mDNS-SD: "every machine in the same network will automatically receive all the announcement traffic." The `ai-sdk-provider-saturn` package operates within this known threat boundary -- ephemeral keys are broadcast in TXT records, which means any device on the network can read them. This is a deliberate trade-off for the target environment (campus WiFi, homes, offices), not an oversight.

3. **The circuit breaker pattern** (`retry.ts`) implements Martin Fowler's Circuit Breaker: after 3 consecutive failures to a service, the circuit trips open and requests route to the next-priority service. After a 30-second cooldown, one probe request tests recovery. Combined with priority-based failover across all discovered services, this provides resilience against both service failures and potentially compromised endpoints -- a service that consistently returns errors is automatically deprioritized.

## Thesis Chapter Mapping

| Chapter | Relevance |
|---------|-----------|
| Ch. 3 (Design) | Demonstrates Saturn's beacon protocol consumed from the client side. The provider only *reads* mDNS announcements -- no API traffic flows through the announcer. Validates the beacon vs. proxy distinction. |
| Ch. 4 (Implementation) | Client-side integration pattern showing how unmodified AI SDK applications gain Saturn capabilities through a provider swap. Cross-platform mDNS via `multicast-dns` npm package. |
| Ch. 5 (Scenarios) | The ELIZA mock server is a self-contained scenario: mDNS announcement, key rotation, OpenAI-compatible API, discovery, authenticated request, response. |
| Ch. 6 (Evaluation) | Step-count comparison: traditional provider setup vs. Saturn provider setup. Measurable reduction in configuration effort. |
| Ch. 7 (Discussion) | Ephemeral key broadcast trade-off. Circuit breaker as mitigation for unreliable/hostile services. Open-source developer access implications. |
