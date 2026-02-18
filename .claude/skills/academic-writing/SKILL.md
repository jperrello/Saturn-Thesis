---
name: academic-writing
description: "Use this skill whenever writing prose, essays, academic content, reports, or any long-form written output, even if the user doesn't explicitly mention writing quality. Trigger for any drafting, revising, or editing of written sections — including when the user pastes text and asks for feedback."
---

# Academic Writing Skill

## General Writing Principles

Evaluate every draft against these rules. Each is pass/fail.

### Concreteness

1. Use concrete terms for concrete things, abstract terms for abstract things. When describing something observable — an action, mechanism, object — the most specific available word is the right one. "Behaved aggressively" could mean yelling, insulting, or throwing things; "punched" tells you exactly what happened.

2. Attach active verbs to clearly identified subjects. Minimize "was," "were," "is" as main verbs. If a reader can't tell who is doing the action, the clause fails.

3. When an action hides inside a noun — analysis, performance, implementation, discovery — and a verb form exists — analyze, perform, implement, discover — use the verb. The noun form buries the action and obscures who is doing it.

4. Break long sentences into shorter ones. Strip excess nouns, adjectives, and adverbs. If a word doesn't change the meaning, remove it.

### Reader-Centered Writing

5. Every sentence must either advance an argument, present evidence, or give the reader information they need. If it does none of these, cut it. Experts read academic work because they expect valuable information or ideas. If they don't find value quickly, they stop reading.

6. Never show that you "considered several approaches" or "thought through" a topic. The reader wants your conclusion and its justification, not a tour of your deliberation.
   - Bad: "We considered several approaches before deciding to use mDNS."
   - Good: "We use mDNS because it requires no infrastructure."

7. Before writing, ask: Who is my reader? What do they already know? What must I explain? What order prevents confusion? Where are the likely points of confusion that need extra care? Structure the section around those answers, not around the order you discovered things.

### Dialogic Framing

8. Before presenting your contribution, explicitly identify the existing conversation, controversy, or gap you're responding to, and frame your work as solving a problem readers perceive. This creates the instability that makes your writing valuable. Grab attention: debunk a myth, correct a misconception, challenge a popular interpretation. If you can't name what you're pushing back against, you haven't framed the work yet.

9. After any claim, finding, or design choice, explain why it matters. Be prepared to express the significance of your topic in a single sentence. Never leave the reader to infer the "so what."

### Structure

10. Paragraph beginnings and endings are natural emphasis points — readers pay the most attention there. Put your strongest claims, sharpest distinctions, and most important findings at these positions, not buried mid-paragraph.

11. Guide the reader with words and phrases that signal the relationship between ideas: *because, therefore, however, similarly, in contrast, specifically, above all, for example, although, having argued that...*. The reader should never have to guess how one idea connects to the next, but the transition should feel natural, not formulaic.

### Rigor

12. Each reference must appear in a sentence that states what the cited work found or argued. A bare trailing citation is insufficient.
   - Bad: "Service discovery matters for local networks \cite{smith2020}."
   - Good: "Smith~\cite{smith2020} showed that 73\% of LAN failures stem from misconfigured discovery."

13. Every technical term and acronym must be defined at first occurrence. Use the short form consistently afterward.

14. "Best," "most," "first," "unique," and "novel" require evidence in the same or immediately preceding sentence. If you cannot back it, cut it.

---

## Core Workflow

**MANDATORY for ALL writing output. Do NOT skip steps.**

Follow this loop every time you produce written prose:

### Step 1: Draft Freely

Write a complete first draft without self-censoring. Focus on getting ideas down with correct content and structure. Don't polish prematurely.

### Step 2: Evaluate the Draft

Run two evaluations on the draft you just produced:

1. **General checklist** — Evaluate against every principle listed in the General Writing Principles section above. Note each violation or weakness explicitly.
2. **Section-specific guidelines** — Read the corresponding reference file (see Section Routing below) and evaluate the draft against those guidelines. Note each violation or weakness explicitly.

Format the evaluation as a short internal list of concrete issues found. If no issues are found for a given principle, skip it — only list problems.

### Step 3: Revise Based on Evaluation

Address every issue identified in Step 2. Make targeted revisions to the draft. Each fix should correspond to a specific evaluation finding.

### Step 4: Present Only the Revised Version

Output the final revised text to the user. Do NOT show the raw first draft or the evaluation unless the user asks to see them.

---

## Section Routing

Before writing, identify which thesis section the work belongs to. Read the matching reference file and apply its guidelines alongside the general principles.

| Section        | Reference File                                                  |
| -------------- | --------------------------------------------------------------- |
| Abstract       | `.claude/skills/academic-writing/references/abstract.md`        |
| Introduction   | `.claude/skills/academic-writing/references/introduction.md`    |
| Background     | `.claude/skills/academic-writing/references/background.md`      |
| Design         | `.claude/skills/academic-writing/references/design.md`          |
| Implementation | `.claude/skills/academic-writing/references/implementation.md`  |
| Evaluation     | `.claude/skills/academic-writing/references/evaluation.md`      |
| Discussion     | `.claude/skills/academic-writing/references/discussion.md`      |
| Conclusion     | `.claude/skills/academic-writing/references/conclusion.md`      |

If the writing doesn't map to a specific section (e.g., general editing, standalone prose), apply only the general principles.
