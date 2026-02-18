# Background Section — Organized Notes

## Purpose

The background section proves the writer understands the problem domain. After reading it, the reader should trust the writer's competence and have enough context to evaluate the design and findings that follow.

This is not the introduction. The introduction garners attention and states purpose. The background is where the writer demonstrates knowledge.

This is not related work. It provides context for the problem, not a thorough survey of every paper in the space.

## Required Elements

- **Core principle** — Explain the fundamental problem domain from first principles. What is the core concept the reader must grasp?
- **Chosen approach (deep)** — Cover the approach the work actually uses in depth. The reader needs to understand how it works and why it fits.
- **Adjacent methods (brief)** — Name alternative approaches that exist in the same space. For each: name it, state why it was not used, move on. Do not explain how the alternative works in detail.
- **Gap** — What remains unsolved or unaddressed that this work targets.

## Ordering

1. Fundamentals of the domain
2. The chosen approach in depth
3. Alternatives briefly dismissed
4. The gap this work fills

Always explain the core principle of the problem before introducing any specific technology or method.

## What This Section Is Not

- **Not a textbook chapter.** Everything here serves the writer's specific problem. If a paragraph could appear in a general-purpose reference, it is too broad.
- **Not a literature dump.** Papers are not listed sequentially. Every reference connects to a narrative thread that leads to the writer's problem.
- **Not related work in disguise.** Individual papers do not get deep treatment. The focus is context, not survey.

## Brevity Rule for Alternatives

An alternative method gets enough space to name it and state why it does not fit. One to two sentences. Example pattern: "DHCP requires centralized infrastructure, which conflicts with the zero-configuration constraint." Not enough to explain how DHCP works internally.

## Relationship to Other Sections

- The **introduction** states the problem and why it matters. The background expands on the domain knowledge behind that problem.
- The **design** chapter specifies what the system is. The background gives the reader the prerequisite knowledge to evaluate that design.
- General writing rules from SKILL.md apply without modification. No overrides needed for this section.

## Scale

Depth depends on the reader. Write enough that the reader can follow the problem and evaluate the work. Demonstrate understanding without overexplaining. Conciseness signals mastery — padding signals insecurity.