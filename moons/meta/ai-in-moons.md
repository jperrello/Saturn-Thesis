# AI in Moons: Knowledge Graph Authorship

**Summary:** The moons knowledge graph (nodes, edges, descriptions) was authored iteratively with Claude. This note documents how that process worked and what it enabled.

## The Problem Moons Solved

Saturn research generated:
- 20+ academic papers (many tangential, some contradictory)
- 6 implementation components (each touching multiple claims)
- 3 major thesis claims (with overlapping evidence)
- Design rationale across voice files, meeting logs, sketches

Organizing this required tracking:
- Which papers support which claims?
- Which components demonstrate which claims?
- Where do we *contrast* with existing work?
- How do concepts nest and relate?

A flat document couldn't answer these queries efficiently. **Moons became a queryable, visually navigable knowledge structure.**

## The Authorship Process

### Phase 1: Scaffold (Oct 2025)
Claude and I defined the node types (concept, claim, paper, component, chapter, voice, meta, person) and initial edge semantics (supports, contrasts, cited_in, demonstrated_by, etc.).

### Phase 2: Bulk Generation (Nov 2025 - Dec 2025)
For each claim, I'd run a conversation like:
```
Me: "What papers support claim-1 (mDNS feasibility)?"
Claude: "Guttman 2001, Siddiqui 2012, Siljanovski 2014. Konings 2013 relates to beacons. Kim-Reeves 2020 discusses mDNS security."
Me: "Generate edges for those relationships."
Claude: [Produces JSON edges]
Me: [Manually integrates, refines descriptions, adds missing papers I found]
```

### Phase 3: Refinement (Jan 2026 - Feb 2026)
- **Consistency pass:** Do edge directions make sense? (supports vs. related vs. contrasts)
- **Gap detection:** "What's missing between concept X and claim Y?"
- **Description quality:** Rewrite auto-generated descriptions to be tighter and more precise

### Phase 4: Live Updates
After each advisor meeting or new insight, update both the content file *and* graph.json edges. This keeps moons a **living knowledge base**, not a frozen artifact.

## Why This Matters for Saturn

**Moons enabled transparent argument architecture.**
- A reader can follow edges: claim-1 → supporting papers → concept definitions → implementation components
- Design decisions are visible: Why do we contrast with BeyondCorp? See the edge and the rationale file.
- Cross-domain connections surface naturally: How does the equity argument (papers on AI access) connect to the technical claims? Follow the edges.

**Claude's role was scaffolding and synthesis, not judgment.**
- Claude suggested edges; I verified them.
- Claude drafted descriptions; I refined them.
- Claude flagged missing connections; I evaluated their relevance.

Without AI-assisted scaffolding, maintaining this graph manually would have been a much slower, more error-prone process. *With* it, we iterated faster while maintaining rigor.

---

See also: **ai-methodology.md** (overview), **Appendix A** (extended walkthrough).
