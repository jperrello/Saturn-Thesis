# OpenAI-Compatible API

The de facto standard REST API for AI text completion. Saturn's endpoint compatibility layer.

## What it is
- REST API with `/v1/chat/completions`, `/v1/models`, `/health` endpoints
- JSON request/response format with messages array, model selection, temperature, etc.
- Originally defined by OpenAI, now implemented by dozens of providers
- Ollama, LiteLLM, vLLM, OpenRouter all expose this interface

## Why Saturn uses it
- **Ubiquity**: most AI apps already speak this protocol
- **Backend agnosticism**: Saturn doesn't care what's behind the API — local Ollama, cloud OpenRouter, or anything else
- **Zero client changes**: apps that support "custom OpenAI endpoint" work with Saturn immediately
- **The protocol doesn't prescribe who runs the server** — university IT or hobbyist on a Pi

## Saturn's endpoint expectations (per docs website)
1. `GET /v1/health` — liveness check, returns JSON status
2. `GET /v1/models` — enumerate available models (OpenAI list-models format)
3. `POST /v1/chat/completions` — chat completion (streaming + non-streaming)

## Chapters
- Ch 3.4: endpoint expectations in protocol spec
- Ch 4.2: server types implement this interface
- Ch 4.3: client patterns consume it
