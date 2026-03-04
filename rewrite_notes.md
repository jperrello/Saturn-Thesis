# RALPH Rewrite Notes

Running log of thesis revision cycles. Run 0 distills writing principles from an earlier detection-based approach (Runs 1–8, now archived). Current runs use rubric-based structural review (see `academic-advisor-prompt.md` and `RALPH_PROMPT.md`).

## Section Status

| Section | Status | Last Pass | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---|---|---|---|---|---|---|---|---|---|
| Introduction | CLEAN | Cross-cutting 4 | 5 | 5 | 4 | 4 | 4 | 3 | 25 |
| Background | CLEAN | Structural Pass 5 | 4 | 3 | 4 | 3 | 3 | 3 | 20 |
| Design | CLEAN | Cross-cutting 3 | 5 | 4 | 5 | 5 | 5 | 4 | 28 |
| Implementation | CLEAN | Structural Pass 3 | 4 | 4 | 4 | 3 | 3 | 3 | 21 |
| Scenarios | CLEAN | Pass 1 (redistributed) | — | — | — | — | — | — | eliminated |
| Evaluation | CLEAN | Cross-cutting 3 | 4 | 5 | 4 | 4 | 5 | 3 | 25 |
| Discussion | CLEAN | Cross-cutting 3 | 4 | 4 | 3 | 4 | 5 | 2 | 22 |
| Conclusion | CLEAN | Cross-cutting 3 | 4 | 4 | 4 | 4 | 4 | 4 | 24 |

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

## Implementation — Structural Pass 1

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 4 |
| C2: Contribution vs. claim | 3 |
| C3: Ordering | 3 |
| C4: Design intent | 3 |
| C5: Trade-off honesty | 3 |
| C6: Value density | 3 |
| **Total** | **19** |

**Issues from grader:** 8 (3 high, 5 medium)

**What I changed:**
- Issue 1 (HIGH, C2): Removed evaluative claims from chapter opening. "Together they constitute the existence proof for Claim 1" → descriptive roadmap sentence. Also removed evaluative \argref assertions from post-table paragraph.
- Issue 2 (HIGH, C4): Added design intent framing to all seven integration pattern subsections. Each now opens by stating what the pattern targets, what it optimizes for, and what it costs.
- Issue 3 (HIGH, C3): Moved the five-pattern taxonomy from the end of the chapter (Section "Integration Pattern Summary") to the beginning of the Client Integration Patterns section. Reader now has the organizing framework before encountering individual components. Removed redundant summary section.
- Issue 4 (MEDIUM, C6): Condensed OpenCode bug list from full enumeration to one-sentence summary of the key finding (host assumptions about static providers).
- Issue 5 (MEDIUM, C5): Trade-off statements now integrated into the taxonomy and into each subsection's design intent framing.
- Issue 6 (MEDIUM, C4): Added explicit design intent to Open WebUI plugin subsection (targets plugin architectures, no compile-time dependency, only apps with extension systems qualify).
- Issue 7 (MEDIUM, C6): Trimmed cross-compilation toolchain details (removed Rust Tier 3, nightly toolchain, -Zbuild-std specifics). Kept binary size constraints and dependency choices.
- Issue 8 (MEDIUM, C2): Removed "Significance" subsubsections from both Router and VLC. These were evaluative interpretations embedded in the Implementation chapter. Reframed Router opening as design constraint rather than thesis claim. Reframed VLC as test case description rather than evaluative assertion.

**Status:** NEEDS ANOTHER PASS

## Implementation — Structural Pass 2

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 4 |
| C2: Contribution vs. claim | 3 |
| C3: Ordering | 4 |
| C4: Design intent | 3 |
| C5: Trade-off honesty | 3 |
| C6: Value density | 3 |
| **Total** | **20** |

**Issues from grader:** 8 (2 high, 6 medium)

**What I changed:**
- Issue 2 (HIGH, C2): Removed evaluative interoperability claims from three locations. Line 29: "each resolve independently with no shared bridging layer" → descriptive inventory of five libraries. Line 73: removed "yet all three interoperate seamlessly" and argref A2. Closing paragraph: "Any language that can multicast an mDNS query can participate" → "The integration pattern varies; the wire format does not." (criterion: C2)
- Issue 1 (HIGH, C4): Strengthened design intent framing in AI SDK and MCP subsection openings. AI SDK now states "targets applications that already use a platform provider interface and optimizes for real-time network awareness" with explicit ecosystem limitation. MCP now states "targets AI coding assistants that support MCP and optimizes for breadth" with protocol dependency cost. (criterion: C4)
- Issue 7 (MEDIUM, C4): Reframed Server Types opening from "demonstrate the protocol" to "exist because backend providers differ in authentication" — three types map to no-auth, ephemeral scoped keys, and canned responses. (criterion: C4)
- Issue 4 (MEDIUM, C6): Trimmed Discovery Layer client-side paragraph. Removed re-specification of PTR/SRV/TXT resolution sequence (already in Design Section 3.5.4). Kept implementation-specific details: zeroconf's async browser, one-second settle-time value. (criterion: C6)
- Issue 3 (MEDIUM, C5): Added operational cost statements for AI SDK. Polling: 5s new-service lag, 20s stale-service lag. 401 retry: 2s blocking wait per concurrent request during key rotation. (criterion: C5)
- Issue 5 (MEDIUM, C5): Expanded router limitations from 3 sentences to full paragraph. Added: ~700KB binary size, RAM-only execution with firmware-upgrade/download dependency, concurrent memory competition with dnsmasq/hostapd/firewall, per-location independent configuration with no sync mechanism. (criterion: C5)
- Issue 6 (MEDIUM, C3): Added forward reference in table introduction: "the Pattern column references the five integration strategies defined in Section 4.3." Reader encounters pattern terms in Table 4.1 with context for where they are defined. (criterion: C3)
- Issue 8 (MEDIUM, C6): Reframed OpenCode bug paragraph. Named the root cause (static-provider assumption) and three specific failure modes (deduplication, model caching, Bun fetch timeout). Removed vague "ranging from...to..." framing. (criterion: C6)

**Status:** CLEAN

## Introduction — Structural Pass 1

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 4 |
| C2: Contribution vs. claim | 4 |
| C3: Ordering | 4 |
| C4: Design intent | 4 |
| C5: Trade-off honesty | 4 |
| C6: Value density | 3 |
| **Total** | **23** |

**Issues from grader:** 3 Introduction-specific (2 high, 1 medium) + cross-cutting terminology issues (deferred — require data changes)

**What I changed:**
- Bare \argref scaffolding: Removed `\argref{V1} \argref{V2} \argref{V3}` line that rendered as three bold labels with no context at the opening of the Thesis Statement section. (criterion: C6)
- List-format contributions: Rewrote Contributions section from three standalone paragraphs (functioning as bullet list) into four connected sentences where each contribution builds on the previous. Protocol spec → validated by census → census establishes interoperability → walkthrough measures cost. Addresses introduction reference Rule 9: "Do not list contributions as bullet points." (criterion: C6)
- Citation parade: Condensed equity paragraph from four consecutive Author-verb-finding sentences (Bassignana, Gabriel, Capraro, Costa) to two sentences with varied citation integration. Three trailing cites merged into one em-dash chain; Costa retained standalone for its strong "named the result" framing. (criterion: C6)

**Not addressed (out of scope — data/technical content changes):**
- "Seven implementations" vs. "nine components" terminology inconsistency (cross-cutting, requires reconciling Implementation table with Introduction/Evaluation counts)
- "Five mDNS libraries" vs. "four" in Evaluation Table 5.4 (cross-cutting, requires verifying correct count against codebase)
- \argref{} labels never explained to reader (cross-cutting, affects all chapters — needs appendix or removal decision)

**Status:** CLEAN

## Scenarios — Structural Pass 1 (Redistribution)

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 3 |
| C2: Contribution vs. claim | 3 |
| C3: Ordering | 3 |
| C4: Design intent | 3 |
| C5: Trade-off honesty | 3 |
| C6: Value density | 2 |
| **Total** | **17** |

**Issues from grader:** 6 (2 high, 4 medium)

**What I changed:**
- Issue 1 (HIGH, C1): Eliminated Chapter 5 as a standalone chapter. Redistributed its three sections: design fictions → Ch3 (Design, new section "Design Origins" after Audiences), VLC security surface → Ch4 (Implementation, appended to subprocess bridge section), integration opportunity analysis → Ch6 (Evaluation, new subsection after R3 interoperability). Thesis reduced from 8 chapters to 7. Updated ch1 organization preview and all hardcoded chapter references to use \ref{} labels.
- Issue 2 (HIGH, C6): Removed VLC technical architecture duplication. Ch5's Section 5.2 repeated the two-layer architecture, dns-sd CLI, and PyInstaller packaging already in Ch4 Section 4.4. Only unique content carried forward: security surface paragraph (to Ch4) and Kim-Reeves evaluative framing (to Ch6's integration opportunity section).
- Issue 3 (MEDIUM, C2): Removed novelty claim "No prior work has been found supporting this use of design fictions as LLM specification input" from main thesis body. Claim remains in Appendix B (AI methodology) where it belongs.
- Issue 4 (MEDIUM, C3): Chapter placement issue resolved by eliminating the standalone chapter entirely.
- Issue 5 (MEDIUM, C4): Added design-intent framing to integration opportunity analysis. New opening states what the analysis measures (protocol compatibility), what it does not measure (adoption likelihood, development effort), and why the distinction matters.
- Issue 6 (MEDIUM, C5): Added paragraph to ch3 Design Origins stating what the fictions did not surface: AP isolation appeared only during campus testing, TXT schema drift emerged during heuristic evaluation. Three personas covered provisioning lifecycle but missed network infrastructure constraints.

**Status:** CLEAN

## Background — Structural Pass 1

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 4 |
| C2: Contribution vs. claim | 4 |
| C3: Ordering | 3 |
| C4: Design intent | 4 |
| C5: Trade-off honesty | 4 |
| C6: Value density | 3 |
| **Total** | **22** |

**Issues from grader:** 7 (2 high, 5 medium)

**What I changed:**
- Issue 1 (HIGH, C3): Reordered all sections. AI Service Landscape moved from Section 3 to Section 1. Reader now encounters the problem domain (AIaaS model, configuration fragmentation, API key fragility) before any protocol discussion. New ordering follows reference file Rule 6: fundamentals → chosen approach → alternatives → gap. (criterion: C3)
- Issue 2 (HIGH, C6): Condensed three application subsections (Hosted Chat Applications, Coding Assistants, Voice Typing and Transcription) into one "Configuration Fragmentation" subsection. Replaced application inventory with structural argument: the API standard specifies how to talk to a provider but not how to find one, so configuration scales linearly with application count. Voice pipelines retained as one concrete example. (criterion: C6)
- Issue 3 (MEDIUM, C6): Eliminated verbatim Open WebUI/LibreChat/Jan example that duplicated Introduction ch1 line 16. Background now explains why fragmentation exists rather than repeating the motivational example. (criterion: C6, cross-cutting redundancy)
- Issue 4 (MEDIUM, C6): Merged Privacy Considerations (former Section 2.6) into Security Context as "mDNS Privacy and Vulnerability Surface" subsection. Eliminated duplicate Kaiser/Waldvogel and Könings et al. citations within the same chapter. (criterion: C6)
- Issue 5 (MEDIUM, C6): Condensed four protocol alternative subsections (NetBIOS, UPnP, DLNA, WS-Discovery) into one paragraph with 1-2 sentences each, per reference file Rule 5. (criterion: C6)
- Issue 6 (MEDIUM, C6): Tightened DHCP analogy from standalone section to subsection within mDNS section. Removed router deployment paragraph that pre-argued Design chapter content. (criterion: C6, cross-cutting redundancy with Design)
- Issue 7 (MEDIUM, C6): Moved Static API Key Fragility from Security Context to Section 1 as part of the fundamental problem. Removed Saturn solution details (Kerberos parallel, ephemeral key mechanism); replaced with forward references to Design and Discussion chapters. (criterion: C6)

**Status:** CLEAN

## Evaluation — Structural Pass 1

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 4 |
| C2: Contribution vs. claim | 5 |
| C3: Ordering | 4 |
| C4: Design intent | 4 |
| C5: Trade-off honesty | 5 |
| C6: Value density | 3 |
| **Total** | **25** |

**Issues from grader:** 5 (1 high, 4 medium) — Evaluation-specific issues identified from grader's priority ranking and cross-cutting analysis. No deep-dive was produced for this section (grader deep-dived Implementation instead), so issues derived from scores, priority note, and cross-cutting findings.

**What I changed:**
- Integration opportunity catalog (HIGH, C6): Replaced 42-application enumeration paragraph (listing every app by name across seven categories) and three-pattern decomposition (with per-pattern example sentences) with two concise paragraphs. Table retains category/count/path data; prose now gives structural observation about viability tiers and a one-sentence summary of pattern distribution (17/12/13). Removed ~180 words of catalog-style listing.
- Meli et al. de-duplication (MEDIUM, C6): The "100,000 repositories, 81% never revoked" statistic appeared three times in the chapter (Analysis, STRIDE, Exposure Window). Kept the first full-statistics occurrence in Analysis. STRIDE paragraph now reads "static keys persist until manually revoked" with bare cite. Exposure Window now reads "Because static keys rarely get revoked" with bare cite. Eliminated two redundant restatements.
- Guttman quotation (MEDIUM, C6): Replaced fourth repetition of the "direct communications between two or more computing devices via IP" quotation with a brief formulation ("Saturn satisfies Guttman's zero-configuration criterion") that cites without re-quoting.
- R2 discovery sequence (MEDIUM, C6): Replaced the four-step enumerated list (Browse PTR, Locate SRV, Describe TXT, Resolve A/AAAA) — which duplicated the canonical version in Design Section 3.5.4 — with a one-sentence forward reference to Section~\ref{sec:discovery-process}. Table and subsequent analysis unchanged.
- R3 integration re-description (MEDIUM, C6): Compressed per-component integration description (five sentences naming each component's approach) into two sentences with a Chapter~\ref{ch:implementation} forward reference. Retained the interoperability-relevant fact: all seven consumers resolve the same records through independent stacks.

**Status:** CLEAN

## Discussion — Structural Pass 1

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 4 |
| C2: Contribution vs. claim | 4 |
| C3: Ordering | 4 |
| C4: Design intent | 4 |
| C5: Trade-off honesty | 5 |
| C6: Value density | 3 |
| **Total** | **24** |

**Issues from grader:** 7 (2 high, 5 medium) — Discussion-specific issues derived from grader priority ranking, cross-cutting redundancy analysis, and score matrix. Deep-dive was on Implementation (already CLEAN); Discussion issues inferred from C6=3 diagnosis: "Relation to prior work partially restates Background material; some paragraphs repeat evaluation findings rather than interpreting them."

**What I changed:**
- Service Discovery citation parade (HIGH, C6): Replaced four consecutive Author-verb-finding sentences (Guttman defined, Siddiqui documented, Siljanovski demonstrated, Kim measured) with one sentence citing Siljanovski and Kim, then immediate interpretation: "the constraint on zero-configuration AI provisioning was never the transport layer." Background restatement eliminated.
- AI Provisioning problem restatement (HIGH, C6): Removed three-sentence re-narration of Syed/Costa/Gabriel problem (already in Background and Introduction). Replaced with one-sentence problem reference, then interpretation: Saturn shifts provisioning from per-user linear cost to per-network constant cost. Cognitive walkthrough number retained as evidence for the structural insight.
- Meli et al. redundancy (MEDIUM, C6): Replaced full restatement of "100,000 repositories, 81% never revoked" (5th or 6th occurrence) with cross-reference to Chapter 2 and one-sentence summary of the temporal failure mode. Statistic no longer repeated.
- AP Isolation evaluation restatement (MEDIUM, C6): Merged two paragraphs (problem description + test result) into one. "We confirmed this in January 2026" reporting eliminated; eduroam/UCSC-guest result now a subordinate clause within the problem description.
- Network Security BeyondCorp redundancy (MEDIUM, C6): Removed "Ward and Beyer established zero-trust as the enterprise standard" (restating Section 6.2). Replaced with interpretation of what modular security posture means for edge networks. Added forward references to existing BeyondCorp and Future Work sections.
- Meta-commentary opening (MEDIUM, C6): Removed "Saturn sits at the intersection of three research areas and contributes something distinct to each." Subsection headings already communicate the structure.
- Syed/Qazi restatement (MEDIUM, C6): Condensed four-sentence Author-verb-finding paragraph about AI key management to three sentences with integrated citations. Eliminated re-narration of Background content.

**Status:** CLEAN

## Design — Structural Pass 1

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 5 |
| C2: Contribution vs. claim | 4 |
| C3: Ordering | 4 |
| C4: Design intent | 5 |
| C5: Trade-off honesty | 5 |
| C6: Value density | 4 |
| **Total** | **27** |

**Issues from grader:** 4 (0 high, 4 medium) — Design scored highest overall. No deep-dive produced (grader deep-dived Background). Issues derived from score matrix, priority ranking note, cross-cutting analysis, and grader notes.

**What I changed:**
- Design Origins process narration (MEDIUM, C3/C6): Compressed section from 26 lines to 12. Eliminated "From Personas to Requirements" subsection (redundant with Goals and Audiences sections). Derek and Mira condensed to one paragraph establishing the asymmetric complexity trade-off. Jordan's ephemeral key connection retained as the strongest design-driving link. Removed Mira's standalone "crystallized the design question" paragraph; trust question now a subordinate clause.
- Meli et al. redundancy (MEDIUM, C6): Replaced full restatement of "81% never revoked" statistic (appears in 5 chapters) with condensed formulation: "the dominant failure mode Meli et al. documented: leaked credentials that persist indefinitely." Cross-cutting redundancy reduced.
- AP isolation test evidence in Design (MEDIUM, C3): Replaced "Eduroam and UCSC-Guest both block mDNS, confirmed in January 2026 testing" with forward reference to Section~\ref{sec:eval-ap-isolation}. The design constraint (AP isolation blocks multicast) remains; the evaluation evidence moves to where it belongs.
- Evaluative "prove the point" language (MEDIUM, C2): Replaced "Seven implementations across four languages prove the point" followed by five-library inventory with design-level statement: "Any language with an mDNS stack can implement a conforming client or server." Evidence deferred to Chapter~\ref{ch:implementation} via forward reference.

**Status:** CLEAN

## Conclusion — Structural Pass 1

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 4 |
| C2: Contribution vs. claim | 5 |
| C3: Ordering | 5 |
| C4: Design intent | 4 |
| C5: Trade-off honesty | 5 |
| C6: Value density | 4 |
| **Total** | **27** |

**Issues from grader:** 2 (0 high, 2 medium) — Conclusion scored 27/30. No deep-dive produced (grader deep-dived Implementation). Issues derived from priority ranking note and grader notes.

**What I changed:**
- Meta-commentary removal (MEDIUM, C6): Removed "Three claims structured this thesis, and the evidence supports each within its stated scope." This sentence narrated the paper's structure; the three claim paragraphs that follow are self-evident without it. (criterion: C6)
- "What comes next?" too thin (MEDIUM, C1): Rewrote the end of the limitation paragraph to frame an explicit open research question. Original ended with factual statement about what institutional adoption "requires." Replaced with: "the open question is how much coordination overhead can return before the zero-configuration property ceases to hold." Names one direction (crossing the subnet boundary via wide-area DNS-SD/relay) and frames the tension (centralized authority vs. zero-configuration property). Satisfies reference file Rule 14 (name the most important open question) and Rule 6 (selective future work). (criterion: C1)

**Status:** CLEAN

## Cross-Cutting Issues — Structural Pass 1

**Grader scores (this cycle):**

| Section | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---|---|---|---|---|---|---|---|
| Introduction | 5 | 5 | 4 | 4 | 4 | 3 | 25 |
| Background | 4 | 4 | 4 | 3 | 4 | 3 | 22 |
| Design | 5 | 4 | 5 | 5 | 5 | 4 | 28 |
| Implementation | 4 | 3 | 4 | 3 | 3 | 3 | 20 |
| Evaluation | 5 | 5 | 4 | 4 | 5 | 4 | 27 |
| Discussion | 5 | 4 | 4 | 4 | 5 | 3 | 25 |
| Conclusion | 5 | 5 | 5 | 4 | 5 | 3 | 27 |

**All sections marked CLEAN from previous passes. Targeted cross-cutting issues per RALPH Phase 2 decision rules.**

**Issues from grader:** 5 cross-cutting categories (concept re-introduction, citation role duplication, terminology inconsistency)

**What I changed:**

- Meli et al. citation recycling (HIGH, C6/C14): Canonical home is ch2 Section 2.1.1 (new label `sec:key-fragility`). Removed redundant `\cite{meli2019secrets}` from ch3-design (2 instances), ch6-evaluation (2 instances), ch7-discussion (1 instance). Each now cross-references Background via `Section~\ref{sec:key-fragility}` instead of re-citing the same finding. ch1-introduction cite retained (different role: first reader contact with the problem). ch6-evaluation:275 cite retained (different role: warrant for Saturn's design consequence). (criterion: C6, academic-writing Rule 13/14)

- Kaiser/Waldvogel citation duplication (MEDIUM, C6/C14): Canonical home is ch2 Section 2.4.2 (new label `sec:mdns-privacy`). Replaced `\cite{kaiser2014privacy}` with cross-references in ch7-discussion (2 instances: campus lab rogue service paragraph, relation-to-prior-work network security paragraph) and ch8-conclusion (1 instance). ch3-design:19 cite retained (different role: warrant for bounded credential design, uses direct quote). ch7-discussion:44 and ch7-discussion:105 cites retained (reference to Kaiser's proposed *solution*, different content from the privacy *findings*). (criterion: C6, academic-writing Rule 13/14)

- Printer/Bonjour analogy repetition (MEDIUM, C6/C13): Canonical home is ch1 Section 1.2. Replaced full re-derivation in ch3-design opener ("Add a printer... Add an AI service...") with a cross-reference that builds on Introduction's framing: "Chapter 1 framed the gap: printers announce themselves over mDNS, but AI services do not." (criterion: C6, academic-writing Rule 13)

- mDNS discovery sequence re-introduction (MEDIUM, C6/C13): Canonical home is ch3 Section 3.5.5 (Discovery Process). In ch4-implementation:125, replaced protocol re-explanation ("sends periodic PTR queries... follows up with SRV and TXT... resolves via A records") with cross-reference to `Section~\ref{sec:discovery-process}`. Implementation-specific timing values (5s polling, 20s staleness, goodbye packets) retained. In ch6-evaluation:41, removed redundant enumeration ("browse PTR, locate SRV, describe TXT, resolve A/AAAA") after existing cross-reference to `Section~\ref{sec:discovery-process}`. (criterion: C6, academic-writing Rule 13)

- Syed et al. citation duplication (MEDIUM, C6/C14): Canonical home is ch2 Section 2.1 (new label `sec:ai-landscape`). Replaced `\cite{syed2025aiaas}` with cross-references in ch6-evaluation:81 (1 instance), ch7-discussion:49 (1 instance), ch7-discussion:88 (1 instance). ch1-introduction:12 cite retained (first reader contact). (criterion: C6, academic-writing Rule 14)

- Terminology inconsistency: "five" vs "four" mDNS libraries (MEDIUM, factual): graph.json claim-1 and feasibility-evidence nodes said "five independent mDNS libraries." Thesis body consistently says "four" (zeroconf, mdns-sd, multicast-dns, dns-sd CLI). OWUI uses the same `zeroconf` package as the core library, so it is not an independent library. Updated graph.json (2 nodes), claims/claim-1.md, claims/evidence-matrix.md, claims/argument-registry.md, and claims/feasibility/evidence.md to say "four." Also corrected "three languages" to "four languages" (Python, Rust, TypeScript, Lua) in graph.json claim-1. Ran visualizations/sync.py.

**Status:** CLEAN

## Conclusion — Structural Pass 2

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 4 |
| C2: Contribution vs. claim | 4 |
| C3: Ordering | 4 |
| C4: Design intent | 3 |
| C5: Trade-off honesty | 4 |
| C6: Value density | 2 |
| **Total** | **21** |

**Issues from grader:** 7 (3 high, 4 medium)

**What I changed:**
- Issue 1 (HIGH, C6): Rewrote opening paragraph. Removed problem re-derivation ("AI tools gate access behind API keys, per-user subscriptions, and manual endpoint configuration") and mechanism re-explanation ("registers AI endpoints under `_saturn._tcp.local.`, and every device on the segment discovers them through mDNS/DNS-SD"). Opening now states the finding directly: "Saturn demonstrates that AI services can be provisioned like printers, DHCP addresses, and file shares." Connects to Introduction's framing without re-deriving it. (criterion: C6)
- Issue 2 (HIGH, C6): Rewrote V1 paragraph. Removed evidence catalog ("Seven implementations across four languages and four independent mDNS libraries interoperate... A Rust binary runs on a $30 GL.iNet travel router alongside DHCP and DNS"). Replaced with synthesis: "Independent implementations interoperate on a shared service type because the protocol specification, not any reference implementation, defines conformance." Numbers have canonical home in Evaluation. (criterion: C6)
- Issue 3 (HIGH, C6): Rewrote V2 paragraph. Removed all walkthrough statistics (53%, 79%, 902-vs-54, "2 to 14 additional steps"). Replaced with structural insight: "Per-user provisioning scales linearly... Saturn makes provisioning a per-network constant." The numbers live in Evaluation Section 5.3.2. (criterion: C6)
- Issue 4 (MEDIUM, C6): Rewrote V3 sentence. Removed STRIDE specifics ("eliminates three high-severity threats at the cost of three medium-severity local-network threats"). Replaced with trade-off pattern: "trades broadcast exposure for temporal containment." (criterion: C6)
- Issue 5 (MEDIUM, C4): Reframed AP isolation as consequence of design intent. Added: "This is the cost of the design's central choice: zero-configuration requires multicast, and multicast requires cooperative infrastructure." Limitation is now a design trade-off, not an accident. (criterion: C4)
- Issue 6 (MEDIUM, C1): Promoted future direction from subordinate clause to standalone paragraph. Wide-area DNS-SD named explicitly. Open question framed: "how much coordination overhead can return before the zero-configuration property ceases to hold." (criterion: C1)
- Issue 7 (MEDIUM, C5): Rewrote final paragraph. Removed "The barrier to treating AI like printing is not technical" which dismissed documented technical barriers. Replaced with: "The remaining barriers are both technical---AP isolation, schema drift, single-segment scope---and organizational." Final statement: "Saturn establishes that the technical path is open." (criterion: C5)

**Status:** CLEAN

## Background — Structural Pass 2

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 4 |
| C2: Contribution vs. claim | 3 |
| C3: Ordering | 4 |
| C4: Design intent | 3 |
| C5: Trade-off honesty | 3 |
| C6: Value density | 3 |
| **Total** | **20** |

**Issues from grader:** 7 (2 high, 5 medium)

**What I changed:**
- Issue 1 (HIGH, C2): Removed evaluative "works/breaks" framing from AI Landscape section. "This architecture works for individual developers building products. It breaks when the goal is shared access." → "For individual developers building products, the model is straightforward: one developer, one key, one billing account. Shared access multiplies every element." Descriptive rather than evaluative; the judgment that this is a problem is inherited from the Introduction. (criterion: C2)
- Issue 2 (HIGH, C4): Reframed four-property mDNS/DNS-SD list from advocacy ("Four properties make mDNS/DNS-SD the right fit for Saturn") to descriptive ("mDNS/DNS-SD has four defining properties"). Removed "matching Saturn's threat model" from link-local scope description. Replaced "discover Saturn services without installing anything" with trade-off acknowledgment sentence referencing Section 2.5. Properties now read as protocol characteristics, not as a pitch for Saturn's design choice. (criterion: C4)
- Issue 3 (MEDIUM, C6): Removed "Every major desktop and mobile operating system already speaks mDNS" from Platform Adoption subsection. Redundant with line 56 ("Both run on every major operating system"). The three platform-specific examples (Bonjour, Avahi, Windows 10) already demonstrate adoption without a summary statement. (criterion: C6)
- Issue 4 (MEDIUM, C5): Added trade-off forward reference at end of mDNS/DNS-SD introductory paragraph: "These properties carry constraints: link-local scope confines discovery to a single network segment, multicast traffic is visible to passive observers, and enterprise access-point isolation can block multicast entirely (Section 2.5)." Reader now encounters limitations before evaluating mDNS against alternatives. (criterion: C5)
- Issue 5 (MEDIUM, C3): Promoted DHCP Parallel from subsection 2.2.5 (nested within mDNS/DNS-SD technical description) to standalone section between Alternative Discovery Protocols and Security Context. Reader now encounters: mDNS mechanics → alternatives dismissed → DHCP conceptual frame → security → gap. The analogy no longer interrupts the technical thread. (criterion: C3)
- Issue 6 (MEDIUM, C6): Replaced gap section's restatement of AI landscape problem and re-citation of Meli 2019 with cross-references to Sections 2.1 and 2.1.2. Gap now synthesizes ("require per-application endpoint configuration") rather than re-describes. (criterion: C6)
- Issue 7 (MEDIUM, C1): Expanded NetBIOS and DLNA descriptions. NetBIOS now explains its mechanism ("resolves host names through broadcast queries on a flat namespace") before the dismissal. DLNA now explains its scope ("defined interoperability profiles for streaming media between consumer devices using UPnP discovery") before the dismissal. (criterion: C1)

**Status:** CLEAN

## Implementation — Structural Pass 3

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 3 |
| C2: Contribution vs. claim | 4 |
| C3: Ordering | 4 |
| C4: Design intent | 3 |
| C5: Trade-off honesty | 4 |
| C6: Value density | 2 |
| **Total** | **20** |

**Issues from grader:** 8 (4 high, 4 medium)

**What I changed:**
- Issue 5 + Issue 2 (HIGH, C1/C6): Replaced mDNS library census paragraph (line 29) with reused-vs-built distinction paragraph. Lists reused infrastructure (mDNS libraries, FastAPI, Vercel AI SDK, PyInstaller) then names original contribution (beacon logic, discovery client, integration code). Addresses reference file Rule 3: "State what you reused before stating what you built." Simultaneously eliminates the evaluative "four mDNS libraries" synthesis that duplicated Evaluation's interoperability finding. (criterion: C1, C6)
- Issue 1 (HIGH, C6): Replaced OpenRouter server description. Removed full ephemeral key lifecycle re-derivation (authenticate, mint, broadcast, rotate, delete, "permanent credential never touches the wire") which duplicated Design Section 3.4.4. Replaced with cross-reference to Section~\ref{sec:ephemeral-keys} and implementation-specific detail: OpenRouter's provisioning API supports the two required operations (scoped sub-key creation, programmatic deletion). (criterion: C6)
- Issue 3 (HIGH, C4): Reframed Open WebUI plugin paragraph. Old text was pure inventory (what the plugin does, what library it uses). New text states the test: "whether a single file---no build step, no dependency declaration---can give an application full Saturn discovery." Removed redundant upload instruction that duplicated new framing. (criterion: C4)
- Issue 4 (MEDIUM, C4): Reframed Jan proxy paragraph. Old text was how-to guide ("Jan is an open-source privacy-focused desktop chat application"). New text states the test case framing: "Jan tests the proxy pattern against the most constrained case." Names the constraints (no plugin system, no tool protocol support, no source code access) and states cost/benefit explicitly. Fixed resulting "zero modification" duplication between paragraphs. (criterion: C4)
- Issue 7 (MEDIUM, C3): Expanded integration pattern taxonomy from five to six. Added "Localhost proxy" as item 5 between Subprocess bridge and Environment variable injection. Updated count from "five" to "six" in both the section opening and the table reference. Taxonomy now matches the subsection structure (6 patterns + 1 fork). (criterion: C3)
- Issue 8 (MEDIUM, C5): Added trade-off statement to discovery layer. After the settle-time description, added: "The settle-time is a trade-off: too short and slow-responding services are missed; too long and every discovery call pays the delay. On a network with no Saturn services, the caller blocks for the full timeout before receiving an empty result." (criterion: C5)

**Not addressed:**
- Issue 6 (MEDIUM, C6): VLC architecture duplication with Evaluation. Checked Evaluation chapter; no VLC content found. Grader may have been referencing pre-redistribution state. No action needed.

**Status:** NEEDS ANOTHER PASS

## Implementation — Structural Pass 4

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 4 |
| C2: Contribution vs. claim | 3 |
| C3: Ordering | 3 |
| C4: Design intent | 3 |
| C5: Trade-off honesty | 3 |
| C6: Value density | 3 |
| **Total** | **19** |

**Issues from grader:** 8 (2 high, 6 medium)

**What I changed:**
- Issue 1 (HIGH, C4): Rewrote taxonomy opening. Old text identified three dimensions (extensibility, language, dependencies) but arranged patterns on a single axis without explaining why. New text states the design constraint that generated the taxonomy: Saturn targets applications not built for mDNS, so integration is dictated by each application's extensibility surface. Six surveyed surfaces produced six patterns. Depth-to-breadth axis now explicitly characterized as a trade-off (better runtime behavior vs. stricter target requirements). (criterion: C4)
- Issue 2 (HIGH, C2): Removed evaluative claims from three subsections. Native SDK (line 125): "No API key. No endpoint URL. No environment variable." → "The code sample omits API keys, endpoint URLs, and environment variables because the provider resolves all three from mDNS at runtime." Open WebUI (line 140): "shows up on the next cache refresh without administrator intervention" → "services that appear between refreshes become available on the next cycle." VLC (line 170): "No environment variables, no Python on the PATH, no API key" → removed; PyInstaller sentence reframed as mechanism description. (criterion: C2)
- Issue 3 (MEDIUM, C3): Renamed "Server-Side Components" section to "Embedded Deployment." Core package is also server-side; old heading implied a category the core package should also belong to. New heading names what distinguishes this section: constrained embedded hardware. (criterion: C3)
- Issue 4 (MEDIUM, C5): Added concrete trade-offs to MCP subsection. Per-call latency from sync-to-async bridge (one-second settle-time blocks a thread pool slot). Subprocess overhead (one stdio process per assistant session). Trust surface (six tools expose full service inventory to any MCP-connected model). (criterion: C5)
- Issue 5 (MEDIUM, C6): Condensed pre-summary paragraph from six sentences to one. Old text re-listed dependencies already shown in Table 4.1. New text: single sentence distinguishing reused infrastructure from original contribution, deferring details to each subsection. (criterion: C6)
- Issue 6 (MEDIUM, C4): Reframed Jan proxy opening. Old text stated "most constrained case" without explaining why that constraint matters. New text states the boundary case explicitly: if Saturn works with an application whose only extensibility is a URL field, the proxy pattern is a universal fallback for any OpenAI-compatible client. (criterion: C4)
- Issue 7 (MEDIUM, C5): Made Native SDK ecosystem lock-in concrete. Old text: "limited to applications within that SDK's ecosystem." New text: "this implementation requires TypeScript applications built on Vercel's AI SDK. Of the seven client applications in Table 4.1, only two qualify." (criterion: C5)
- Issue 8 (MEDIUM, C6): Replaced closing paragraph. Old text restated the thesis principle ("the constant is the protocol... the wire format does not") already established in Design Section 3.6.4. New text: forward-looking sentence connecting Implementation to Evaluation ("Chapter 5 evaluates whether these nine components... interoperate on the shared wire format defined in Chapter 3"). (criterion: C6)

**Status:** CLEAN

## Cross-Cutting Issues — Structural Pass 2

**Grader scores (this cycle):**

| Section | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---|---|---|---|---|---|---|---|
| Introduction | 4 | 4 | 5 | 4 | 4 | 4 | 25 |
| Background | 4 | 4 | 4 | 3 | 3 | 3 | 21 |
| Design | 5 | 4 | 5 | 5 | 5 | 4 | 28 |
| Implementation | 4 | 4 | 4 | 3 | 3 | 3 | 21 |
| Evaluation | 4 | 5 | 4 | 4 | 5 | 3 | 25 |
| Discussion | 4 | 4 | 4 | 4 | 5 | 3 | 24 |
| Conclusion | 4 | 5 | 5 | 4 | 4 | 4 | 26 |

**All sections marked CLEAN from previous passes. Targeted cross-cutting issues per RALPH Phase 2 decision rules.**

**Issues from grader:** 7 cross-cutting categories (concept re-introduction, citation role duplication, terminology inconsistency, chapter inheritance violations)

**What I changed:**

- BeyondCorp re-introduction in Discussion (HIGH, C6/C13): ch7 Section 6.2 re-explained BeyondCorp from scratch ("Ward and Beyer's BeyondCorp model treats every network as hostile: no request is trusted based on origin...") duplicating Background Section 2.6.1. Replaced with cross-reference: "The BeyondCorp model (Section~\ref{sec:security-context}) requires managed devices, identity providers, and per-request verification." Removed redundant `\cite{ward2014beyondcorp}` (same evidence role as Background). Retained `\cite{osborn2016beyondcorp2}` in ch7 line 44 (different role: warrant for convergence direction).

- AP isolation re-description in Discussion (HIGH, C6/C13): ch7 Section 6.4 re-described test results ("Testing on eduroam and UCSC-guest confirmed total failure---no discovery traffic crosses the isolation boundary") already documented in Evaluation Section 5.4.4. Replaced with cross-reference: "Section~\ref{sec:eval-ap-isolation} confirmed the consequence: on both campus networks tested, discovery failed completely." Discussion Rule 1: interpret, don't restate.

- Ephemeral key numbers in Evaluation (MEDIUM, C6/C13): ch6 Section 5.3.1 re-stated "10-minute lifetime and 5-minute rotation cycle" already established in Design Section 3.4.4. Replaced with cross-reference: "an ephemeral key with the lifecycle defined in Section~\ref{sec:ephemeral-keys}." Numbers retained in Evaluation Table 5.7 (different role: quantifying exposure window).

- "Ships on every major OS" redundancy in Background (MEDIUM, C6/C13): ch2 line 126 ("ships on every major operating system") repeated ch2 line 56 within the same chapter. Replaced with "in a preinstalled stack" — references the established fact without restating it.

- Bonjour "shipped in 2002" re-introduction in Background (MEDIUM, C6/C13): ch2 line 106 ("Apple shipped Bonjour with macOS in 2002") duplicated Introduction ch1 lines 29-30. Replaced with "On macOS, Bonjour powers AirPrint, AirPlay, and AirDrop" — keeps new information (what Bonjour powers), removes repeated fact (ship date).

- Background opening re-deriving Introduction motivation (MEDIUM, C3/C13): ch2 line 4 ("Every application that consumes AI text completion asks the same questions on first launch: where is the endpoint, what are the credentials, which model") near-verbatim repetition of ch1 lines 33-36. Replaced with "The Introduction identified the configuration burden: every AI application demands its own endpoint, credentials, and model selection." Inherits from Introduction per chapter contract instead of re-deriving.

- Forward references in Background key fragility section (MEDIUM, C3): ch2 line 49 ("Chapter~\ref{ch:design} specifies Saturn's ephemeral key mechanism; Chapter~\ref{ch:discussion} analyzes its residual risks") introduced Saturn's solution in Background, which should only establish the problem. Removed. Background Rule 6: no forward references that introduce content before its time.

**Not addressed (deferred — require data reconciliation or broader changes):**
- Terminology: "consumer" vs "client" vs "user" distinction never explicitly stated (cross-cutting, all chapters)
- Language count inconsistency: Abstract says "four languages," argument-registry says "3 languages" (cross-cutting, requires verifying Lua's status)
- Background DHCP Parallel belongs in Design per grader deep-dive (structural move, deferred to next cycle)
- Background Gap subsection buried under Security Context instead of standalone section (structural promotion, deferred)
- Alternative protocols section reads as dismissal, not trade-off analysis (content change, deferred)

**Status:** CLEAN

## Introduction — Structural Pass 2

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 4 |
| C2: Contribution vs. claim | 4 |
| C3: Ordering | 4 |
| C4: Design intent | 4 |
| C5: Trade-off honesty | 4 |
| C6: Value density | 3 |
| **Total** | **23** |

**Issues from grader:** 7 (2 high, 5 medium)

**What I changed:**
- Issue 1 (HIGH, C6): Reduced equity paragraph from three sentences with four citations (Bassignana, Gabriel, Capraro, Costa) to one sentence with one citation (Bassignana) and a cross-reference to Discussion Section~\ref{sec:implications}. Moved Capraro citation to Discussion's Broader Implications section where the other equity citations already live. Gabriel, Costa already had canonical homes in Discussion/Evaluation. (criterion: C6)
- Issue 2 (HIGH, C1): Rewrote Contributions section to focus on artifacts (protocol specification, nine implementations, cognitive walkthrough instrument). Removed evaluative language: "validate" → "exercise," "establishing that the wire format enables interoperable discovery" → removed. Evaluative claims remain in Thesis Statement where they belong. Updated "seven" to "nine implementations" in Thesis Statement to match Contributions and Implementation Table 4.1 counts. (criterion: C1)
- Issue 3 (MEDIUM, C6): Removed RFC 6762 and RFC 6763 citations from Introduction line 30 (canonical home is Background Section 2.2). Replaced with forward reference: "the protocols behind AirPrint and Chromecast (Chapter~\ref{ch:background})." Protocol names (mDNS, DNS-SD) retained for first-use definition. (criterion: C6)
- Issue 4 (MEDIUM, C3): Moved "Saturn in Brief" section before "Thesis Statement." Reader now encounters the concrete system (service type, TXT records, beacon architecture) before evaluating claims about it. New sequence: Problem → Vision → Saturn in Brief → Thesis Statement → Contributions → Organization. (criterion: C3)
- Issue 5 (MEDIUM, C4): Added design intent to router mention: "demonstrating that AI provisioning fits in the network infrastructure layer." Changed "existing network services" to "DHCP and DNS" for concreteness. Router is no longer inventory; it's evidence for infrastructure-layer positioning. (criterion: C4)
- Issue 6 (MEDIUM, C5): Added trade-off sentence after the Vision section's benefits paragraph: "The cost is scope: discovery reaches only the local network segment, and enterprise networks that isolate wireless clients can block the multicast traffic it depends on." Reader encounters a constraint within two sentences of the benefit. (criterion: C5)
- Issue 7 (MEDIUM, C6): Replaced three-sentence AI disclosure in Organization (meta-commentary about why we disclose + narrative about Claude's role) with one navigational sentence: "Appendix~B documents where Anthropic's Claude contributed to this work and where we overruled it." Organization section is now purely structural. (criterion: C6)

**Status:** CLEAN

## Cross-Cutting Issues — Structural Pass 3

**Grader scores (this cycle):**

| Section | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---|---|---|---|---|---|---|---|
| Introduction | 5 | 4 | 4 | 4 | 4 | 3 | 24 |
| Background | 4 | 4 | 4 | 3 | 3 | 3 | 21 |
| Design | 5 | 4 | 5 | 5 | 5 | 4 | 28 |
| Implementation | 4 | 3 | 4 | 3 | 3 | 3 | 20 |
| Evaluation | 4 | 5 | 4 | 4 | 5 | 3 | 25 |
| Discussion | 4 | 4 | 4 | 4 | 5 | 3 | 24 |
| Conclusion | 4 | 5 | 5 | 4 | 4 | 4 | 26 |

**Cross-cutting issues from grader:** 5 categories (terminology inconsistency, concept re-introduction x3, citation role duplication x2)

**What I changed:**
- Terminology: "five" mDNS libraries in abstract changed to "four" to match Evaluation Table 5.6 and all other references. The abstract previously contradicted every other count in the thesis. (criterion: C6, factual accuracy)
- Terminology: Introduction now distinguishes nine components from seven independent mDNS consumers. Added clarifying sentence: "Seven of those components resolve \_saturn.\_tcp.local. through four independent mDNS libraries with no shared discovery code; two reuse the core package's mDNS stack to test additional integration patterns." Resolves the nine-vs-seven confusion the grader flagged as the most visible terminology issue. (criterion: C6)
- Concept re-introduction: Implementation Section 4.2 opening re-derived the "application layer vs. infrastructure layer" design rationale from scratch. Replaced three-sentence re-argument with one-sentence cross-reference to Design Section 3.1 Goals. (criterion: C6, chapter contract)
- Concept re-introduction: Implementation Section 4.2.1 Hardware re-argued the beacon's lightweight nature ("registers mDNS records and rotates API keys---work measured in kilobytes and milliseconds") already established in Design Section 3.4.2. Replaced with hardware specs and cross-reference to Section 3.4.2 Beacons. (criterion: C6, chapter contract)
- Concept re-introduction: Evaluation R2 (line 39) re-stated the Siddiqui zero-config definition already established in Background Section 2.2. Replaced inline re-statement with cross-reference: "the zero-configuration standard defined in Section 2.2." (criterion: C6)
- Concept re-introduction: Evaluation R2 (line 62) repeated the "No account creation, no key management portal" refrain from Introduction line 39. Replaced with structural language: "the credential arrives through the same multicast channel as the endpoint address, eliminating the out-of-band provisioning that Section 2.1 documented." (criterion: C6)

**Not changed (deferred):**
- Citation role duplication (Meli et al. in Introduction): The Introduction already cross-references Background ("at rates documented in Chapter 2") rather than re-stating the evidence. Borderline acceptable; left as-is.
- Citation role duplication (Kaiser in Discussion): Discussion uses Kaiser in warrant role (convergence path) rather than re-stating the Background evidence role. Different role; left as-is.
- Implementation deep-dive issues (C2, C4, C5): The grader identified 8 section-level issues in Implementation (2 HIGH, 6 MEDIUM). These are section-specific, not cross-cutting. Implementation remains the weakest section (20/30) and will be the next revision target when its status resets.

**Status:** CLEAN

## Implementation — Structural Pass 1

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 3 |
| C2: Contribution vs. claim | 4 |
| C3: Ordering | 4 |
| C4: Design intent | 4 |
| C5: Trade-off honesty | 4 |
| C6: Value density | 3 |
| **Total** | **22** |

**Issues from grader:** 7 (2 high, 5 medium)

**What I changed:**
- Issue 1 (HIGH, C1): Added three figures with terminal output as visual evidence — `saturn run ollama` (Figure 4.2), `saturn discover` (Figure 4.3), and Python `discover()` session (Figure 4.4). These are the first figures in the Implementation chapter. Note: actual screenshots of the running system would further strengthen this; the current figures use representative terminal output consistent with the moons knowledge base.
- Issue 2 (HIGH, C1): Added Section 4.4 "System Walkthrough" with three subsections mapping to system goals — Administrator: Deploying a Beacon (infrastructure-layer provisioning), Developer: Discovering and Using a Service (zero-config consumer path), End User: AI Without Configuration (transparency goal). Each walkthrough describes user actions and observable outcomes.
- Issue 3 (MEDIUM, C6): Removed double introductions from six subsection openers (Native SDK, Application Plugin, Tool Protocol Bridge, Subprocess Bridge, Localhost Proxy, Environment Variable Injection). Each subsection now opens with the specific implementation rather than re-defining the pattern already established in the enumerated list.
- Issue 4 (MEDIUM, C6): Tightened Discovery Layer subsection to cross-reference the resolution sequence and describe only implementation-specific details (settle-time value, async browser choice). Removed re-listing of `select_best_service()` filter criteria already defined in Design.
- Issue 5 (MEDIUM, C4): Reframed Open WebUI's five settings by the Valves architecture constraint — "the plugin system's only mechanism for runtime configuration" — rather than listing them as unframed features.
- Issue 6 (MEDIUM, C3): Reordered embedded deployment subsections from Hardware → Rust Binary → OpenWRT → Limitations to OpenWRT Integration → Rust Binary → Hardware Constraints → Limitations. Admin-first ordering: what the administrator sees (LuCI/UCI) before what executes (binary) before platform constraints (hardware). Moved cross-compilation details from Rust Binary into Hardware Constraints where they serve as justification for the size optimization choices.
- Issue 7 (MEDIUM, C2): Replaced evaluative claim in Native SDK circuit breaker description ("a client routes around service failures automatically") with mechanism description: what happens when circuits open, how fallback proceeds, and when requests fail. Defers reliability evaluation to Chapter 5.

**Status:** NEEDS ANOTHER PASS

## Implementation — Structural Pass 2

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 4 |
| C2: Contribution vs. claim | 4 |
| C3: Ordering | 4 |
| C4: Design intent | 3 |
| C5: Trade-off honesty | 4 |
| C6: Value density | 3 |
| **Total** | **22** |

**Issues from grader:** 5 targeted (0 high, 5 medium — grader deep-dived Background this cycle; Implementation issues extracted from priority ranking and cross-cutting notes)

**What I changed:**
- Core Package opening re-introduced three-layer structural preview that subsections immediately deliver. Replaced with technology rationale: Python chosen because AI tooling ecosystem centers on it; `zeroconf` chosen for async support and cross-platform registration with no native dependencies. (criterion: C4)
- Discovery Layer re-described protocol mechanics from Design (service registration under `_saturn._tcp.local.`, TXT record packing). Refocused on implementation-specific details: collision avoidance scan, settle-time trade-off. Removed redundant "Consumers call two functions" sentence already covered in System Walkthrough. (criterion: C6)
- Rust binary section stated "written in Rust" without rationale. Now leads with the hardware constraint that motivates the choice: MIPS32 processor and 16 MB flash rule out interpreted languages. Also ties third-library-in-third-language fact to vendor-independence goal. (criterion: C4)
- Client Integration Patterns opened with "Saturn targets applications that were not built for mDNS discovery" — re-introducing Design context the reader already has. Replaced with direct statement of the integration challenge: each application exposes a different extensibility surface. (criterion: C6)
- SDK provider section re-explained Design's resolution sequence ("resolved which services advertise the requested model, sorted them by priority, and selected the best one"). Compressed to "the provider holds a live, priority-sorted service registry." (criterion: C6)

**Status:** NEEDS ANOTHER PASS

## Implementation — Structural Pass 3

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 4 |
| C2: Contribution vs. claim | 4 |
| C3: Ordering | 5 |
| C4: Design intent | 4 |
| C5: Trade-off honesty | 4 |
| C6: Value density | 3 |
| **Total** | **24** |

**Issues from grader:** C6 remains the weakest criterion across the thesis, driven by cross-cutting refrain repetition and meta-commentary.

**What I changed:**
- Refrain repetition: "no URLs, no keys, no config" appeared 4 times in this chapter (line 121, Fig 4.5 caption, line 249, line 253). Removed all four instances. Line 121 now states the mechanism (mDNS resolution at runtime). Caption states what the call resolves. Line 249 trimmed to the outcome. Line 253 reframed as the user's perspective ("AI capability is a feature of the application"). (criterion: C6)
- Meta-commentary: Line 29 narrated what Table 4.1 "distinguishes" — reframed as a direct statement of original vs. reused work. Line 104 told the reader what the subsections would do — cut the meta sentence. Line 192 opened the walkthrough with "The preceding sections described..." — cut process narration. Line 211 narrated what the terminal output already showed — cut. Line 231 said "The following Python session demonstrates" — cut. (criterion: C6)
- VLC opening: Third sentence ("VLC tests whether the subprocess pattern works...") restated the first sentence. Cut. (criterion: C6)
- Admin walkthrough: "Every device on the local network can now discover the service through mDNS" re-explained mDNS behavior established in Background. Reframed to emphasize the outcome (no further configuration needed). (criterion: C6)

**Status:** CLEAN

## Background — Structural Pass 4

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 4 |
| C2: Contribution vs. claim | 3 |
| C3: Ordering | 4 |
| C4: Design intent | 3 |
| C5: Trade-off honesty | 3 |
| C6: Value density | 3 |
| **Total** | **20** |

**Issues from grader:** 8 (2 high, 6 medium)

**What I changed:**
- Section 2.1 opening re-introduced AIaaS access model already established in Introduction: replaced with cross-reference to Section 1.1 and a sentence scoping the deeper technical examination (criterion: C6)
- Section 2.1.3 restated Meli/Qazi statistics in the same evidence role as Introduction: rewrote to cross-reference Introduction's hook, then advance to deeper details (25% scanner rate, no-expiration-by-default compound failure) that the Introduction did not cover (criterion: C6)
- Section 2.1.1 embedded Saturn design claims ("Saturn adopts it wholesale") in Background: reframed as general observation about the API's ubiquity without naming Saturn (criterion: C2)
- Section 2.5 DHCP mixed background concept with Saturn design rationale: rewrote to present DHCP as a network-level provisioning exemplar and its limits for dynamic, metadata-rich services, without Saturn-specific comparison (criterion: C2)
- Section 2.2 batched all mDNS constraints into trailing sentence: restructured so each of four properties immediately states its corresponding cost inline (criterion: C5)
- Section 2.3 alternative protocols lacked explicit evaluation criteria: added three-criteria framework (no infrastructure, structured metadata, preinstalled stack) before evaluating each protocol against them (criterion: C4)
- Section 2.6.3 gap statement was two sentences: expanded to explain why the gap persists (cloud-first context made discovery unnecessary; AI endpoints carry credentials that mDNS apps never needed) (criterion: C1)
- Added \label{sec:problem} to Introduction Section 1.1 to support new cross-reference from Background

**Not addressed:**
- Issue 7 (C3, MEDIUM): Moving security context sections after mDNS — too large a structural reorder for this pass
- Saturn-specific content remains in TXT Records subsection and Security Context section — these connect Background to the thesis problem per the reference file's rule about covering the chosen approach in depth

**Status:** NEEDS ANOTHER PASS

## Background — Structural Pass 5

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 4 |
| C2: Contribution vs. claim | 3 |
| C3: Ordering | 4 |
| C4: Design intent | 3 |
| C5: Trade-off honesty | 3 |
| C6: Value density | 3 |
| **Total** | **20** |

**Issues from grader:** 7 (2 high, 5 medium)

**What I changed:**
- Issue 4 (C6, HIGH): Removed platform adoption list ("AirPrint, AirPlay, Chromecast, Spotify Connect—on billions of devices") from Section 2.2 opening; that fact now lives only in Section 2.2.4 (Platform Adoption). Replaced with technical characterization of mDNS/DNS-SD.
- Issue 1+7 (C2/C1, HIGH/MEDIUM): Rewrote Section 2.7 gap closing. Removed contribution-claiming sentence ("No system has defined what AI service metadata belongs in a TXT record, how credentials rotate in a broadcast environment, or how to manage the trade-offs that follow") and replaced with observational framing ("The result is a class of network services that remains manually configured despite a mature, preinstalled discovery substrate").
- Issue 2 (C4, MEDIUM): Derived the three alternative-evaluation criteria from the problem domain ("The problem domain from Section 2.1 constrains the choice") instead of presenting them as freestanding requirements.
- Issue 3 (C5, MEDIUM): Added cost statements to alternative protocol dismissals. UPnP now acknowledges cross-subnet discovery capability Saturn lacks. WS-Discovery now acknowledges managed namespaces. Added closing sentence explicitly stating the cost of choosing mDNS (link-local scope, no cross-subnet reach).
- Issue 5 (C6, MEDIUM): Redirected Section 2.1.1 stress position from restating "ubiquity" to stating the unsolved problem: "The wire format is settled; the unsolved problem is how a client finds a server in the first place."

**Not addressed:**
- Issue 6 (C3, MEDIUM): Moving DHCP parallel earlier — too large a structural reorder for this pass; current C3 score is already 4.

**Status:** CLEAN

## Introduction — Cross-cutting Pass 4

**Grader scores (this cycle):**

| Criterion | Score |
|---|---|
| C1: Structural completeness | 5 |
| C2: Contribution vs. claim | 5 |
| C3: Ordering | 4 |
| C4: Design intent | 4 |
| C5: Trade-off honesty | 4 |
| C6: Value density | 3 |
| **Total** | 25 |

**Issues from grader:** 7 (1 high, 6 medium)

**What I changed:**
- Issue 1 (C6, HIGH): Collapsed two-sentence Meli+Qazi evidence paragraph into single claim-level statement with forward reference to Background. Background now owns both citations' evidence role.
- Issue 3 (C3, MEDIUM): Moved Bassignana equity argument from mid-Section 1.1 (where it was a dropped thread between technical paragraphs) to Thesis Statement section where it is explicitly scoped as motivating context.
- Issue 7 (C6, MEDIUM): Removed "A crashed beacon leaves active connections untouched" — unsupported assertion in Introduction; Design Section 3.5.1 already states this with full architectural context.
- Issue 2 (C6, MEDIUM): Trimmed mDNS/DNS-SD re-explanation in Section 1.2. Protocols are named once for context; mechanism explanation left to Background Section 2.2.
- Issue 5 (C6, MEDIUM): Restructured "since Bonjour shipped" sentence so stress position lands on the new insight (AI services need the same three fields printers broadcast) rather than chronological anchor.
- Issue 6 (C5, MEDIUM): Split AP isolation from subordinate clause into its own sentence, signaling it as a deployment-breaking constraint for universities (Saturn's motivating environment) with forward reference to Evaluation.
- Issue 4 (C4, MEDIUM): Reframed nine-component contribution from inventory ("ranging from native SDK integrations to...") to evaluative purpose ("test whether the specification—not the reference implementation—carries the design").

**Status:** CLEAN
