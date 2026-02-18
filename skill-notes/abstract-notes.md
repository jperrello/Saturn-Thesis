# Abstract Reference File — Organized Notes

## Purpose

An abstract is a brief summary of a paper written to let readers decide if the paper contains information relevant to their work. Every word must earn its place or be cut.

## Constraints

- 150–200 words.
- No citations.
- Every term must be understandable without reading the full paper.
- Typically a single paragraph.

## Required Elements

An abstract must contain all five of the following. Order is flexible, but a natural default follows IMRAD (Introduction, Methods, Results, Discussion):

1. **Problem or gap** — What question or problem does this work address?
2. **Significance** — Why does the problem matter?
3. **Methods or approach** — What did you do?
4. **Findings or results** — What did you find? State outcomes, not promises.
5. **Implications** — What do the findings mean for the reader's world?

## Drafting Strategy

- Write 1–2 sentences per element as a baseline. This naturally produces the right length.
- Draft the abstract after the paper is finished. Condense each major section rather than writing from memory.

## How General Writing Principles Apply Under the Word Constraint

The general principles from SKILL.md are not relaxed for abstracts. Some are amplified, some are compressed, and some shift in application:

- **Concreteness** — Fully applies. At 150–200 words every vague word wastes a larger percentage of space. Active verbs, specific subjects, no nominalizations.
- **Reader-centered writing** — This is the entire purpose of an abstract. No exemptions.
- **Dialogic framing** — Compresses to one sentence (the problem/gap statement) rather than a full paragraph. Still required.
- **Rigor** — No citations in abstracts. Technical terms still defined at first use. Superlatives ("first," "novel," "unique") still require justification, but that justification must fit within the word constraint.
- **Structure (paragraph emphasis)** — Most abstracts are a single paragraph, so the "beginning and ending are emphasis points" rule applies to the abstract as a whole: open with the strongest framing of the problem, close with the strongest statement of implications.

## Common Failures

These are abstract-specific mistakes the agent should watch for:

- **Teasing instead of stating.** "Results are discussed" or "findings are presented" tells the reader nothing. State the actual results.
- **Restating the title.** The first sentence should not be a rephrasing of the title. It should establish the problem or gap.
- **Including citations.** Abstracts stand alone. No \cite{}, no [1], no (Smith, 2020).
- **Introducing undefined jargon.** A reader from an adjacent field should be able to follow the abstract without the paper.
- **Omitting results.** Many draft abstracts describe problem + methods but never state what was found. Results are the most important element.
- **Promising instead of delivering.** "This paper proposes..." or "We aim to..." belongs in a proposal, not a completed work's abstract.

## Examples

### Bad Example

> This paper presents a study of service discovery protocols in local area networks. We aim to analyze the performance of several protocols and discuss their trade-offs. A literature review was conducted and experiments were performed. Results are discussed. The implications of these findings for network administrators are also considered.

**Why it fails:**

- "This paper presents a study of" — buries the action in nouns, tells us nothing specific.
- "We aim to analyze" — this is a promise, not a result. The work is done; state what you found.
- "A literature review was conducted and experiments were performed" — passive, no specifics about the method.
- "Results are discussed" — teases instead of stating findings.
- "The implications... are also considered" — another tease. What are the implications?
- Violates concreteness (no specific subjects, passive throughout), reader-centered writing (no useful information), and dialogic framing (no gap or problem established).

### Good Example

> Local networks rely on service discovery protocols to find printers, file shares, and other resources, yet administrators lack empirical guidance on which protocols perform reliably at scale. We benchmarked mDNS, SSDP, and WS-Discovery across networks of 50 to 10,000 devices, measuring discovery time, packet overhead, and failure rate. mDNS resolved services in under 200ms for networks up to 2,000 devices but generated unsustainable broadcast traffic beyond that threshold. SSDP scaled to 10,000 devices with 40% less overhead than mDNS but failed silently when firewalls blocked multicast. WS-Discovery handled all scales with managed unicast but required a discovery proxy that added a single point of failure. Administrators choosing a protocol must weigh scale requirements against infrastructure complexity: mDNS suits small networks, SSDP fits mid-scale deployments with permissive firewalls, and WS-Discovery serves large networks that tolerate proxy dependency.

**Why it works:**

- Opens by establishing the gap (no empirical guidance).
- States exact methods (benchmarked three protocols, four metrics, defined scale).
- Delivers concrete results with numbers (200ms, 2,000 devices, 40% less overhead).
- Every sentence advances information — no filler, no promises.
- Closes with actionable implications tied directly to findings.
- Active verbs throughout, specific subjects, no nominalizations.