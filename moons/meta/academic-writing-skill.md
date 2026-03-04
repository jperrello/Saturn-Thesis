# Academic Writing Skill

Claude Code skill that governs all thesis prose generation and revision. Invoked automatically when agents write or edit thesis sections.

## Problem it solves

Even with moons providing full Saturn knowledge, agents wrote bad academic prose. Output followed repetitive structure, cherry-picked information without cohesion, and read like "pulling slips of paper out of a hat." One-shotting a thesis section or even dividing into sections and prompting individually produced text where sections repeated each other or read as if written without knowledge of adjacent sections.

## Architecture

Two-part system:

1. **General rules** — five categories of writing principles, applicable to any academic writing (not Saturn-specific):
   - **Concreteness** — lead with specific examples, mechanisms, scenarios
   - **Reader-Centered Writing** — serve the reader's learning path, not the author's timeline
   - **Dialogic Framing** — engage with counterarguments and alternative perspectives
   - **Structure** — vary paragraph and section structure to avoid formulaic patterns
   - **Rigor** — every claim backed by evidence, every trade-off stated honestly

2. **Section-specific reference files** — markdown files with additional rules for writing specific thesis sections (abstract, introduction, evaluation, etc.). The main skill body directs the agent to read the file for whatever section it's currently writing.

3. **Core workflow** — draft → evaluate → revise → present revision

## Origin

Written Feb 16, 2026 by Joey with research assistance from Claude. The five rule categories came from research into academic writing best practices, not from the RALPH detection runs (though Run 0's distilled principles overlap and reinforce them).

## Design choice: no Saturn content

The skill deliberately contains no mention of Saturn. The rules apply to academic writing generally. Saturn knowledge comes from moons; writing quality comes from this skill. Separation of concerns.
