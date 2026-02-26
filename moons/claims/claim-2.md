# Claim 2: Network-Provisioned AI Reduces Total Configuration Effort

> Saturn reduces the total configuration burden across a network compared to per-user manual setup, at the cost of shifting complexity to a single administrator.

## Core argument

The claim is comparative and honest about the trade-off: N users do zero work, 1 admin does more work. Net effort decreases. The complexity hasn't disappeared -- it's been centralized in one place instead of scattered across N users.

## Literature grounding

- **Syed et al. (2025)** -- Documents the AIaaS status quo: API keys, accounts, platform lock-in
- **Costa et al. (2024)** -- Accessibility and usability as dimensions of AI democratization
- **Guttman (2001)** -- Quoting RFC 1122: "It would be ideal if a host implementation of the Internet protocol suite could be entirely self-configuring"
- **Meli et al. (2019)** -- Static API key management fails at scale; "secret leakage pervasive -- affecting over 100,000 repositories"; Saturn eliminates per-user key handling entirely
- **Qazi (2023)** -- "Most of the corporations, unfortunately, do not know the number of APIs they have or how to secure them"; Saturn's ephemeral beacon removes the inventory problem

## Evidence

**Comparison baselines (evaluation planned):**
1. Manual API setup (get key -> install client -> paste key -> configure endpoint -> select model)
2. Existing aggregators (LiteLLM, Requesty, OpenRouter direct)
3. Saturn-aware integrations (Jan.ai, OpenCode -- zero config vs. their current setup flows)

**Evaluation gap**: No existing literature covers AI service discovery comparison methodology. This is novel territory -- Saturn defines the benchmark. Formal evaluation is planned (setup step counts and/or timing across tools).

## Open issue: step-count scope (discuss with Adam)

The blind-agent evaluation scenarios pre-stage infrastructure (API keys in files, Ollama already running, LiteLLM pre-installed). This means the automated step counts only measure the **client-configuration portion** -- not the full onboarding flow (account creation, email verification, payment, key generation).

**Consequence**: Automated results will understate the real gap. If Saturn measures 3 steps and manual-openrouter measures 6, the real-world difference is more like 3 vs 15 because the early steps are skipped.

**Why it's done this way**: Those early steps can't be automated (CAPTCHAs, email verification, credit cards). Also, Saturn's claim is about per-user config on a network where the admin already has a backend -- the scenarios test exactly that scope.

**Possible fix**: Report automated step counts as the "last-mile configuration" metric. Add a separate analytical table enumerating the full onboarding flow per baseline (from documentation, not measurement). Present both. Be explicit about what each number covers.
