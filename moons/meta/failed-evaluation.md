# Failed Evaluation (Archived)

Removed February 2026 after meeting with Adam.

## What It Was

An automated evaluation framework where Claude Code subagents acted as blind test participants. Three claims were tested:

- **Claim 1 (Discovery Feasibility):** Blind agents received "find and use an AI service on this network" with no Saturn knowledge. They ran in Docker containers with a Saturn beacon advertising Ollama via mDNS. 5 trials, all succeeded. Mean discovery latency ~9.2s (dominated by Docker orchestration overhead, not mDNS).

- **Claim 2 (Configuration Effort):** Control agent configured Open WebUI + Ollama manually (20 steps). Treatment agent used Saturn-enabled Open WebUI (7 steps). 65% step reduction. Also a cognitive walkthrough comparing OpenRouter (17 steps), LiteLLM (10), Ollama manual (8), Saturn (2).

- **Claim 3 (Security Analysis):** Passive packet capture of mDNS traffic during Saturn operation. tcpdump sidecar recorded 25 packets. Found 11 metadata fields exposed, zero credential material. STRIDE comparison against static API keys and OAuth. Exposure window analysis showing Saturn's 10-minute key lifetime vs unbounded static keys.

## How It Worked

- Docker Compose sandboxes spun up isolated environments per claim
- Blind subagents received only task descriptions (no grading criteria, no Saturn vocabulary)
- Automated graders (TypeScript) analyzed execution traces: discovery-latency, step-counter, artifact-counter, success-rate, exposure-analyzer
- A `trace` wrapper inside containers logged every command for post-hoc analysis
- Pilot batches of N=5, with Student's t confidence intervals and CV thresholds

The entire pipeline was orchestrated by a Claude Code skill (`/evaluate`) that could run all three claims in parallel using teams of subagents.

## Why It Was Removed

Joey delegated too much responsibility to the LLM agent. Claude designed the tests, wrote the grading scripts, built the Docker sandboxes, ran the experiments, and interpreted the results. Joey was not involved in the execution or design at a level where he could explain or defend the work.

When Adam asked in a meeting how the evaluation worked or what specific descriptions meant, Joey was unable to answer any of the questions. The evaluation existed as an artifact of agent output rather than as work Joey understood and owned.

This is the negative consequence of using AI agents irresponsibly — producing work you cannot explain or defend is worse than producing no work at all.

## What Survived

- The thesis claims (C1, C2, C3) remain valid and worth evaluating
- The threat model content in Chapter 7 (corporate exfiltration, untrusted admin, rogue registration, ISP injection) was written with more human involvement and may be reusable
- The STRIDE framework and exposure window analysis concepts are sound, just need to be redone with Joey's involvement
