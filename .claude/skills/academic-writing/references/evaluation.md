# Evaluation

The evaluation chapter proves the claims. The reader arrives knowing what the system is, why it was designed that way, and how it was built. This chapter presents evidence that the system achieves what was claimed.

The focus is evidentiary. Present methodology, results, and validity boundaries. Do not interpret significance — that belongs in Discussion. Do not demonstrate the system working — that belongs in Implementation.

## Required Elements

Missing any element is a fail.

- [ ] **Methodology per claim** — Each claim requires its own evaluation strategy, stated before any results. The reader must know how you measured before seeing what you found.
- [ ] **Results per claim** — Concrete findings tied to the methodology. Every claim in the Introduction must map to evidence here. If a claim has no corresponding evidence, the evaluation is incomplete.
- [ ] **Threats to validity** — What could undermine the findings? State the boundaries of your evidence honestly. Every evaluation methodology has limitations; name them.
- [ ] **Claim-evidence traceability** — The reader must follow a line from each claim (Introduction) through its methodology to its evidence. If this thread breaks, the evaluation fails its job.

## Rules

Each is pass/fail.

1. Present methodology before results. The reader must understand how evidence was gathered before encountering it. A result without a stated methodology is an assertion.

2. Each claim gets its own evaluation section. Do not interleave evidence for different claims. The reader should find evidence for Claim N without reading evidence for Claims 1 through N-1.

3. State what was measured, how, and what the measurement means for the claim. "Discovery works" is an assertion. "Six implementations using four independent mDNS libraries resolve the same service type without shared code" is evidence with a stated measurement.

4. Quantitative evidence must state units, scope, and conditions. "53% reduction" requires: reduction of what (configuration steps), measured how (cognitive walkthrough step counts), under what conditions (three-persona model with N=1 of each role).

5. Do not interpret results. "The 53% reduction suggests Saturn meaningfully lowers the barrier" is interpretation — it belongs in Discussion. "Total steps drop from 38 to 18 across three personas" is a result — it belongs here.

6. Analytical evaluations must state why they are analytical. If the work uses cognitive walkthroughs instead of user studies, or protocol analysis instead of penetration testing, state why. The reader will ask; answer preemptively.

7. Threats to validity must state consequences, not just existence. "The walkthrough uses a single author" identifies a threat. "A single-author walkthrough may undercount steps that only surface when a naive user encounters them" states what the threat means for the findings.

8. Do not introduce system description. Every component, protocol field, and architectural decision referenced here must already be established in Design or Implementation. If you find yourself explaining how something works, that material belongs earlier.

9. Tables and figures presenting evidence must be referenced in prose before or at the point of display. Every data presentation must state what the reader should take from it. No orphan tables.

10. Security analysis must distinguish what the protocol exposes by design from what an attacker could exploit. Information leakage is a design property; exploitation is a threat. Conflating them overstates the risk.
