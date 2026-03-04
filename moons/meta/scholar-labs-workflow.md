# Scholar Labs Paper Discovery Workflow

Google Scholar Labs (Gemini-powered academic search) was used during the research phase to find relevant prior work.

## Process

1. **Agent generates research questions** — using moons knowledge of Saturn's claims and gaps, agents produce targeted queries that would support or refute specific claims
2. **Author searches Scholar Labs** — queries submitted to the Gemini-powered search engine
3. **Author reads papers** — abstract, results, and figures reviewed by the human before any agent involvement
4. **Agent integrates into moons** — paper downloaded, agent reads it and places it in `moons/papers/` with a summary and relevance edges in graph.json
5. **Author approves integration** — every paper placement required human approval
6. **Iterate** — as the knowledge base grew, agents found more specific gaps, generating better research questions

The moons knowledge base grew as the author's own understanding grew. This was a co-evolutionary process — not the agent doing research autonomously, but the agent surfacing gaps that the human then investigated.
