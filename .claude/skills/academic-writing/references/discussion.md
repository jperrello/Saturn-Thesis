# Discussion

The discussion ties the work together. The reader arrives here knowing what the system does, how it was built, and how it performed. This chapter explains what all of that means — how the results connect back to the original motivations, what the work accomplished in the context of the problem domain, and what remains to be done.

The focus is interpretive, not demonstrative or analytical. Connect findings to motivations, situate the work in the broader landscape, and look forward.

## Required Elements

Missing any element is a fail.

- [ ] What did the work accomplish relative to its original motivations? Restate the core problem briefly, then explain how the results address it. The reader must see the thread from motivation to outcome.
- [ ] How do the findings relate to existing work in the domain? State whether results confirm, extend, or contradict what others have found, and explain why.
- [ ] What are the limitations of this work? State the boundaries honestly — scope constraints, validity threats, assumptions that may not generalize.
- [ ] What should be done next? Identify specific, concrete directions for future work grounded in what this study revealed.

## Rules

Each is pass/fail.

1. Interpret, do not restate. The evaluation already presented the data. Repeating that "latency dropped from 320 ms to 180 ms" without explaining what that means for the problem is redundant. State what the numbers tell us about the original question.

2. Every interpretation must trace back to a stated motivation or research question. If a paragraph does not connect a finding to a reason the work was undertaken, it has no purpose in this chapter.

3. Distinguish between what the data supports and what you speculate. Use hedged language — "suggest," "indicate," "is consistent with" — for interpretations that go beyond direct measurement. "Prove," "demonstrate conclusively," and "establish" overstate what a single study can do.

4. Engage with prior work substantively. "Our results are consistent with Smith (2020)" is a bare assertion. "Smith (2020) reported discovery times under 250 ms for networks up to 1,000 nodes; our results extend this finding to 5,000 nodes, suggesting the protocol scales beyond previously tested limits" connects, compares, and advances.

5. Do not introduce new results. Every finding discussed here must already appear in the evaluation. If you discover something worth reporting while writing the discussion, move it to the evaluation first.

6. Present limitations as facts, not apologies. "Unfortunately, we were only able to test on four nodes" is defensive. "The evaluation used a four-node cluster; behavior at larger scales remains untested" is informative. Every study has boundaries — state them and move on.

7. Limitations must state their consequence. "The sample size was small" identifies a constraint but does not explain its impact. "The four-node cluster may not reveal contention effects that emerge at larger scales" tells the reader what the limitation means for the findings.

8. Future work must be specific and grounded in the current results. "More research is needed" is filler. "Testing discovery latency on networks above 10,000 nodes would reveal whether the linear scaling observed in our experiments holds at production scale" gives the next researcher a concrete starting point.

9. Do not re-explain the system. The reader already knows how it works. If you find yourself describing architecture or walking through components, that material belongs earlier in the paper.

10. Close with the strongest statement of what this work means for the domain. The final paragraph should leave the reader with a clear understanding of the contribution's significance — not a list of future work or a restatement of limitations.