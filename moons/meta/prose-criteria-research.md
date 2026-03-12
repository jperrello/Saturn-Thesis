# Prose Criteria Research

The five prose criteria (P1–P5) in the grader agent are grounded in published research on writing craft. These are not subjective aesthetic preferences — they describe empirically validated reader-comprehension mechanics.

## Sources

### Gopen & Swan — "The Science of Scientific Writing" (1990)
**Informs:** P1 (Information Flow)

Readers have hard-wired expectations about where information appears in a sentence:
- **Topic position** (beginning): old information that links backward, giving context
- **Stress position** (end): new information the writer wants the reader to emphasize

The old-to-new contract: "Put in the topic position the old information that links backward; put in the stress position the new information you want the reader to emphasize."

Key finding: when writers violate these expectations, readers misinterpret the intended emphasis — they emphasize whatever lands in the stress position, regardless of the writer's intent.

### Joseph Williams — *Style: Lessons in Clarity and Grace*
**Informs:** P1 (Information Flow), P4 (Rhetorical Effectiveness)

Formalized two distinct properties:
- **Cohesion**: old-to-new flow *between* sentences. Each sentence begins where the last ended.
- **Coherence**: consistent topic strings *across* paragraphs. The reader always knows what the paragraph is "about."

Key finding: readers process cohesive text faster and retain more. A structurally perfect section with broken cohesion reads like a bulleted list disguised as paragraphs.

### Helen Sword — *Stylish Academic Writing* / "Zombie Nouns"
**Informs:** P2 (Voice and Agency)

"Zombie nouns" are nominalizations that "cannibalize active verbs, suck the lifeblood from adjectives, and substitute abstract entities for human beings."

Key finding: LLM revision loops tend to *increase* nominalization density. PNAS research (2024) shows LLM-generated text is characteristically noun-heavy and informationally dense — the opposite of vivid prose. A grader that rewards conciseness (C7) and value density (C6) without a prose counterweight could accidentally reward zombie prose.

### Steven Pinker — *The Sense of Style* (2014)
**Informs:** P2 (Voice and Agency), P5 (Concrete Grounding)

**Classic style**: the writer sees something the reader hasn't noticed and orients the reader's gaze so they see it for themselves. The purpose of writing is presentation; the motive is disinterested truth.

Anti-patterns: metadiscourse, excessive signposting, hedging, professional narcissism, clichés, zombie nouns, unnecessary passives.

Key finding: a structurally-focused revision loop can *introduce* these anti-patterns. Satisfying "ordering serves the reader" (C3) leads to more signposting. Satisfying "design intent" (C4) produces formulaic "we chose X rather than Y because Z" patterns.

### John Swales — CARS Model (1990)
**Informs:** P4 (Rhetorical Effectiveness)

The Create a Research Space (CARS) model describes rhetorical moves in academic writing:
1. Establishing a territory (claiming centrality, reviewing prior work)
2. Establishing a niche (identifying a gap, raising a question)
3. Occupying the niche (stating contribution, outlining structure)

Key finding: effective academic paragraphs make identifiable *moves* in an argument. Paragraphs that list facts without argumentative purpose fail to engage the reader regardless of structural correctness.

## Why This Matters for RALPH

The original grader (v3) evaluated only structure (C1–C7). What gets measured gets managed; what doesn't get measured gets destroyed. Without prose criteria, the RALPH loop was at risk of converging on structurally excellent but prosetically dead text — correct but lifeless, like a building with perfect engineering but no architecture.

The v4 grader adds P1–P5 to create productive tension with the structural criteria. C7 says "fit the page budget" while P3 says "maintain sentence variety." The writer must find solutions that satisfy both — which forces actual rewriting rather than mere truncation.
