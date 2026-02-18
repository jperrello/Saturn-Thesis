# Vercel AI SDK

TypeScript framework for building AI applications. Saturn has a native provider for it.

## What it is
- Unified API for multiple AI providers (OpenAI, Anthropic, Google, etc.)
- Provider pattern: swap backends without changing application code
- Streaming support, tool calling, structured output
- Used by Next.js apps, Vercel-hosted AI products

## Saturn's integration
- `ai-sdk-provider-saturn`: native Saturn provider for Vercel AI SDK
- Uses `multicast-dns` npm package to query `_saturn._tcp.local.`
- Cross-language interop proof: TypeScript mDNS consumes same service as Python zeroconf
- Developer experience: `npm install` + `import`. Zero keys, zero env vars, zero URLs.

## Significance for thesis
- 3rd protocol implementation (after Python, Rust)
- Validates Claim 1 beyond single-language demo
- Circuit breaker pattern (3 failures → trip → 30s cooldown)
- Auto key refresh on 401 — handles ephemeral key rotation transparently

## Chapters
- Ch 4.3: native SDK client pattern
