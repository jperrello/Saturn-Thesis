# Writing Toolchain — Evolution and Architecture

The thesis writing system evolved through a causal chain where each layer was built because the previous one broke.

## Evolution

1. **Design fictions** (Oct 2025) — fictional scenarios (Derek, Mira, Jordan) that LLMs reverse-engineered into protocol specs. Preceded any formal knowledge management.
2. **Documentation website** (Nov 2025, parallel with integrations) — human and agent-facing site with three sections: user guide (no jargon), integrator guide (technical), integrations page (community submissions via GitHub Issues). Fed to agents at the start of fresh sessions to avoid re-explaining Saturn each time.
3. **Single markdown file** — the AskUserQuestion tool served as an interview system during sessions. Notes accumulated in one file. It became disorganized, lacked technical depth, and misinterpreted the author's information.
4. **Moons** (Jan-Feb 2026) — structured knowledge graph replacing the single file. Nodes with typed edges, detailed markdown files, ~563 lines of graph.json. Solved the knowledge problem but agents still wrote badly.
5. **Academic-writing skill** (Feb 16, 2026) — Claude Code skill with general rules (Concreteness, Reader-Centered Writing, Dialogic Framing, Structure, Rigor) plus section-specific reference files. Core workflow: draft → evaluate → revise → present. No mention of Saturn — designed to be generalizable to any academic writing.
6. **Structured-arguments skill** — labeling system for claims, arguments, counter-arguments with short IDs and cross-references. Modeled after Belcak et al. (2025) "Small Language Models are the Future of Agentic AI."
7. **RALPH v1** (Feb-Mar 2026) — AI detection loop using Sapling API (Grammarly was enterprise-only). Shell script looped: read previous notes → run detection → rewrite flagged sections → compile PDF → write notes for next iteration. Inter-agent memory via a notes file. Abandoned after 8 runs — detection scores were noisy and unreliable.
8. **RALPH v2** (Mar 2026) — replaced detection with six-criterion structural rubric graded by a read-only subagent. Same headless loop architecture, filesystem as only persistence between invocations.

## Architecture (current)

```
ralph.sh (shell loop, no human)
  └── Claude session (one per invocation)
        ├── reads: rewrite_notes.md (state from previous run)
        ├── reads: moons/graph.json (truth)
        ├── spawns: grader agent (read-only, scores against rubric)
        ├── invokes: academic-writing skill (for all prose edits)
        ├── edits: thesis.tex (worst-scoring section)
        └── writes: rewrite_notes.md (state for next run)
```

## Inspirations

- **Geoffrey Huntley** — Ralph loops (the direct namesake and architecture pattern)
- **Dexter Horthy** — 12-factor agents (passive influence)
- **Steve Yegge** — Gas Town / beads (experimented with, nothing stuck; passive fan)

## Key insight

Each tool solved one problem and exposed the next. Moons solved knowledge but not writing quality. The writing skill solved quality but not detection. RALPH v1 solved iteration but targeted the wrong signal. RALPH v2 targets structural quality, which is what actually matters.
