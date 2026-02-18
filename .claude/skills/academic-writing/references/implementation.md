# Implementation

The implementation chapter demonstrates that the system exists and functions. The reader arrives here knowing what the system is and why it is shaped that way. This chapter shows them the system alive.

The focus is demonstrative, not analytical. Show the reader the constructed system, the concrete technology decisions that brought it to life, and proof that it meets its goals.

## Required Elements

Missing any element is a fail.

- [ ] What did you build versus what you reused? Identify major dependencies and frameworks at a surface level — enough for the reader to understand the foundation without losing focus on your original work.
- [ ] Where the system required a concrete tool, library, or platform, state what you chose and why. Each choice must reference the goal or constraint it satisfies.
- [ ] Step-by-step demonstrations of the system performing its core tasks. Each walkthrough must map to a system goal. The reader should finish each one convinced that the corresponding goal is met.
- [ ] Screenshots, terminal output, or other visual evidence of the system running. Every figure must be referenced in the prose and tied to a specific walkthrough step or goal. No orphan figures.

## Rules

Each is pass/fail.

1. Every walkthrough must trace back to a named system goal. If a walkthrough does not demonstrate a goal, it has no purpose in this chapter. If a goal has no walkthrough, the implementation is incomplete.

2. Technology choices must reference the constraint they satisfy. "We used SQLite" fails. "We used SQLite because the system requires a persistent store that supports concurrent reads" passes. The link from choice to constraint must be explicit.

3. State what you reused before stating what you built. The reader needs the foundation before they can understand the contribution. Dependencies first, original work second.

4. Every figure must appear in the prose before or at the point where it is displayed. A figure the reader encounters without context forces them to guess what they are looking at. Reference it, explain what it shows, then present it.

5. Walkthroughs must describe what the user or system does at each step and what the observable outcome is. "The service is discovered" fails. "The client broadcasts an mDNS query, the host responds with an A record, and the client displays the resolved address in the service list" passes.

6. Do not introduce new terminology. Every concept used in this chapter should already be familiar to the reader. If you find yourself defining a new term, it likely belongs earlier in the paper.

7. Keep walkthroughs in the order a user or operator would encounter them. If the system has a setup phase, a runtime phase, and a teardown phase, present them in that order. Organize by experience, not by component.

8. If the implementation deviates from the original plan, state the deviation, state why, and state the consequence. Do not silently diverge.

9. Do not measure or compare. This chapter demonstrates that the system works, not how well it works. If you catch yourself reporting benchmarks, percentages, or comparisons against alternatives, that work belongs elsewhere.

10. Explain dependencies only enough to establish context. A sentence or two on what a framework provides is sufficient. Deep explanations of tools you did not build distract from your contribution.