# API Key Leakage

The static API key management model is fundamentally broken. Saturn's ephemeral keys sidestep this entire failure class.

## The problem
- Over 100,000 GitHub repos contain leaked secrets (Meli 2019)
- 81% of leaked secrets are never removed after notification
- Best automated scanning tools only detect 25% of leaks
- "All mitigations act too late" — damage done before detection
- Organizations can't track their own API keys (Qazi 2023)

## How Saturn solves it
- Ephemeral keys expire in 10 minutes — leaked keys are already dead
- Keys never stored in config files, env vars, or repos
- Broadcast via mDNS TXT records — only available while on the network
- No inventory problem: keys are transient, not persistent artifacts

## The AI context
Per-user API key management for AI services (OpenAI, Anthropic, etc.) replicates the same failure pattern at consumer scale. Every user managing their own key = N potential leaks.

## Papers
- meli-2019, qazi-2023

## Chapters
- Ch 1.1: configuration burden
- Ch 2.5: static key failure
- Ch 3.3: ephemeral key design
