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
1. Always `Read(moons/graph.json)` first. It gives you the full node/edge map in ~200 lines.
2. Follow edges to specific content files only when you need depth.
3. After interviews or new information, update both the relevant content file AND graph.json edges.
4. Keep graph.json lean — short descriptions, not full content. Depth lives in the files.

**Moons is the workspace. thesis.tex is the submission.** Moons organizes thinking; thesis.tex is the final output.

### Writing

You should be envoking the academic-writer skill when the user asks to edit the thesis. When you edit the thesis latex file, make sure to compile it to a pdf so the user can easily verify your output.