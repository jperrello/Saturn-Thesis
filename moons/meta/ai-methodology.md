# Generative AI in Saturn Thesis Creation

**Brief summary:** Saturn's thesis was developed with iterative support from Claude (Anthropic), an LLM-powered advisor. This document explains three key roles AI played: authoring the structured knowledge graph (moons), serving as an iterative thesis advisor, and supporting evaluation design and interpretation.

## Why Document This?

Generative AI has become a fundamental research tool, yet its role in academic work is often opaque. By documenting how Claude supported Saturn's development, we:

1. **Increase transparency** — readers understand the thesis development pipeline
2. **Model responsible AI use** — show how to leverage AI for synthesis without outsourcing judgment  
3. **Ground the equity argument** — Saturn aims to democratize AI access; using AI transparently demonstrates belief in its accessibility benefits
4. **Acknowledge methodology** — structured knowledge management and iterative refinement are *methodological choices*, not shortcuts

---

## Three Components

### 1. Moons Knowledge Authoring
The `moons/` directory is a structured knowledge graph authored via iterative prompting with Claude. Rather than writing prose that might contradict itself, we:
- Decomposed claims into nodes (concepts, papers, components, chapters)
- Used Claude to generate candidate edges (relationships) and descriptions
- Manually reviewed and refined the graph for accuracy and consistency
- Iterated on the structure as new papers, ideas, and counterarguments emerged

This approach enabled **transparent argument scaffolding** — readers can follow the graph to see how claims connect to evidence.

### 2. Claude as Iterative Advisor
Claude served as a thesis advisor through ongoing conversation, providing:
- **Conceptual feedback** — "Does this framing match Saturn's goals?"
- **Argument coherence** — "Where do the three claims diverge?"
- **Writing support** — drafting sections, refining arguments, flagging gaps
- **Cross-domain synthesis** — connecting mDNS design to AI accessibility literature

This is distinct from *outsourcing judgment* — every recommendation was evaluated and either adopted, rejected, or refined by the human advisor (me).

### 3. AI in Evaluation
Claude supported the evaluation pipeline:
- **Experiment design validation** — checking STRIDE threat model completeness, cognitive walkthrough logic
- **Grader prompt generation** — writing robust, unambiguous prompts for automated result analysis
- **Result interpretation** — flagging anomalies, suggesting alternative explanations

---

## The Longer Story

See **Appendix A** for an extended walkthrough of:
- How moons emerged from initial chaos into structured argument
- The advisor feedback loop and when/why recommendations were rejected
- Evaluation system design and AI's role in grader reliability
- Limitations and moments where human judgment overrode AI suggestions
