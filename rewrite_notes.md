# RALPH Rewrite Notes

Running log of thesis revision cycles. Run 0 distills writing principles from an earlier detection-based approach (Runs 1–8, now archived). Current runs use rubric-based structural review (see `academic-advisor-prompt.md` and `RALPH_PROMPT.md`).

## Section Status

| Section | Status | Last Pass |
|---|---|---|
| Introduction | PENDING | — |
| Background | PENDING | — |
| Design | PENDING | — |
| Implementation | PENDING | — |
| Evaluation | PENDING | — |
| Discussion | PENDING | — |
| Conclusion | PENDING | — |

---

## Run Log

## Run 0 — Writing Principles (distilled from Runs 1–8)

Runs 1–8 chased AI detection scores. The scores were noisy and the strategy was abandoned, but the revision cycles surfaced real writing problems. These principles are what survived:

**Section-level texture over sentence-level fixes.** When every paragraph follows the same template (topic sentence → evidence → citation → significance), the section reads as formulaic regardless of how good individual sentences are. Adjacent paragraphs should be structurally dissimilar.

**Cut meta-commentary.** "This section specifies...", "The literature corroborates...", "Three claims follow:", "Chapter 2 established two facts:" — these narrate the paper's structure instead of making arguments. Delete them.

**Concrete before abstract.** Lead with the scenario, example, or mechanism. Then cite. A developer juggling three API keys is more informative than "credential fragmentation is a known problem (Syed 2024)."

**Vary citation integration.** Four consecutive Author-verb-finding sentences read as a citation parade. Mix trailing cites, evidence-then-cite, and embedded references. Merge where possible.

**Kill formulaic enumerations.** First/Second/Third lists, triple-colon patterns, balanced antithesis ("X is not Y. It is Z."), and numbered "three pillars" constructions are structural clichés. Break them into dissimilar forms.

**Earned specificity.** Port 5353, `/api/tags`, MIPS processors, "ten minutes after issuance" — concrete details beat vague claims like "well-established protocols" or "widely deployed infrastructure."

**Vary internal structure across subsections.** If every subsection in a chapter follows define→explain→justify, the chapter is monotonous even if each subsection is individually clear. Reverse the order, lead with a negation, open with a scenario, open with a concession — make each subsection's skeleton different.

*New entries appended below after each review → revision cycle.*
