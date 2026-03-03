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
- **Wharton et al. (1994)** -- Cognitive walkthrough methodology used for evaluation

## Evidence: Cognitive Walkthrough

Three-persona cognitive walkthrough comparing Saturn vs traditional AI provisioning. Completion criterion: "an end user on the network uses an AI-powered feature in an application."

### Step counts (from `cog_walkthrough/*.py`)

| Persona | Traditional | Saturn (package) | Change |
|---------|------------|-----------------|--------|
| Sysadmin | 12 | 14 | +2 (+17%) |
| App Developer | 19 | 4 | -15 (-79%) |
| End User | 7 | 0 | -7 (-100%) |
| **Total (1+1+1)** | **38** | **18** | **-20 (-53%)** |

### Scaling formula

- Traditional: 12 + 19N + 7M
- Saturn: 14 + 4N + 0M
- At N=10 devs, M=100 users: 902 vs 54 steps (94% reduction)

### Key insight

Saturn concentrates complexity at the sysadmin level (one person, one time) and eliminates it for app developers and end users. The sysadmin does 2 more steps; each developer saves 15 steps; each end user saves 7 steps. The billing/payment integration stack (13 Stripe steps) vanishes entirely.

### Limitations

- Single-author walkthroughs (analytical step counts, not empirical timing)
- Walkthrough scripts included in repository for reproducibility
