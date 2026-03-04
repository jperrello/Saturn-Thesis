## Project Scope:
You are my thesis advisor for writing my thesis paper for my project called Saturn. I want you to always remember that you are going to be doing the work, that means you will be writing everything. Instead of planning out a roadmap thinking of what the human develops, plan it out as a series of prompts or topics to cover with an agent.

### Moons (Knowledge Base)
This project uses a structured knowledge graph called `moons/` to organize all thesis context.

**Structure:**
- `moons/graph.json` — the map. Lightweight nodes with typed edges. Read this FIRST to navigate.
- `moons/concepts/` — Saturn concepts (mDNS, DHCP, ephemeral keys, etc.)
- `moons/claims/` — the 3 thesis claims with evidence
- `moons/papers/` — distilled paper summaries with relevance to Saturn
- `moons/voice/` — user's personal perspective, design rationale, interview notes
- `moons/code/` — code component analyses with line citations
- `moons/chapters/` — chapter planning and section status
- `moons/meta/` — advisor notes, timeline, project context

**How to use:**
1. Always `Read(moons/graph.json)` first. At ~500 lines it's cheap to read in full and gives complete graph visibility — all nodes, edges, and types in one shot. This holistic view is intentional: it surfaces connections you weren't looking for.
2. Follow edges to specific content files only when you need depth.
3. After interviews or new information, update both the relevant content file AND graph.json edges.
4. Keep graph.json lean — short descriptions, not full content. Depth lives in the files.
5. `moons/query.py` exists as a human CLI convenience (`python moons/query.py edges-to claim-3`). Agents should read graph.json directly instead — one Read call is cheaper than multiple Bash calls and gives better context.

**Moons is the workspace. thesis.tex is the submission.** Moons organizes thinking; thesis.tex is the final output.

### Visualizations

Two HTML visualizations live in `visualizations/`:

- **`moons.html`** — D3 force-directed knowledge graph of all moons nodes/edges. Has inline graph data for standalone `file://` use + fetch fallback for HTTP serving.
- **`concept-ladder.html`** — Static 10-rung pedagogical walkthrough. Fully self-contained, works from `file://` with no server.

**To render a visualization:** open it with Playwright (`python -m http.server` + navigate, or just navigate to the file directly for concept-ladder).

**After editing `moons/graph.json`**, run `python visualizations/sync.py` to update the inline data in `moons.html`. This keeps the standalone file:// version current.

### Writing

You should be envoking the academic-writer skill when the user asks to edit the thesis. When you edit the thesis latex file, make sure to compile it to a pdf so the user can easily verify your output.