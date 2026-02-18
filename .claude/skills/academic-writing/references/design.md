# Design

The design chapter is the blueprint of the system. It defines what the system is, what properties it must have, and why it is shaped the way it is. A competent engineer should be able to produce a conforming implementation from this chapter alone without consulting the author.

Design is not implementation. It specifies constraints and interfaces, not tools, versions, or build steps. If a detail only matters during construction, it belongs in the implementation chapter.

## Required Elements

Missing any element is a fail.

- [ ] **Goals** — What properties must the system achieve? State these before any design detail.
- [ ] **Audiences** — Who interacts with the system and in what roles? Name them early and use these roles consistently when describing behavior.
- [ ] **Concepts** — Every domain-specific abstraction the reader needs before understanding the protocol or architecture. Define each in one or two sentences with its purpose, not just its mechanism.
- [ ] **Protocol or interface specification** — Concrete, implementable detail: names, formats, fields, expected behaviors. A reader should be able to build a conforming implementation from this section alone.
- [ ] **Architecture decisions** — Each significant choice paired with its rationale and the alternative it beat.

## Rules

Each is pass/fail.

1. Present goals before mechanisms. The reader must know what problem a component solves before learning how it works. If a concept appears before its motivating goal, reorder.

2. Introduce every concept exactly once, in its own space, before using it elsewhere. If a term appears in the protocol spec, it must already be defined under concepts. Forward references break comprehension.

3. Justify every design choice against a named alternative. "We use mDNS" fails. "We use mDNS rather than a central registry because the system must operate without infrastructure" passes. If no alternative existed, say so — that is still a justification.

4. Specification details must be exact and testable. Field names, record formats, expected endpoints, and response behaviors need enough precision that two independent implementors would produce compatible systems. Vague specs ("the service should respond appropriately") fail.

5. Separate mechanism from policy. Describe what the system does (mechanism) distinctly from the rules governing when and why (policy). Mixing them forces the reader to untangle two concerns at once.

6. When a design choice creates a limitation or trade-off, state it immediately. Do not defer to the discussion chapter. The reader evaluating the design needs the trade-off in context.

7. Use consistent terminology. If you define something as a "beacon," never call it an "announcement" or "advertisement" later. One concept, one name.

8. Diagrams or protocol flows, if used, must be referenced in the prose and explained. Do not leave them for the reader to interpret independently.

9. The design must specify what kind of work it supports — experimental, theoretical, simulation-based, or engineering — and the tools or techniques it requires at the design level (not implementation level). Data collection and analysis approaches belong here if they are design constraints; specific tool versions do not.