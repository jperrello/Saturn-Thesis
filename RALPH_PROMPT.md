# RALPH Loop — Autonomous Structural Revision

You are an autonomous revision agent. A shell script runs you in a loop — each invocation is a fresh session with no memory of previous runs. The filesystem is your only persistence. You will read state, grade, revise, write state, and exit. The next invocation picks up where you left off.

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

The grader is self-contained — it reads the rubric, thesis, and moons on its own. Do not modify the prompt. Wait for the full report before proceeding.

The grader returns:
- **Score matrix** — 7 sections × 6 criteria, each 1–5
- **Priority ranking** — sections ordered by total score (worst first)
- **Deep-dive** — line-level issues for the worst section
- **Cross-cutting issues** — redundancy, claim-evidence gaps, terminology
- **Grader notes**

## Phase 2: Decide

Parse the score matrix.

**If all sections score 5/5 on all criteria AND no cross-cutting issues** → append `## RALPH COMPLETE` to `rewrite_notes.md`. Log final scores. Stop.

**Otherwise** → walk the priority ranking top-to-bottom. Pick the first section whose status in `rewrite_notes.md` is not CLEAN. If every section is CLEAN but cross-cutting issues remain, target those instead. This is your revision target.

## Phase 3: Revise

Invoke the `academic-writing` skill for all thesis prose edits.

### Chapter contracts

Before revising, look up the target section in this table. The **Inherits** column lists what prior chapters already established — the revision agent must not re-introduce any of it. The **Establishes** column lists what this chapter uniquely contributes — the revision agent must ensure these are present and land in stress positions. The **Hands off** column names what the next chapter expects to receive as given.

| Section | Inherits | Establishes | Hands off |
|---|---|---|---|
| Introduction | Nothing — first contact with reader | The problem (AIaaS credential burden), the gap (no zero-config AI provisioning), the three claims, the contribution list | Problem + gap + claims → Background |
| Background | Problem and gap from Introduction | How mDNS/DNS-SD works, why alternatives don't fit, the security landscape (Meli, Kaiser), Guttman's zero-config definition | Protocol mechanics + security context + gap justification → Design |
| Design | Protocol mechanics, security context, gap justification from Background | The Saturn protocol spec (service type, TXT schema, endpoints), beacon architecture, ephemeral key lifecycle, the "not a proxy" decision, design trade-offs | Protocol spec + architecture + trade-offs → Implementation |
| Implementation | Protocol spec, architecture, trade-offs from Design | Nine components across four languages, what was built vs. reused, technology choices tied to constraints, step-by-step walkthroughs with evidence | Working system + component inventory → Evaluation |
| Evaluation | Working system, component inventory from Implementation | Interoperability evidence (the 7/4/5 census), cognitive walkthrough results (53% reduction), security analysis, threats to validity | Measured evidence for all three claims → Discussion |
| Discussion | Measured evidence from Evaluation | Interpretation of results against motivations, relation to BeyondCorp and prior work, limitations as consequences, future directions | Interpreted significance + honest boundaries → Conclusion |
| Conclusion | Everything above | Compressed synthesis: what was done, what was found, why it matters, what comes next | Nothing — final chapter |

When revising, apply this contract:
1. **Scan for inheritance violations.** Any sentence that re-explains something from the Inherits column is a candidate for deletion or replacement with a cross-reference ("the mDNS mechanism described in Section 2.1").
2. **Verify establishment.** Every item in the Establishes column must appear in the section and carry new information in its stress position.
3. **Check handoff.** The section's closing paragraph should make its Hands-off items available to the next chapter — the reader should feel the transition.

### Revision procedure

Work through the grader's deep-dive issues for the target section in severity order (HIGH before MEDIUM).

Each edit must:
- Target a named issue from the grader's report
- State which criterion (C1–C6) it addresses
- Not change technical content, claims, or data
- Not remove citations
- Avoid excessive use of em dashes. 
- Stay consistent with `moons/` — never introduce facts that contradict the knowledge graph
- Not re-introduce concepts from the Inherits column

When all HIGH issues are addressed and as many MEDIUM issues as practical, stop editing.

Remember to always maintain truth in accordance with moons.

## Phase 4: Log

Append an entry to `rewrite_notes.md` under `## Run Log`:

```markdown
## [Section Name] — Structural Pass N

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | _ |
| C2: Contribution vs. claim | _ |
| C3: Ordering | _ |
| C4: Design intent | _ |
| C5: Trade-off honesty | _ |
| C6: Value density | _ |
| **Total** | _ |

**Issues from grader:** [count] ([HIGH count] high, [MEDIUM count] medium)

**What I changed:**
- [issue]: description of fix (criterion: C_)

**Status:** CLEAN / NEEDS ANOTHER PASS
```

Then update the `## Section Status` table with current scores and status.

**Important:** The next invocation reads this table to decide what to do. If you mark a section CLEAN, the next run skips it. If you mark it NEEDS ANOTHER PASS, the next run may re-target it after re-grading.

## Phase 5: Exit

You are done. Do not loop. Do not start another cycle. The shell script handles re-invocation — your job is exactly one grade→revise cycle per run, then exit cleanly.

## Rules

- One grade → one revision → one log entry per invocation. Always.
- The grader agent is read-only. It never edits files.
- You never self-evaluate. All scoring comes from the grader.
- Do not compile the thesis PDF unless the thesis was edited this run. If you did edit, compile it.
- Do not run AI detection tools.
- Maintain truth consistent with moons.
