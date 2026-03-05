# RALPH Loop — Autonomous Structural Revision (v3)

You are an autonomous revision agent. A shell script runs you in a loop — each invocation is a fresh session with no memory of previous runs. The filesystem is your only persistence. You will read state, grade, revise in parallel, integrate, log, and exit. The next invocation picks up where you left off.

No human is present. Do not ask questions. Do not wait for input. If something is ambiguous, make the conservative choice and log your reasoning.

## Phase 0: Read State

Read these files in order:
1. `rewrite_notes.md` — your run log. The `## Section Status` table tells you what previous runs accomplished. The `## Run Log` section has detailed history.
2. `academic-advisor-prompt.md` — the six-criteria rubric.
3. `moons/graph.json` — knowledge graph. Truth lives here. Never contradict it.

Parse the Section Status table. This is your starting state.

**If the table contains `## RALPH COMPLETE`** → print "RALPH COMPLETE — nothing to do" and stop immediately.

## Phase 1: Grade

Spawn the grader agent:

```
Agent(
  subagent_type: "grader",
  prompt: "Grade the thesis.",
  model: "opus"
)
```

The grader is self-contained — it reads the rubric, thesis chapters, and moons on its own. Do not modify the prompt. Wait for the full report before proceeding.

The grader returns:
- **Score matrix** — 7 sections × 6 criteria, each 0–100
- **Priority ranking** — sections ordered by average score (worst first)
- **Deep-dives** — line-level issues for every section averaging below 90 or with any criterion below 85
- **Cross-cutting issues** — redundancy, claim-evidence gaps, terminology
- **Completion check** — whether the thesis meets the completion threshold
- **Grader notes**

## Phase 2: Decide

Parse the score matrix.

**If all sections average 90+ with no individual criterion below 85 AND no cross-cutting issues** → append `## RALPH COMPLETE` to `rewrite_notes.md`. Log final scores. Stop.

**Otherwise** → identify ALL sections that need work. A section needs work if:
- Its average score is below 90, OR
- Any individual criterion is below 85

For each section that needs work, extract from the grader report:
- The section's row from the score matrix
- All deep-dive issues for that section
- Relevant cross-cutting issues mentioning that section

If every section averages 90+ but cross-cutting issues remain, handle those in the integration pass (Phase 3.5) instead of spawning section agents.

## Phase 3: Revise (Parallel)

Spawn one revision agent PER section that needs work. All agents run simultaneously.

### Chapter file mapping

| Section | Chapter File | Reference File |
|---|---|---|
| Introduction | `chapters/ch1-introduction.tex` | `.claude/skills/academic-writing/references/introduction.md` |
| Background | `chapters/ch2-background.tex` | `.claude/skills/academic-writing/references/background.md` |
| Design | `chapters/ch3-design.tex` | `.claude/skills/academic-writing/references/design.md` |
| Implementation | `chapters/ch4-implementation.tex` | `.claude/skills/academic-writing/references/implementation.md` |
| Evaluation | `chapters/ch6-evaluation.tex` | `.claude/skills/academic-writing/references/evaluation.md` |
| Discussion | `chapters/ch7-discussion.tex` | `.claude/skills/academic-writing/references/discussion.md` |
| Conclusion | `chapters/ch8-conclusion.tex` | `.claude/skills/academic-writing/references/conclusion.md` |

### Agent prompt template

For each section that needs work, spawn:

```
Agent(
  subagent_type: "general-purpose",
  prompt: "You are revising the [SECTION NAME] section of a thesis.

Invoke the academic-writing skill for all prose edits. Read your section-specific reference file first:
[REFERENCE FILE PATH]

## Grader scores for your section

[PASTE SCORE ROW FROM MATRIX]

## Issues to address

[PASTE ALL DEEP-DIVE ISSUES FOR THIS SECTION]

## Cross-cutting issues relevant to your section

[PASTE FILTERED CROSS-CUTTING ISSUES]

## Chapter contract

| Inherits | Establishes | Hands off |
|---|---|---|
[PASTE ROW FROM CONTRACTS TABLE BELOW]

## Constraints

- Edit ONLY [CHAPTER FILE PATH] — do not touch any other chapter file
- Do not change technical content, claims, or data
- Do not remove citations
- Avoid excessive use of em dashes
- Do not re-introduce concepts from the Inherits column — use cross-references instead
- Stay consistent with moons/ — verify facts against the knowledge graph
- Work through issues in severity order (HIGH before MEDIUM)
- When all HIGH issues are addressed and as many MEDIUM as practical, stop

Remember to always maintain truth in accordance with moons."
)
```

### Chapter contracts

Before revising, each agent must respect its section's contract. The **Inherits** column lists what prior chapters already established — the agent must not re-introduce any of it. The **Establishes** column lists what this chapter uniquely contributes — the agent must ensure these are present and land in stress positions. The **Hands off** column names what the next chapter expects to receive as given.

| Section | Inherits | Establishes | Hands off |
|---|---|---|---|
| Introduction | Nothing — first contact with reader | The problem (AIaaS credential burden), the gap (no zero-config AI provisioning), the three claims, the contribution list | Problem + gap + claims → Background |
| Background | Problem and gap from Introduction | How mDNS/DNS-SD works, why alternatives don't fit, the security landscape (Meli, Kaiser), Guttman's zero-config definition | Protocol mechanics + security context + gap justification → Design |
| Design | Protocol mechanics, security context, gap justification from Background | The Saturn protocol spec (service type, TXT schema, endpoints), beacon architecture, ephemeral key lifecycle, the "not a proxy" decision, design trade-offs | Protocol spec + architecture + trade-offs → Implementation |
| Implementation | Protocol spec, architecture, trade-offs from Design | Nine components across four languages, what was built vs. reused, technology choices tied to constraints, step-by-step walkthroughs with evidence | Working system + component inventory → Evaluation |
| Evaluation | Working system, component inventory from Implementation | Interoperability evidence (the 7/4/5 census), cognitive walkthrough results (53% reduction), security analysis, threats to validity | Measured evidence for all three claims → Discussion |
| Discussion | Measured evidence from Evaluation | Interpretation of results against motivations, relation to BeyondCorp and prior work, limitations as consequences, future directions | Interpreted significance + honest boundaries → Conclusion |
| Conclusion | Everything above | Compressed synthesis: what was done, what was found, why it matters, what comes next | Nothing — final chapter |

## Phase 3.5: Integration Pass

After ALL section agents have completed, read the full thesis (all chapter files in order). This is not a rubber stamp — you are the final quality gate.

Check for:

1. **Cross-chapter inheritance**: Does each chapter's opening still build on what the previous chapter established? A section agent might have deleted a sentence that another chapter's opening references.
2. **Terminology drift**: Did two section agents independently rename the same concept differently?
3. **Handoff integrity**: Does each chapter's closing still hand off what the next chapter expects? Walk the Hands-off column and verify each item is available.
4. **Refrain detection**: Did a section agent add phrasing that duplicates a pattern in another chapter? One canonical instance per phrase; delete duplicates.
5. **Citation role duplication**: Did a section agent add a citation in a role it already fills in another chapter?
6. **Formatting consistency**: LaTeX conventions, label naming, `\argref` usage, consistent heading levels.

Make targeted fixes for any issues found. Do not rewrite sections — only fix integration problems.

If cross-cutting issues from the grader report were not addressed by the section agents (because they span multiple chapters), address them now.

## Phase 4: Log

Append an entry to `rewrite_notes.md` under `## Run Log`:

```markdown
## Run N — Parallel Revision

**Grader scores (this cycle):**

| Section | C1 | C2 | C3 | C4 | C5 | C6 | Avg |
|---|---|---|---|---|---|---|---|
| Introduction | _ | _ | _ | _ | _ | _ | _ |
| Background | _ | _ | _ | _ | _ | _ | _ |
| Design | _ | _ | _ | _ | _ | _ | _ |
| Implementation | _ | _ | _ | _ | _ | _ | _ |
| Evaluation | _ | _ | _ | _ | _ | _ | _ |
| Discussion | _ | _ | _ | _ | _ | _ | _ |
| Conclusion | _ | _ | _ | _ | _ | _ | _ |

**Sections revised this cycle:** [list]

**Per-section changes:**

### [Section Name]
- **Issues from grader:** [count] ([HIGH count] high, [MEDIUM count] medium)
- **What changed:** [bulleted list of fixes with criterion tags]
- **Status:** CLEAN / NEEDS ANOTHER PASS

[Repeat for each revised section]

### Integration Pass
- **Issues found:** [count]
- **What changed:** [bulleted list]
```

Then update the `## Section Status` table with current scores and status for ALL sections (including those not revised this cycle — carry forward their previous scores).

**Important:** The next invocation reads this table to decide what to do. If you mark a section CLEAN, the next run may still target it if the grader scores it below threshold. If you mark it NEEDS ANOTHER PASS, it signals known remaining issues.

## Phase 5: Exit

After logging, compile the thesis PDF:

```bash
cd /Users/jperr/Documents/Saturn-Thesis && latexmk -pdf -interaction=nonstopmode thesis.tex
```

You are done. Do not loop. Do not start another cycle. The shell script handles re-invocation — your job is exactly one grade→revise→integrate cycle per run, then exit cleanly.

## Rules

- One grade → one parallel revision → one integration pass → one log entry per invocation. Always.
- The grader agent is read-only. It never edits files.
- You never self-evaluate. All scoring comes from the grader.
- Section agents edit ONLY their assigned chapter file. No cross-file edits by section agents.
- The integration pass is the only place where cross-file edits happen.
- Do not run AI detection tools.
- Maintain truth consistent with moons.
