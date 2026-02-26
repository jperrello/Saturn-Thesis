# Appendix A: Generative AI in Saturn Thesis Creation

## Executive Summary

This thesis was developed with substantial support from Claude (Anthropic), a large language model. This appendix documents:

1. **Moons knowledge graph authorship** — how iterative prompting with an LLM organized Saturn's evidence and argument structure
2. **Claude as thesis advisor** — what role an AI played in refining claims, identifying gaps, and writing thesis content
3. **AI in evaluation design** — how Claude assisted in experiment design, grader prompting, and result interpretation
4. **Decision boundaries** — where human judgment overrode AI suggestions and why

The goal is transparent methodology, not to diminish human intellectual contribution. Every AI output was reviewed, questioned, and refined by human judgment.

---

## Part 1: Moons Knowledge Graph Authorship

### The Problem

Saturn research spans:
- **20+ papers** from five domains (networking, security, HCI, AI/accessibility, threat modeling)
- **6 implementation components**, each touching 2-3 thesis claims
- **3 thesis claims** with overlapping evidence
- **Design rationale** scattered across voice files, meeting logs, and code comments

A traditional document (or even an outline) couldn't efficiently track relationships:
- Which papers support claim-1 vs. claim-3?
- Where do we explicitly *contrast* with existing work (BeyondCorp, DNS-SD alternatives)?
- How do concepts (beacons, ephemeral keys, mDNS) nest logically?
- Which components demonstrate which claims?

**The need:** A queryable, visually navigable knowledge structure that surfaces connections and ensures consistency.

### Moons as Solution

In October 2025, I sketched the moons architecture: lightweight nodes (concept, claim, paper, component, chapter, person) with typed edges (supports, contrasts, related, demonstrated_by, etc.). The graph itself is ~500 lines of JSON; depth lives in linked files.

**Why AI was helpful here:**
- **Scaffolding speed** — generating candidate edges is fast; reviewing them is careful
- **Cross-domain synthesis** — Claude can connect a mDNS paper to an AI accessibility paper without prompting
- **Consistency checking** — flag contradictions or orphaned nodes
- **Iteration** — refine the graph as new papers arrive or claims shift

### The Authorship Process

#### Phase 1: Structure Definition (Oct 2025)

Claude and I defined:
```
node_types: ["concept", "claim", "paper", "component", "chapter", "person", "voice", "meta"]
edge_types: ["supports", "contrasts", "cited_in", "demonstrated_by", 
             "rationale", "related", "discussed_in", "advises"]
```

We iterated on semantics. For example:
- **supports** = a paper provides direct evidence for a claim
- **contrasts** = a paper or approach intentionally diverges from Saturn (e.g., BeyondCorp vs. our zero-config model)
- **related** = connection exists but isn't a support/contrast/citation (weaker claim)

This precision mattered: broad "related" would obscure meaningful distinctions.

#### Phase 2: Bulk Generation (Nov-Dec 2025)

For claim-1 (mDNS feasibility), the conversation went roughly:

```
Me: "Generate a first-pass set of edges for claim-1. What papers support it?"

Claude:
- guttman-2001 → claim-1 (supports) [Zeroconf origins]
- siddiqui-2012 → claim-1 (supports) [DNS-SD foundations]
- siljanovski-2014 → claim-1 (supports) [mDNS for IoT]
- kim-reeves-2020 → claim-1 (supports) [DNS vulnerabilities matter for mDNS]
- kaiser-waldvogel-2014a → claim-1 (contrasts) [privacy concerns limit some deployments]

Me: "Generate edges for related concepts."

Claude:
- claim-1 → mdns (related)
- claim-1 → dns-sd (related)
- ... [more edges]

Me: [Manually review, add missing papers I found, refine descriptions]
"Siljanovski says mDNS works for IoT—is that direct support or just precedent?"
"Kim-Reeves focuses on DNS attacks broadly; which mDNS-specific concerns matter?"
[Integration into graph.json]
```

This process repeated for claim-2 (configuration effort) and claim-3 (security tradeoffs).

#### Phase 3: Refinement (Jan-Feb 2026)

Iterative refinement pass:
- **Consistency:** Do edge directions make sense? Is a paper supporting or contrasting?
- **Completeness:** Are there obvious gaps? (e.g., missing connection between beacons and ephemeral-keys)
- **Description quality:** Auto-generated descriptions were often vague; rewrite for precision
  - Before: `"Related to DNS"`
  - After: `"Multicast DNS — link-local name resolution without infrastructure"`

#### Phase 4: Living Knowledge Base

Moons isn't frozen. After advisor meetings, I update:
1. The relevant content file (e.g., `voice/interview-2.md`)
2. The graph edges that changed (e.g., new rationale connections)
3. Rebuild the visualization (run `sync.py`)

This keeps moons a **reflection of current thinking**, not a snapshot.

### What AI Did Well

1. **Fast edge generation** — Claude produced ~100 candidate edges in minutes; manually researching each would have taken hours
2. **Cross-domain connections** — Claude linked a networking paper to an AI accessibility paper without me prompting; I wouldn't have made that connection alone
3. **Gap detection** — "You have papers on mDNS security, but nothing on *performance* implications. Should you?"
4. **Consistency validation** — Flagging contradictions (e.g., two papers claiming opposite things about mDNS latency)

### What AI Couldn't Do (And What I Did)

1. **Verify claim accuracy** — Claude can't judge whether Siddiqui 2012 truly supports claim-1; I read the papers and decided
2. **Resolve contradictions** — When two papers disagreed, Claude generated both edges; I chose which relationship made sense for Saturn
3. **Define semantics** — What does "supports" mean for Saturn? I decided; Claude executed
4. **Check descriptions for accuracy** — Auto-generated descriptions often missed nuance; I rewrote them

**Example:** Kim-Reeves 2020 discusses broad DNS vulnerabilities. Claude suggested it "supports" claim-1 because DNS is involved. But I refined it to "supports" because the threat model for mDNS-delivered credentials is specifically relevant to our ephemeral-key mechanism. The edge is correct, but the *reasoning* matters.

---

## Part 2: Claude as Thesis Advisor

### The Advisor Relationship

Starting in January 2026, I established a rolling conversation with Claude where:
- I describe an idea, draft, or problem
- Claude asks clarifying questions and offers suggestions
- I evaluate those suggestions in the context of Saturn's design and goals
- We iterate

This is *not* Claude writing the thesis. It's Claude helping me think through it.

### Advisor Roles

#### 1. Conceptual Feedback

Example 1: **Claim framing**

Me: "Claim 2 is about reducing configuration effort. But compared to what? If I'm configuring mDNS manually, Saturn is better. But if I'm using a cloud vendor's pre-configured AI platform, Saturn might be worse."

Claude: "Good catch. What's your comparison baseline?"

Me: "The status quo: developers using OpenAI API directly, managing API keys manually, no local fallback."

Claude: "Okay, so your claim is relative to that baseline. Does your evaluation measure against it?"

Me: "Not explicitly. I'm measuring discovery latency and steps to first inference. Should I add a cloud-vs-local time comparison?"

[Refined the evaluation plan]

This feedback didn't come from Claude's knowledge of networks. It came from Claude asking a clarifying question I hadn't asked myself.

#### 2. Argument Coherence

Example 2: **Cross-claim consistency**

Claude: "Claim 1 (mDNS feasibility) assumes routers can announce via mDNS. Claim 3 (security is addressable) includes a threat model where a rogue announcement lies about a service. But if announcements are just broadcasts, how do you prevent the lie?"

Me: "We don't, at the broadcast level. We rely on client-side validation and ephemeral keys. Let me rewrite the threat model to make that clear."

[Revised threat model, clarified the boundary between infrastructure and client responsibility]

Claude didn't know Saturn's security design. But asking "are these claims consistent?" surfaced an explanation gap.

#### 3. Writing Support

Example 3: **Chapter 1 draft**

Me: "Here's my intro paragraph. Does it work?"

> "The proliferation of local AI services creates a configuration burden. Existing solutions require either manual setup or centralized cloud platforms. We propose Saturn, a protocol for zero-configuration AI discovery and provisioning..."

Claude: "What's your target audience? Is this framed for systems researchers, practitioners, or policy makers?"

Me: "All three, but I lean toward practitioners—people building AI applications."

Claude: "Your draft speaks to the problem (config burden) but not to *who feels* it. Try:"

> "Developers building AI applications today face a choice: manually configure local LLMs (error-prone, time-consuming) or rely on cloud APIs (expensive, requires internet). We propose Saturn..."

Me: [Incorporated, reworded to match my voice]

This is Claude offering draft prose, not writing the thesis. I evaluated and refined.

### What AI Got Wrong (And What I Corrected)

#### 1. Overcomplexity

Claude sometimes suggested features that sounded sophisticated but weren't aligned with Saturn's goals:

Claude: "Why not include DRM (Digital Rights Management) to prevent unauthorized model access?"

Me: "Because Saturn's target is resource-constrained environments and developing countries. Adding DRM increases deployment friction. Pass."

[Rejected]

#### 2. Domain Knowledge Gaps

Claude sometimes lacked context on Saturn's specific design constraints. These gaps were caught during review and corrected. The three concrete rejected suggestions are documented in Part 4 below (fourth cost claim, Monte Carlo simulation, quantum threats).

### The Bottom Line: Advisor vs. Author

Claude made me a *better advisor* to myself, not an *author in disguise*. The thesis claims, design decisions, and evidence interpretation came from me. Claude helped me:
- Spot inconsistencies
- Articulate ideas more clearly
- Generate alternatives
- Challenge assumptions

---

## Part 3: AI in Evaluation Design

### Evaluation Complexity

Chapter 6 requires measuring whether Saturn's three claims hold:

1. **Claim 1 (Feasibility):** mDNS discovery works at scale
   - Measure: Discovery latency, failover time, success rate
2. **Claim 2 (Efficiency):** Configuration effort is reduced
   - Measure: Steps to first inference, retry logic, multi-target selection
3. **Claim 3 (Security):** Trade-offs are known and addressable
   - Measure: Threat model completeness (STRIDE), exposure analysis

These measures require:
- Precise, unambiguous grading criteria
- Comprehensive threat coverage
- Automated analysis of complex results

### Claude's Role

#### 1. Experiment Design Validation

Before running trials, Claude helped validate the design:

**Cognitive walkthrough**

Me: "Walk through the first-time user experience for Saturn discovery."

Claude:
1. User starts with local service IP unknown
2. Sends multicast query for `_saturn._tcp.local`
3. Router responds with TXT records (priority, endpoint, API key)
4. Client decodes TXT and connects to endpoint
5. Success: first inference achieved

Claude: "What happens if the router's response is slow? Does the client retry?"

Me: "Yes, mDNS has retry logic, but it's not guaranteed. Let me measure how often retry is needed."

[Added failover-time as a metric]

**STRIDE threat modeling**

Me: "Generate a STRIDE threat model for Saturn's beacon mode."

Claude:
- **Spoofing:** Router identity — can a rogue device claim to be Saturn?
- **Tampering:** TXT record integrity — can attacker modify announcements mid-flight?
- **Repudiation:** Who provisioned the key? Can the router deny it?
- **Information Disclosure:** Can a passive observer extract API keys from broadcasts?
- **Denial of Service:** Can attacker flood announcements or exhaust key quotas?
- **Elevation of Privilege:** Can a low-privilege client escalate to high-privilege access?

Me: [Reviewed against actual design] "Good start. But this misses **scope crossing**: our ephemeral keys are link-local, so cross-network access requires deliberate routing. Add that as a distinct assumption."

[Refined threat model, clarified assumptions]

#### 2. Grader Prompt Generation

The evaluation pipeline runs automated graders. Claude helped draft unambiguous prompts:

**Discovery-latency grader**

Prompt draft 1:
> "Measure how long it took for the client to discover the Saturn endpoint."

Problem: "Discover" is ambiguous. Does it mean:
- Time from query to first response?
- Time from query to fully parsed TXT records?
- Time from query to first successful connection?

Refined prompt:
> "Measure the time from mDNS query to first successful TCP connection to the Saturn endpoint. Include retry delays if applicable. Report in milliseconds."

**Config-steps grader**

Prompt draft 1:
> "Count the number of steps the user took to set up Saturn."

Problem: What's a "step"? Install packages? Edit config files? Run a command?

Refined prompt:
> "Count distinct user actions: (1) install Saturn binary/package, (2) configure router beacon settings, (3) run client software. Do not count subprocess steps (e.g., installing dependencies during package install). Report as integer 1-3."

These refinements happened through iteration:
- Claude drafted the prompt
- I identified edge cases
- Claude revised
- I tested on a small trial run
- Final prompt was precise enough for reliable grading

#### 3. Result Interpretation

After running trials, Claude helped interpret anomalies:

**Interpreting discovery latency variance**

Across 5 trials, discovery latencies were [9983, 8954, 8753, 8915, 9623]ms (median 8,954ms). These include Docker container overhead; pure mDNS discovery is likely <2s. Success rate was 100% (5/5) for both discovery and configuration effort.

Claude helped brainstorm why latencies varied across trials (container startup time, network initialization, mDNS retry timing). We traced the variance primarily to Docker overhead rather than mDNS protocol issues.

### What AI Helped and What It Missed

#### Helped:
- Brainstorming metric alternatives
- Drafting grader prompts (I refined them)
- Flagging ambiguous design choices
- Synthesizing results patterns

#### Missed or Required Correction:
- **Domain specificity:** Claude's threat model didn't account for link-local scope as a *security assumption*. I added it.
- **Practical constraints:** Claude suggested testing with 1000 concurrent clients; I knew our lab router maxed at ~100.
- **Evaluation priority:** Claude wanted to measure "latency across 100 network topologies." I focused on the 3 most realistic scenarios, given time constraints.

---

## Part 4: Where Human Judgment Overrode AI

### Decision 1: Claim Framing

**AI suggestion:** "Add a fourth claim about cost savings (money = deployment-hours saved)."

**My decision:** No. Saturn is framed as *equity* (access, not efficiency). Cost savings are secondary. The fourth claim would dilute focus.

### Decision 2: Evaluation Methodology

**AI suggestion:** "Use Monte Carlo simulation to predict large-scale performance."

**My decision:** No. Real trials with a physical router are more credible than simulation. Simulation is a risk if parameters are wrong.

### Decision 3: Threat Model Scope

**AI suggestion:** "Include threats from quantum computing to make the work future-proof."

**My decision:** No. Saturn's ephemeral keys are good enough for classic attacks; quantum threats are speculative for this scope.

### The Pattern

Claude is great at **generating options**. I'm responsible for **evaluating them in context**: Saturn's actual goals, constraints, and timeline.

---

## Conclusion: AI as Amplifier, Not Author

This thesis would exist without Claude, but it would be:
- **Slower to write** — organizing 20+ papers without structured support takes more time
- **Less coherent** — iterative feedback helped catch inconsistencies
- **More isolated** — cross-domain synthesis didn't happen naturally
- **Less defended** — reviewing critique (even from an AI) sharpened arguments

But the intellectual contribution is **human**: design choices, claim framing, evidence evaluation, and judgment calls.

Claude was a **tool for synthesis and refinement**, not a proxy for thinking.

---

## Recommendations for Readers

- If you want to understand **how claims connect to evidence**, navigate the moons graph (graph.json or viewer.html)
- If you want to understand **why specific design choices were made**, read the voice files (rationale narratives)
- If you want to evaluate **the quality of evidence**, read the cited papers (Chapter 2 bibliography)
- If you're **skeptical of AI-assisted work**, that's healthy — scrutinize the claims, check the papers, validate the experiment design

The thesis stands on Saturn's design and evidence, not on having used AI to develop it.
