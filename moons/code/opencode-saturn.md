# OpenCode Saturn
**Source**: code/opencode-saturn.md
**Claims**: Claim 1 (7th Saturn consumer, 2nd TypeScript), Claim 2 (zero-config coding agent), Claim 3 (inherits ephemeral keys from ai-sdk-provider-saturn)

## Source Files
**Repository**: [`jperrello/opencode-saturn`](https://github.com/jperrello/opencode-saturn) (fork of [anomalyco/opencode](https://github.com/anomalyco/opencode))
**Default branch**: `dev`

Key files modified from upstream:
- `packages/opencode/src/provider/provider.ts` — Saturn custom loader, dynamic registration, failover, fetch patch
- `packages/opencode/src/server/mdns.ts` — MDNS namespace wrapping ai-sdk-provider-saturn
- `packages/opencode/src/bus/index.ts` — ProviderChanged event definition
- `packages/opencode/src/session/processor.ts` — V3 finishReason normalization
- `packages/opencode/test/provider/saturn.test.ts` — Unit tests for adapt, failover
- `.opencode/opencode.jsonc` — default config with Saturn enabled

## What It Is

A fork of [OpenCode](https://github.com/anomalyco/opencode) -- an open-source AI coding agent built by Anomaly -- with `ai-sdk-provider-saturn` integrated as a bundled provider. When launched, OpenCode-Saturn automatically discovers Saturn services on the local network via mDNS and makes their models available for code generation, editing, and agentic tool use. No API keys, no endpoint URLs, no `.env` files.

## Implementation Details

### CUSTOM_LOADERS["saturn"] Registration

The Saturn loader is registered as a custom loader in the `CUSTOM_LOADERS` record alongside anthropic, openai, etc.:

```typescript
const CUSTOM_LOADERS: Record<string, CustomLoader> = {
  // ... anthropic, openai, etc.
  saturn: async () => { /* ... */ }
}
```

**Initialization:** Creates a `createSaturn()` SDK instance with `discoveryTimeout: 3000`, stored in the module-level `saturnDiscoverySdk` variable. Waits up to 3 seconds for mDNS responses, then fetches `/v1/models` from all discovered services.

### createProviderInfo() Flow

For each discovered service with models, `createProviderInfo` builds a provider entry:

1. Provider ID: `saturn:{serviceName}`
2. Display name: `Saturn • {ServiceName}` (formatted with capitalized words)
3. Models get `toolcall: true` capability by default
4. Options carry `serviceEndpoint`, `serviceName`, `serviceEphemeralKey` for direct-mode connection
5. Model loader uses direct mode (`createSaturn({ serviceEndpoint, serviceName, serviceEphemeralKey })`) to create per-service SDK instances, avoiding re-discovery
6. Returns `{ autoload: total > 0, getModel, options, dynamicProviders }`

### Background Re-Registration Callbacks

After initial discovery, two callbacks handle dynamic changes:

**`onServiceDiscovered`:** When a new service appears on the network:
1. Runs inside `Instance.provide()` to set correct instance context
2. Fetches models with retry (up to 3 attempts, 500ms delay)
3. Creates provider info and calls `registerDynamic()`

**`onServiceRemoved`:** When a service disappears:
1. Checks if service was re-discovered (race condition guard)
2. If truly gone, calls `unregisterDynamic()`

### registerDynamic() / unregisterDynamic()

```typescript
export async function registerDynamic(providerID: string, provider: Info): Promise<void>
```

`registerDynamic()`:
1. Adds provider to instance-level state (`s.providers[providerID]`)
2. For Saturn providers (`providerID.startsWith("saturn:")`): creates a model loader that fetches fresh ephemeral key from discovery before each call, stores in `globalSaturnProviders` Map
3. Emits two events:
   - `GlobalBus.emit("event", { directory: "global", payload: { type: "server.provider.changed" } })`
   - `Bus.publish(Bus.ProviderChanged, { action: "added", providerID })`

`unregisterDynamic()`:
- Re-checks if service still exists in discovery (debounce against race conditions)
- Removes from `globalSaturnProviders`, instance state, and model loaders
- Emits removal events on both GlobalBus and Bus

### Bun Fetch Timeout Patch

```typescript
function patchSaturnFetch<T extends (...args: any[]) => Promise<any>>(fn: T): T {
  return (async (...args: any[]) => {
    const original = globalThis.fetch
    globalThis.fetch = ((input: any, init?: any) =>
      original(input, { ...init, timeout: false })) as typeof fetch
    try {
      return await fn(...args)
    } finally {
      globalThis.fetch = original
    }
  }) as T
}

function wrapSaturnModel(model: any) {
  const doStream = model.doStream.bind(model)
  const doGenerate = model.doGenerate.bind(model)
  model.doStream = patchSaturnFetch(doStream)
  model.doGenerate = patchSaturnFetch(doGenerate)
  return model
}
```

**Problem:** Bun's fetch has a default timeout (bun issue #16682). Long-running LLM streaming requests get killed.
**Solution:** Monkey-patches `globalThis.fetch` for the duration of each `doStream`/`doGenerate` call, adding `timeout: false`. Restores original fetch in `finally` block.

### V3 finishReason Normalization

**File:** `packages/opencode/src/session/processor.ts`

OpenCode's session processor expects `finishReason` as a string (V2 format: `"stop"`, `"length"`, etc.), but Saturn's AI SDK provider returns V3 format: `{ unified: "stop", raw: "end_turn" }`.

```typescript
const reason = typeof value.finishReason === "object" && value.finishReason !== null
  ? (value.finishReason as any).unified ?? "unknown"
  : value.finishReason
```

One-line conversion bridging V3→V2 without changes to ai-sdk-provider-saturn.

### Bus Event System (ProviderChanged)

**File:** `packages/opencode/src/bus/index.ts`

```typescript
export const ProviderChanged = BusEvent.define(
  "server.provider.changed",
  z.object({
    action: z.enum(["added", "removed"]),
    providerID: z.string(),
  }),
)
```

Published when Saturn services appear or disappear. Two event buses are used:
1. `Bus.publish()` — Instance-scoped (current project session)
2. `GlobalBus.emit()` — Process-wide EventEmitter (cross-instance updates, web UI)

Both fire on registration/unregistration, allowing TUI and web UI to update the model selector in real time.

### MDNS Module Wrapper

**File:** `packages/opencode/src/server/mdns.ts`

Wraps `ai-sdk-provider-saturn` for OpenCode's architecture:

```typescript
export namespace MDNS {
  export function publish(port: number): void;     // Publish opencode's own mDNS service
  export function unpublish(): void;
  export async function discover(options): Promise<DiscoveredService[]>;
  export function services(): DiscoveredService[];
  export function service(name: string): DiscoveredService | undefined;
  export async function fetchModels(): Promise<void>;
  export async function fetchModelsFor(name: string): Promise<boolean>;
  export function model(id: string): LanguageModelV3;
  export function destroy(): void;
}
```

Uses `bonjour-service` for publishing OpenCode's own HTTP service (separate from Saturn discovery), and `ai-sdk-provider-saturn` for Saturn service discovery.

### Failover Function

**File:** `packages/opencode/src/provider/provider.ts`

```typescript
export async function failover(input: {
  providerID: string
  modelID: string
}): Promise<{ providerID: string; modelID: string } | undefined>
```

When a Saturn provider fails:
1. Only activates for Saturn providers (`id.startsWith("saturn:")`)
2. Searches all other `saturn:*` providers for the same model
3. If found, returns the alternative provider+model pair
4. Falls back to `defaultModel()` as last resort
5. Returns `undefined` if no failover available

### Global Saturn Provider Cache

```typescript
let saturnDiscoverySdk: ReturnType<typeof createSaturn> | null = null
const globalSaturnProviders = new Map<string, { info: Info; loader: CustomModelLoader }>()
```

**Problem:** OpenCode uses instance-scoped state tied to project directories. Switching projects resets provider state, losing Saturn services.
**Solution:** Module-level `globalSaturnProviders` Map persists across instance resets. The `list()` function merges global Saturn providers back into the current instance's provider list.

## Commit History (Saturn-specific, chronological)

| Commit | Message | Key Change |
|--------|---------|------------|
| `f8d8f6c` | feat(provider): add saturn network provider with mDNS discovery | Initial integration, +115 lines to provider.ts |
| `19975c7` | refactor: rename AGENTS.md to CLAUDE.md and fix saturn naming conventions | Naming cleanup |
| `4e9a4c6` | docs: rewrite README for Saturn fork with upstream attribution | Documentation |
| `3560f67` | feat(provider): add saturn dynamic registration with queued message fixes | `registerDynamic`/`unregisterDynamic`, +324/-28 lines |
| `eb8f37a` | fix(session): convert V3 finishReason to string before message save | First finishReason fix |
| `992cd94` | fix(types): resolve TypeScript errors from Saturn provider integration | Type fixes |
| `db3e433` | fix(session): normalize V3 finishReason to string in processor | Processor-level finishReason normalization |
| `e64ae8d` | fix(provider): add failover and bridge provider events to instance bus | Instance.provide() wrapping, global cache |
| `a851d2d` | feat(saturn): add fetch timeout patch, failover, and service notifications | MDNS module, Bun fetch patch, +134 lines test |
| `22edeef` | fix(provider): show all saturn models in web UI model selector | Web UI propagation |
| `781bb21` | fix(provider): enable tool calling for Saturn models | `toolcall: true` capability flag |

## Bugs Found During Integration

The Jan 31, 2026 meeting log documents three bugs discovered during initial testing:

1. **Model list staleness**: Models don't update when new Saturn providers join the network while OpenCode is running. Fixed by the dynamic registration system (commit `3560f67`).
2. **Provider deduplication**: Multiple Saturn servers only show one provider if OpenCode started after them. Fixed by the mDNS module refactor (commit `a851d2d`).
3. **Message queuing**: After first response, messages queue instead of sending. Fixed by the finishReason normalization (commits `eb8f37a`, `db3e433`).

Additional bugs from integration:
4. **Bun fetch timeout**: Long-running LLM streaming killed by Bun's default HTTP timeout. Fixed with `globalThis.fetch` monkey-patch (commit `a851d2d`).
5. **Instance scope race conditions**: Discovery callbacks fired outside correct Instance context. Fixed by wrapping in `Instance.provide()` and adding the global cache (commit `e64ae8d`).
6. **Tool calling disabled**: Saturn models missing `toolCalling` capability flag, causing structured function calls to serialize as plain text. Fixed by setting `toolcall: true` in `fromDynamicModel()` (commit `781bb21`).

These bugs and their fixes are evidence that integrating Saturn into a real application surfaces non-trivial engineering challenges -- the protocol works, but the host application's assumptions about provider lifecycle need to change.

## Test Suite

**File:** `packages/opencode/test/provider/saturn.test.ts`

- V3 finishReason object-to-string conversion
- String finishReason passthrough
- Missing finishReason defaults to "unknown"
- Failover returns undefined for non-saturn providers
- Failover returns undefined when no saturn services exist (does not throw)

## Why It Matters for the Thesis

### Different from ai-sdk-provider-saturn

The SDK provider is a library -- it gives developers the *ability* to build Saturn-aware apps. OpenCode-Saturn is a *finished application* that uses that library. The distinction matters: the SDK proves the protocol works at the API level; OpenCode proves it works in a real, complex application with a TUI, a web UI, an event bus, session persistence, and agentic tool calling.

### Complexity of the host application

OpenCode is not a toy. It has a client/server architecture, LSP integration, provider-agnostic model routing, and a reactive UI layer. Integrating Saturn required changes across 12 files in 4 packages. The fact that Saturn plugged in without forking OpenCode's core abstractions -- only extending them -- is evidence of protocol composability.

## How It Supports the Thesis Claims

### Claim 1 -- Zero-Config AI Provisioning Is Feasible

**Supports.** OpenCode-Saturn is the 7th Saturn consumer implementation and the 2nd TypeScript consumer (after ai-sdk-provider-saturn itself). It demonstrates Saturn working in an agentic coding context -- the most demanding AI use case, requiring streaming responses, tool calling, and multi-turn conversations.

**Evidence:**

1. The custom loader in `provider.ts` uses `ai-sdk-provider-saturn` to query `_saturn._tcp.local`, parse TXT records, and register models -- the same protocol every other Saturn consumer uses. **Siddiqui et al. (2012)** describe zero-config as enabling service use with "little end-user intervention"; OpenCode-Saturn requires none.

2. Tool calling works over Saturn-discovered models (commit `781bb21`). This is significant because agentic coding requires structured function calls, not just text generation. Saturn's OpenAI-compatible passthrough preserves the full tool-calling protocol end-to-end.

### Claim 2 -- Network-Provisioned AI Reduces Total Configuration Effort

**Supports.** This is the strongest claim support. Coding agents are among the most configuration-heavy AI applications.

**Evidence:**

1. **Baseline comparison.** Setting up OpenCode with a cloud provider: create account, generate API key, add to `.opencode/opencode.jsonc` or environment variable, specify model ID. Setting up OpenCode-Saturn: `bun run dev`. The developer does nothing. The models appear from the network.

2. **The dynamic registration system** (commit `3560f67`) means the coding agent adapts to network changes without restart. If an admin deploys a new Saturn beacon advertising GPT-4o, OpenCode-Saturn picks it up live. Traditional setup would require the user to stop, edit config, and restart.

3. **Costa et al. (2024)** define accessibility as a dimension of AI democratization. A coding agent that works without API key configuration is more accessible to developers who cannot or do not want to manage provider accounts -- students, open-source contributors, workshop participants.

### Claim 3 -- Security Trade-offs Are Known and Addressable

**Partially supports.** OpenCode-Saturn inherits the security properties of `ai-sdk-provider-saturn`, including ephemeral key consumption and automatic retry on 401 (key rotation). It does not add its own security mechanisms.

The relevant security consideration is that a coding agent has high-privilege tool access (file editing, shell execution). If a rogue Saturn service on the network advertises a malicious model, OpenCode-Saturn would route requests to it. This is the same threat model as any mDNS-based service, mitigated by the LAN trust boundary assumption documented in the thesis.

## Thesis Chapter Mapping

| Chapter | Relevance |
|---------|-----------|
| Ch. 3 (Design) | Demonstrates Saturn's protocol consumed by a complex, multi-component application without protocol modifications. The dynamic registration pattern shows how applications adapt to Saturn's runtime discovery model. |
| Ch. 4 (Implementation) | Fork-based integration pattern. 11 commits, 12 files, 4 packages. Shows the engineering work required to make a static-provider application dynamic. |
| Ch. 5 (Scenarios) | A developer at a university opens their laptop, runs OpenCode-Saturn, and immediately has access to whatever AI models the campus Saturn network provides. They write code, use tools, and never configure a provider. |
| Ch. 6 (Evaluation) | Cognitive walkthrough comparison: OpenCode manual provider setup (5+ steps) vs. OpenCode-Saturn (0 steps, models discovered automatically). |
| Ch. 7 (Discussion) | The tool-calling fix illustrates a real integration challenge: capability flags must propagate correctly through the discovery chain. The rogue-service threat model is amplified in an agentic context. |
