# MCP (Model Context Protocol)

Anthropic's protocol for connecting AI assistants to external tools. Saturn has an MCP server implementation.

## What it is
- Standardized protocol for AI assistants to discover and use tools
- Client-server architecture: AI assistant (client) connects to tool servers
- Transport via stdio, HTTP, or SSE
- Dominant extension protocol for AI coding assistants (Claude, Cursor, etc.)

## Saturn's MCP integration
- `saturn-mcp`: MCP server that exposes Saturn discovery as tools
- One JSON config entry replaces per-provider API key management
- `list_available_models` aggregates all discovered Saturn services
- AI assistant acts on user's behalf — new security surface

## Significance for thesis
- 5th independent protocol consumer (after Python, Rust, TypeScript, Lua)
- Demonstrates Saturn works in the AI assistant ecosystem, not just standalone apps
- MCP is how coding agents will most likely consume Saturn services

## Chapters
- Ch 4.3: tool protocol bridge pattern
- Ch 7.1: new threat surface (AI acting on user's behalf)
