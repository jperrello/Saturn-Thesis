# Cognitive Walkthrough — Evaluation Methodology for Claim 2

## Completion Criteria

The "done state" that makes Saturn and traditional paradigms comparable:

**An end user on the network can use an AI-powered feature in an application.**

This is the full chain:
1. Sysadmin/IT provisions AI access on the infrastructure
2. App developer integrates AI into their application
3. End user consumes the AI feature

Both paradigms must be walked to this same finish line. Without a shared completion point, step counts are not comparable — you'd be measuring Saturn's full story against traditional's first chapter.

## Three Personas

The cognitive walkthrough separates configuration burden across three distinct roles:

1. **Sysadmin/IT person** — configures Saturn at the institutional level, or provisions and distributes API keys in the traditional model
2. **App developer** — builds an application that uses AI services
3. **End user** — a person on the network using an app with AI features

## Shared Prerequisites

Both paradigms share initial steps (API key procurement):
- Go to openrouter.ai (or any API key provisioner)
- Create an account and sign in
- Go to settings
- Click API keys
- Create a new key
- Copy key and store it somewhere safe
- Create a .env file
- Place key in file as OPENROUTER_API_KEY

**Saturn and traditional methods diverge after this point.**

## Key Insight: Where Burden Shifts

Saturn concentrates complexity at the sysadmin level (one person, one time) and eliminates it for app developers and end users. Traditional distributes complexity across every developer and every end user.

- **Sysadmin**: Saturn has MORE steps (deploys a server), but the outcome is qualitatively different (centralized service with discovery vs. raw key distribution)
- **App developer**: Saturn has FAR FEWER steps (4 vs. 19) because it eliminates the entire billing/payment integration stack
- **End user**: Saturn eliminates the payment barrier entirely — the ONLY steps that differ are the payment-related ones (credit card, subscription, ToS). App onboarding steps (download, account creation, login) are shared and orthogonal to the AI paradigm.

## Walkthrough Files

Located at: `cog_walkthrough/` (relative to project root)

| File | Persona | Paradigm | Steps |
|------|---------|----------|-------|
| `cog_saturn.py` | Sysadmin | Saturn (manual) | 8 prereqs + 18 code = 26 |
| `cog_sat_package.py` | Sysadmin | Saturn (package) | 8 prereqs + 6 code = 14 |
| `cog_traditional.py` | Sysadmin | Traditional | 8 prereqs + 4 distribution = 12 |
| `app_dev_sat.py` | App Dev | Saturn | 4 |
| `app_dev_trad.py` | App Dev | Traditional | 6 AI + 13 billing = 19 |
| `end_user_sat.py` | End User | Saturn | shared app steps + 0 payment = 0 additional |
| `end_user_trad.py` | End User | Traditional | shared app steps + 7 payment = 7 additional |

## Why This Matters for Claim 2

Claim 2: "Network-provisioned AI reduces total configuration effort."

The cognitive walkthrough provides concrete, countable evidence. The step counts show that Saturn shifts burden upward (to the sysadmin) and eliminates it downward (for developers and end users). The total system-wide configuration effort is lower because one sysadmin setup replaces N developer billing integrations and M end user payment flows.
