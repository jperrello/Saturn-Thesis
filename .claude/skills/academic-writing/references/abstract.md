# Abstract

An abstract is a single paragraph of 150–200 words. It contains no citations. Every term must be understandable without reading the full paper.

## Required Elements

Missing any element is a fail.

- [ ] **Problem or gap** — What question or problem does this work address?
- [ ] **Significance** — Why does the problem matter?
- [ ] **Methods** — What did you do?
- [ ] **Findings** — What did you find? State outcomes, not promises.
- [ ] **Implications** — What do the findings mean for the reader's world?

Write 1–2 sentences per element. Draft after the paper is finished — condense each section, don't write from memory.

---

## Rules

Each is pass/fail.

1. No nominalizations. At 150 words a single buried verb ("an analysis of" instead of "we analyzed") wastes space you don't have.

2. No passive voice unless the agent is genuinely unknown. "A study was conducted" fails. "We benchmarked three protocols" passes.

3. Every sentence must deliver information. A sentence that could describe any paper ("results are presented," "findings are discussed") delivers nothing. State the actual results.

4. No deliberation verbs. "This paper examines," "we investigate," "we explore," "we aim to" — these describe intent, not outcomes. State what you found, not what you set out to do. "This paper proposes" and "we aim to" belong in proposals, not completed work.

5. Open with the problem or gap in one or two sentences. The first sentence must name a gap, problem, or tension. Do not rephrase the title. Do not open with "In recent years," "It is well known that," or any other throat-clearing.

6. Close with implications in one or two sentences. The closing must connect findings to the reader's world. "These results have implications for the field" is generic filler — state the actual implications. Do not end on methods or results without a "so what."

7. Open with the strongest framing of the problem. Close with the strongest statement of implications. Bury neither in the middle.

8. Signal transitions between elements with single words ("yet," "however," "because"). Multi-clause transition sentences waste space at this length.

9. No citations. No `\cite{}`, no `[1]`, no `(Smith, 2020)`.

10. Define every technical term and acronym at first use. A reader from an adjacent field must follow the abstract without the paper.

11. "First," "novel," "unique" require evidence in the same sentence. If you cannot back a superlative within the word budget, cut it.

---

## Examples

### Bad

> This paper presents a study of service discovery protocols in local area networks. We aim to analyze the performance of several protocols and discuss their trade-offs. A literature review was conducted and experiments were performed. Results are discussed. The implications of these findings for network administrators are also considered.

- "presents a study of" — nominalization, buries action (rule 1)
- "We aim to analyze" — deliberation verb, promises instead of delivering (rule 4)
- "was conducted," "were performed" — passive, no specifics (rule 2)
- "Results are discussed" — teases instead of stating (rule 3)
- "implications... are also considered" — teases, no actual implication (rule 6)
- No gap established, no real results, no real implications. **Elements: 1/5.**

### Good

> Local networks rely on service discovery protocols to find printers, file shares, and other resources, yet administrators lack empirical guidance on which protocols perform reliably at scale. We benchmarked mDNS, SSDP, and WS-Discovery across networks of 50 to 10,000 devices, measuring discovery time, packet overhead, and failure rate. mDNS resolved services in under 200 ms for networks up to 2,000 devices but generated unsustainable broadcast traffic beyond that threshold. SSDP scaled to 10,000 devices with 40% less overhead than mDNS but failed silently when firewalls blocked multicast. WS-Discovery handled all scales with managed unicast but required a discovery proxy that added a single point of failure. Administrators choosing a protocol must weigh scale requirements against infrastructure complexity: mDNS suits small networks, SSDP fits mid-scale deployments with permissive firewalls, and WS-Discovery serves large networks that tolerate proxy dependency.

- Opens with the gap ("lack empirical guidance") — rule 5
- Names exact methods, protocols, metrics, scale — rules 1, 2
- States results with numbers, no teasing — rule 3
- Closes with actionable decision framework tied to findings — rule 6
- **Elements: 5/5.**
