# AI Modality Coverage

What types of AI people can use through Saturn today. Current state only.

## Fully supported

### Text chat completions
Saturn's core use case. All six components demonstrate it. Any backend exposing chat completion endpoints works.

**Backends confirmed**: Ollama, OpenRouter, DeepInfra, LiteLLM, vLLM.

**Clients confirmed**: Core Python CLI, ai-sdk-provider (TypeScript), Open WebUI plugin, saturn-mcp (Claude Code/Cursor/Windsurf), VLC extension.

### Agentic coding
Works through saturn-mcp. AI coding assistants (Claude Code, Cursor, Windsurf) discover Saturn services and use them for code generation, explanation, refactoring, etc. The assistant's tool-use loop is the "agentic" part — Saturn provides the model endpoint.

**How it works**: One MCP server JSON entry. `list_available_models` aggregates all services. `chat_completion` routes to the best service by priority with ephemeral key auth.

## Works via passthrough (not explicitly advertised)

### Vision / photo analysis
The OpenAI chat completions API supports multimodal inputs (images as base64 or URLs in the messages array). If the backend model supports vision, the request passes through Saturn transparently.

**Backends that support this**: Ollama with vision models (llava, llama3.2-vision), OpenRouter with GPT-4o/Claude, DeepInfra with vision-capable models.

**Limitation**: Saturn's TXT records don't advertise "vision" or "multimodal" as capabilities. A client has no way to discover which services support image input without trying or knowing the model name. Discovery finds the service; capability awareness is left to the client's knowledge of the model.

### Embeddings
Ollama exposes `/api/embeddings` natively. OpenAI-compatible backends may expose `/v1/embeddings`. Saturn discovers the service; if the client knows to call the embeddings endpoint, it works.

**Same limitation**: Not advertised in TXT records. Client must know the backend supports it.

### Audio transcription
Ollama and some OpenAI-compatible backends support audio endpoints. Same passthrough pattern — Saturn discovers the service, client calls the endpoint directly.

## Does not work today

### Image generation
`/v1/images/generations` exists in the OpenAI API but Saturn doesn't advertise or route to this endpoint. A Saturn service could expose it, but no current implementation does.

### Real-time / WebSocket APIs
WebSocket-based real-time APIs (OpenAI's Realtime API) don't fit Saturn's HTTP-based discovery model. Saturn supports SSE streaming for chat completions but not persistent WebSocket connections.

### Text-to-speech
`/v1/audio/speech` — not part of any current Saturn implementation.

## The pattern

Saturn's discovery is **modality-agnostic at the protocol level**. The TXT records provide a URL, credentials, and metadata. What the client does with that URL is unconstrained. The limitation is practical, not architectural:

1. Saturn implementations currently target chat completions because that's the dominant use case
2. TXT records don't advertise capabilities beyond `api_type` and model names
3. Clients must independently know what endpoints a discovered backend supports

The equity argument (students accessing LLMs for writing, coding, learning) is fully served by the current scope. Chat completions + agentic coding cover the use cases that matter most for the thesis claims.
