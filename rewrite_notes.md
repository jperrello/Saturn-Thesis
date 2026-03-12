# RALPH Rewrite Notes

## Section Status

| Section | C1 | C2 | C3 | C4 | C5 | C6 | C7 | P1 | P2 | P3 | P4 | P5 | Avg | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Introduction | 91 | 88 | 91 | 84 | 82 | 83 | 90 | 88 | 86 | 80 | 87 | 90 | 87 | NEEDS WORK |
| Background | 91 | 86 | 91 | 83 | 82 | 84 | 88 | 87 | 81 | 81 | 87 | 85 | 86 | NEEDS WORK |
| Design | 91 | 87 | 91 | 88 | 90 | 84 | 83 | 88 | 90 | 83 | 87 | 88 | 87 | NEEDS WORK |
| Implementation | 68 | 86 | 88 | 84 | 83 | 82 | 76 | 84 | 83 | 81 | 84 | 76 | 81 | NEEDS WORK |
| Evaluation | 93 | 92 | 90 | 87 | 90 | 83 | 86 | 87 | 86 | 82 | 87 | 90 | 88 | NEEDS WORK |
| Discussion | 93 | 90 | 86 | 85 | 88 | 81 | 84 | 86 | 87 | 83 | 87 | 88 | 87 | NEEDS WORK |
| Conclusion | 91 | 90 | 92 | 84 | 89 | 88 | 95 | 89 | 92 | 85 | 90 | 88 | 89 | NEEDS WORK |

## Run Log

### Pass 1 — Section Team Revision

**Grader scores:**

| Section | C1 | C2 | C3 | C4 | C5 | C6 | C7 | P1 | P2 | P3 | P4 | P5 | Avg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Introduction | 82 | 78 | 88 | 75 | 72 | 74 | 85 | 84 | 86 | 78 | 82 | 88 | 81 |
| Background | 88 | 82 | 90 | 75 | 68 | 78 | 85 | 82 | 72 | 76 | 84 | 80 | 80 |
| Design | 88 | 82 | 90 | 85 | 88 | 80 | 78 | 84 | 82 | 76 | 83 | 86 | 83 |
| Implementation | 72 | 82 | 86 | 80 | 68 | 74 | 55 | 81 | 78 | 72 | 80 | 84 | 76 |
| Evaluation | 92 | 90 | 88 | 82 | 88 | 78 | 82 | 84 | 80 | 72 | 84 | 90 | 84 |
| Discussion | 92 | 85 | 88 | 78 | 82 | 80 | 85 | 82 | 76 | 74 | 84 | 86 | 83 |
| Conclusion | 92 | 88 | 91 | 78 | 85 | 82 | 95 | 86 | 91 | 83 | 88 | 90 | 87 |

**Sections revised:** Introduction, Background, Design, Implementation, Evaluation, Discussion, Conclusion

**Final pass this cycle:** No — pass 1 is not divisible by 3

**Per-section summary:**

#### Introduction
- Issues from grader: 12 (3 HIGH, 9 MEDIUM)
- What changed:
  - [C2] Replaced description list with prose-woven claims using inline \argref{} tags
  - [C4] Added design intent for mDNS TXT records and no-proxy decision
  - [C5] Added early security trade-off acknowledgment (broadcast visibility + ephemeral mitigation)
  - [C6] Compressed background paragraph from 7 sentences/5 citations to 3 sentences/2 citations
  - [P3] Added short declarative sentences ("The prediction failed for energy. Its logic did not.")
  - [C1/C3] Section now closes on contribution statement after structure preview
  - [P2] Claims paragraph uses first-person voice
  - [P4] Gap statement leads rather than following citation inventory
  - [P5] Bridged transition from personal experience to protocol need
- Status: NEEDS WORK (avg 81)

#### Background
- Issues from grader: 12 (3 HIGH, 9 MEDIUM)
- What changed:
  - [C4] Added positive argument for mDNS choice before trade-offs ("I chose mDNS/DNS-SD because...")
  - [C5] Added explicit trade-offs: 255-byte TXT limit, link-local scope, no authentication, multicast scaling
  - [P2] Introduced first-person throughout all sections
  - [C1] Compressed alternatives to 1-2 sentences each, removed internal mechanics
  - [C2] Gap section now explicitly names all three thesis claims
  - [C6] Removed "billions of devices" refrain and DHCP truism; added concrete comparisons
  - [C7] Folded privacy subsection into parent
  - [P1] AI consumers section uses flowing prose with consistent "configuration burden" topic string
  - [P3] Varied sentence structures across alternatives
  - [P4] AI consumers section opens with argumentative claim
  - [P5] Concrete byte comparison for WS-Discovery, specific ports/layers for DHCP
- Status: NEEDS WORK (avg 80)

#### Design
- Issues from grader: 12 (2 HIGH, 10 MEDIUM)
- What changed:
  - [C6] Removed DNS Record Structure subsection (redundant with Background); replaced with cross-reference
  - [C7] Removed Summary section and post-table paragraph; ~30-line reduction
  - [P2] Added first-person throughout including Security threat models ("I do not want companies like OpenAI...")
  - [P3] Broke uniform sentence patterns with short declaratives and rhetorical questions
  - [C1] Added work type statement (engineering contribution) to opening
  - [C2] Reframed "zero-configuration consumer access" as design constraint
  - [C4] Priorities subsection opens with design intent before mechanism
  - [C5] Replaced vague "modestly" with concrete costs
  - [P1] Beacons deployment types flow as paragraph rather than inventory
  - [P4] Discovery Flow opens with significance claim
  - [P5] Added concrete example for administrative centralization
- Status: NEEDS WORK (avg 83)

#### Implementation
- Issues from grader: 14 (3 HIGH, 11 MEDIUM)
- What changed:
  - [C1] Added three figure TODO placeholders (actual screenshots needed)
  - [C5] Added trade-offs: VLC GET payload limits, Python process delay, Rust ecosystem constraints, fetch monkey-patching fragility
  - [C7] Reduced from 269 to ~165 lines (39% reduction); merged subsections, eliminated "What X Proves"
  - [C2] Replaced "proves" with "demonstrates" throughout
  - [C3] Added "This project had a deadline" narrative context
  - [C4] Stated scope boundaries (macOS-only for VLC, single router model)
  - [C6] Compressed Rust binary and OpenWRT descriptions to functional narratives
  - [P2] Added first-person in Shared Foundation and all sections
  - [P3] Added short punchy sentences and varied structure
  - [P4] OpenWRT paragraph states collective purpose before listing components
  - [P5] Added descriptions for Open WebUI plugin and MCP server at first mention
- Status: NEEDS WORK (avg 76)

#### Evaluation
- Issues from grader: 11 (3 HIGH, 8 MEDIUM)
- What changed:
  - [C4] Added justification for R1/R2/R3 decomposition (find/connect/interoperate lifecycle)
  - [C6] Removed Background-level re-explanations of cognitive walkthroughs and Nielsen; compressed scaling arithmetic
  - [P2] Injected first-person throughout results ("I wrote all six," "This is the result I find most telling")
  - [P3] Added short declarative sentences for emphasis ("That is the cost." "It is structural.")
  - [C5] Added step-counting limitation acknowledgment in Claim 2 Assessment
  - [C7] Compressed Nielsen section by ~40%
  - [P1] Rewrote STRIDE paragraph with consistent topic string
  - [P4] Restructured Claim 1 Assessment to lead with positive findings
  - [P5] Added concrete vocabulary alternative in H2 trade-off
- Status: NEEDS WORK (avg 84)

#### Discussion
- Issues from grader: 11 (3 HIGH, 8 MEDIUM)
- What changed:
  - [P2] Rewrote with first-person voice throughout ("I began," "I believe," "I deliberately inverted")
  - [P3] Broke uniform compound sentence patterns; added short emphatic sentences ("Four steps." "Students pay nothing upfront.")
  - [C4] Added design intent framing to all three future work items with success criteria
  - [C6] Removed re-explanation of Saturn mechanics and redundant printer analogy
  - [C3] Reordered prior work: BeyondCorp philosophical frame before detailed security findings
  - [C5] Added governance/resource-exhaustion trade-off paragraph for university scenario
  - [C2] Separated walkthrough artifact from implication
  - [P1] Stabilized topic strings in prior work paragraphs
  - [P4] Significance section builds to "protocol problem, not cost problem" as closing punch
  - [P5] Costa et al. connection demonstrated with specific definitions
  - [C7] Compressed significance section from 8 to 5 sentences
- Status: NEEDS WORK (avg 83)

#### Conclusion
- Issues from grader: 8 (2 HIGH, 6 MEDIUM)
- What changed:
  - [C4] Rewrote paragraph 3 to state design intent positively before limitations
  - [C6] Removed re-reported evaluation numbers; synthesized findings instead
  - [P3] Broke monotonous rhythm with varied sentence lengths
  - [C2] Split paragraph 2 into contributions proved + their limits
  - [C5] Added trade-off synthesis for all three claims including cognitive walkthrough limitation
  - [P1] Stabilized paragraph 4 topic string
  - [P4] Adoption-dependency claim in its own sentence at paragraph boundary
- Status: NEEDS WORK (avg 87)

### Pass 2 — Section Team Revision

**Grader scores:**

| Section | C1 | C2 | C3 | C4 | C5 | C6 | C7 | P1 | P2 | P3 | P4 | P5 | Avg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Introduction | 88 | 84 | 90 | 80 | 78 | 79 | 88 | 86 | 84 | 82 | 85 | 88 | 84 |
| Background | 90 | 84 | 91 | 80 | 76 | 82 | 88 | 85 | 78 | 79 | 86 | 83 | 84 |
| Design | 90 | 85 | 91 | 87 | 89 | 82 | 80 | 86 | 88 | 80 | 85 | 88 | 86 |
| Implementation | 68 | 84 | 88 | 82 | 78 | 80 | 72 | 83 | 82 | 78 | 82 | 74 | 79 |
| Evaluation | 92 | 91 | 88 | 84 | 89 | 80 | 83 | 85 | 83 | 78 | 85 | 90 | 86 |
| Discussion | 93 | 88 | 86 | 82 | 85 | 78 | 82 | 84 | 83 | 80 | 86 | 88 | 85 |
| Conclusion | 93 | 90 | 91 | 80 | 86 | 84 | 95 | 88 | 92 | 85 | 89 | 88 | 89 |

**Sections revised:** Introduction, Background, Design, Implementation, Evaluation, Discussion, Conclusion

**Final pass this cycle:** No — pass 2 is not divisible by 3

**Per-section summary:**

#### Introduction
- Issues from grader: 12 (2 HIGH, 10 MEDIUM)
- What changed:
  - [C4] Added explicit design intent for mDNS/DNS-SD choice over UPnP/SLP
  - [C5] Added trade-off costs to V1 (link-local scope) and V2 (admin burden shift)
  - [C6] Compressed paragraph 2 by removing redundant AI-prefix triple and duplicated access-model point
  - [C6] Trimmed structure preview from 7 detail-heavy lines to 6 compact entries
  - [C1] Moved gap statement earlier in paragraph 3 with bridge from personal experience
  - [C2] Separated Saturn definition from design rationale; security trade-off moved to claims paragraph
  - [C3] Stripped V3 forward-reference from definition paragraph
  - [C7] Split long definition paragraph; extracted admin/consumer operational model
  - [P1] Added bridging in paragraph 3 from personal experience to gap
  - [P2] Rewrote paragraphs 1-2 with author perspective framing citations
  - [P3] Varied claims paragraph structure; removed identical First/Second/Third template
  - [P4] Strengthened "whether to how" pivot as paragraph climax
- Status: NEEDS WORK (avg 84)

#### Background
- Issues from grader: 12 (3 HIGH, 9 MEDIUM)
- What changed:
  - [C4] Added three-criteria evaluation framework applied consistently to each alternative
  - [C5] Replaced advocacy "No alternative provides all three" with trade-off acknowledgment
  - [P2] Rewrote AI consumers section with first-person experience (LibreChat/Open WebUI deployment, Continue daily use, VS Code mDNS discovery)
  - [C2] Rewrote gap section separating open problem from empirical questions
  - [C5] Added Saturn cost: requires administrator to run beacon
  - [C6] Compressed developer configuration enumeration from 4 steps to 2 clauses
  - [C6] Restructured DHCP comparison to lead with Saturn property
  - [P1] Reorganized platform implementations around findings not actors
  - [P3] Compressed Section 2.1 opening; added short declarative for emphasis
  - [P4] Added sufficiency claim to TXT records subsection
  - [P5] Added UDP ports 137-138, 15-char limit, 2015 deprecation to NetBIOS
- Status: NEEDS WORK (avg 84)

#### Design
- Issues from grader: 11 (2 HIGH, 9 MEDIUM)
- What changed:
  - [C6] Compressed beacon-not-proxy from 3 paragraphs to 2
  - [C7] Net reduction ~20 lines; compressed beacon-not-proxy, broadcast exposure, opening
  - [C6] Reduced product inventory from 7 to 5 products
  - [C2] Removed evaluation methodology preview from opening
  - [C4] Replaced meta-organizational concepts opening with goal-linked framing
  - [P1] Cut meta-justification for security section placement
  - [P2] Added authorial voice to discovery flow framing
  - [P3] Varied four design goal paragraphs with different entry points
  - [P3] Rewrote TXT schema post-table prose with varied sentence lengths
  - [P4] Moved API choice rationale to emphasis position
  - [P5] Added concrete student-on-campus example to end user paragraph
- Status: NEEDS WORK (avg 86)

#### Implementation
- Issues from grader: 14 (3 HIGH, 11 MEDIUM)
- What changed:
  - [C1] Prose works around absent figures; TODO placeholders preserved
  - [C1] Summary reframes Open WebUI/MCP as supporting artifacts
  - [C2] Closing paragraphs rewritten to describe what was built, not evaluate
  - [C3] Shared Foundation separates reused dependencies from original work
  - [C4] OpenCode section explains fork decision (runtime provider registration needed)
  - [C5] Added architectural cost of dynamic registration
  - [C6] Summary compressed; no parenthetical mini-introductions
  - [P1] Dynamic registration paragraph rewritten with consistent topic string
  - [P2] OpenWRT paragraph rewritten with first-person active voice
  - [P3] Router section has varied sentence lengths with short declaratives
  - [P4] Integration challenges leads with insight, presents bugs as evidence
  - [P5] Added concrete end-to-end OpenCode-Saturn walkthrough
  - [P5] Ephemeral credentials grounded with specifics (32-char, 10-min expiry, 5-min rotation)
- Status: NEEDS WORK (avg 79)

#### Evaluation
- Issues from grader: 11 (3 HIGH, 8 MEDIUM)
- What changed:
  - [C4] Added existence-proof methodology framing (what it enables vs. what it cannot show)
  - [C6] Merged "What Drives the Reduction" into Results subsection
  - [C6] Cut meta-promise final sentence of paragraph 2
  - [C7] Collapsed three Nielsen subsections into paragraph entries in parent section
  - [P1] Restructured STRIDE comparison to eliminate ping-pong alternation
  - [P2] Injected first-person voice throughout Nielsen section
  - [P2] Connected R1 results to access equity motivation from Introduction
  - [P3] Reorganized Nielsen findings by claim with varied structure
  - [P3] Varied sentence length in Information Leakage paragraph
  - [P4] Restructured Threats section: three named categories matching three paragraphs
  - [C3] Reorganized Nielsen by claim with explicit cross-references
- Status: NEEDS WORK (avg 86)

#### Discussion
- Issues from grader: 12 (3 HIGH, 9 MEDIUM)
- What changed:
  - [C4] Third limitation connects schema drift to deliberate extensibility design choice
  - [C6] Compressed repeated analogy and metadata re-enumeration
  - [P2] Prior Work paragraphs rewritten with first-person interpretive voice
  - [P3] Limitation blocks now vary in internal rhythm with short declaratives
  - [C2] Hedged Costa et al. "both dimensions" claim
  - [C3] Reorganized Prior Work: grouped all mDNS material, then BeyondCorp
  - [C5] Developer benefit paragraph names runtime dependency trade-off
  - [C7] Folded Significance section into closing paragraph of Future Work
  - [P1] Replaced ambiguous "This" with specific noun phrase
  - [P3] Future work paragraphs vary in structure
  - [P4] Prior Work opens with question before answer
- Status: NEEDS WORK (avg 85)

#### Conclusion
- Issues from grader: 8 (1 HIGH, 7 MEDIUM)
- What changed:
  - [C4] Added explicit clause: multicast is prerequisite, solving WiFi infrastructure compromises zero-config guarantee
  - [C5] Reframed adoption as cost: administrators bear effort with limited return until critical mass
  - [C6] Deleted meta-commentary "These limits are real..." sentences
  - [C6] Compressed printer/file-share analogy to brief echo
  - [P1] Bridged paragraph 3 opening from limits to "what comes next"
  - [P3] Varied three claim restatements: no longer identical "It proved that..." template
  - [P4] Moved "value compounds" to emphasis-position sentence
  - [P5] Replaced generic "empirical user studies" with specific study: university residence-hall beacon deployment
- Status: NEEDS WORK (avg 89)

### Pass 3 — Section Team Revision

**Grader scores:**

| Section | C1 | C2 | C3 | C4 | C5 | C6 | C7 | P1 | P2 | P3 | P4 | P5 | Avg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Introduction | 90 | 86 | 91 | 82 | 80 | 81 | 90 | 87 | 85 | 78 | 86 | 89 | 85 |
| Background | 91 | 85 | 91 | 82 | 80 | 83 | 89 | 86 | 80 | 80 | 87 | 84 | 85 |
| Design | 91 | 86 | 91 | 88 | 90 | 83 | 82 | 87 | 89 | 82 | 86 | 88 | 88 |
| Implementation | 72 | 86 | 88 | 83 | 82 | 82 | 78 | 84 | 84 | 80 | 83 | 78 | 82 |
| Evaluation | 93 | 91 | 89 | 86 | 90 | 82 | 85 | 86 | 85 | 80 | 86 | 90 | 87 |
| Discussion | 93 | 89 | 87 | 84 | 87 | 80 | 83 | 85 | 85 | 82 | 87 | 88 | 86 |
| Conclusion | 93 | 91 | 92 | 82 | 88 | 86 | 95 | 89 | 93 | 86 | 90 | 89 | 89 |

**Sections revised:** Introduction, Background, Design, Implementation, Evaluation, Discussion, Conclusion

**Final pass this cycle:** Yes — pass 3 is divisible by 3

**Per-section summary:**

#### Introduction
- Issues from grader: 11 (3 HIGH, 8 MEDIUM)
- What changed:
  - [C4] Design intent now explicit — Saturn definition paragraph ends on beacon vs. proxy distinction with optimization/sacrifice statement
  - [C5] Trade-offs rewritten as deliberate design consequences, not trailing qualifiers
  - [C6] Paragraph 2 compressed — Bassignana/Gabriel merged, closing re-statement removed
  - [P3] Claims broken into three separate paragraphs with varied sentence structures (short declaratives, evidence-first, reasoning-first)
  - [C2] Artifacts paragraph added before claims, naming protocol, six implementations, and walkthrough methodology
  - [P1] Paragraph 4 opens with gap connection before introducing mDNS/DNS-SD
  - [P2] Paragraph 2 opens with author's interpretive frame
  - [P3] Structure preview compressed from six sentences to three
  - [P4] Saturn definition paragraph ends on beacon architecture distinction
  - [P5] Specific cost figure added ($0.15 per million input tokens for GPT-4o mini)
- Status: NEEDS WORK (avg 85)

#### Background
- Issues from grader: 12 (3 HIGH, 9 MEDIUM)
- What changed:
  - [C4] Three requirements moved into Section 2.1 before mDNS coverage; mDNS section now opens by satisfying stated requirements
  - [C5] Broadcast-visibility cost paragraph added to AI consumers section
  - [P2] Author's voice threaded through mDNS mechanics ("No central server. No account.", personal AirPrint parallel)
  - [C2] Saturn design decisions forward-reference Chapter 3
  - [C6] Product name-drops removed; Siddiqui compressed to single clause
  - [P1] Platform Implementations split into availability/interoperability and privacy paragraphs
  - [P2] Problem statement grounded in author's personal experience before citations
  - [P3] Alternative protocols varied: dismissal-first, strength-first, near-viability, inheritance
  - [P4] Platform Implementations framed around potential obstacle and resolution
  - [P5] Concrete scenario added (50 students × 3 backends = 150 configurations)
- Status: NEEDS WORK (avg 85)

#### Design
- Issues from grader: 11 (2 HIGH, 9 MEDIUM)
- What changed:
  - [C6] Beacon-Not-Proxy rewritten to cross-reference Section 3.3.2 properties; focused on deliberation (why proxy was attractive, why insufficient)
  - [C7] Net 4-line reduction — compressed Design Goals, discovery flow, Priority as Policy cross-reference, OpenAI API subsection
  - [P3] Design Goals varied — admin centralization punchy 2-line, security posture short declarative
  - [C2] Removed "not a hypothesis but a design constraint" and DHCP evaluative comparison
  - [C4] Added TXT-inline vs HTTPS bootstrap credential transport justification
  - [C6] Deleted meta-statement from Priorities
  - [P1] Threat Model 2 topic string stabilized on "administrator"
  - [P2] Protocol Specification meta-commentary replaced with substantive opening
  - [P4] "Sidestep this failure class" moved to paragraph-closing emphasis position
  - [P5] Concrete `discover()` function call added for developer paragraph
- Status: NEEDS WORK (avg 88)

#### Implementation
- Issues from grader: 15 (3 HIGH, 12 MEDIUM)
- What changed:
  - [C3] Shared Foundation compressed from 3 paragraphs to 1; process narration eliminated
  - [C4] Fork rationale states scope (dynamic provider discovery) and deliberate exclusions (no UI changes)
  - [C5] Dynamic registration failure consequence grounded (stale reference → silent request failure)
  - [C5] Bridge pattern generalization qualified with inherited costs
  - [C6] "This project had a deadline" deleted; time pressure folded into progression sentence
  - [C6] VLC closing replaced with insight about value scaling with host constraints
  - [C7] Shared Foundation compressed ~10→4 lines; Bun timeout bug compressed to 2 sentences; ~15 lines recovered
  - [P1] Dynamic registration topic string stabilized
  - [P2] First person added at router architecture, file count, SDK layer
  - [P3] OpenWRT "I [verb] a [noun]" pattern broken with varied openings
  - [P4] Integration challenges reordered with explicit escalation (mildest → most disruptive)
  - [P5] "backend-agnostic proxying" replaced with concrete backend list (OpenRouter, Ollama, direct provider API)
  - [P5] Open WebUI plugin and MCP server given one-clause descriptions
- Status: NEEDS WORK (avg 82)

#### Evaluation
- Issues from grader: 11 (2 HIGH, 9 MEDIUM)
- What changed:
  - [C6] Existence proof tutorial compressed from 5 sentences to 1 clause plus requirement decomposition
  - [P3] STRIDE rewritten with varied structures: dependent clause, short rhetorical question, first-person design statement
  - [C3] Redundant argument ID mapping removed (argrefs already inline)
  - [C4] Single-author heuristic evaluation justified (35% coverage rate, structured friction check)
  - [C6] Redundant results paragraph compressed from 5 to 2 sentences
  - [C7] Cognitive walkthrough justification compressed from 3 sentences to 1
  - [P1] Information Leakage Surface topic string unified around TXT fields
  - [P2] First-person voice added to STRIDE section
  - [P3] Nielsen heuristic paragraph H[N] pattern varied
  - [P4] Threats to Validity reordered weakest→strongest; ends on most consequential limitation
  - [C6] Result preview removed from Claim 2 opening
- Status: NEEDS WORK (avg 87)

#### Discussion
- Issues from grader: 13 (3 HIGH, 10 MEDIUM)
- What changed:
  - [C4] Design rationale for mDNS-only added before hybrid discovery future work proposal
  - [C6] Syed et al. repurposed from redundant config-burden to distinct lock-in claim
  - [P3] Limitations rewritten with varied structures — short declaratives ("Seven to zero.", "It may not."), first-person openers
  - [C1] Closing paragraph synthesizes discussion's interpretive thread instead of restating evaluation evidence
  - [C2] Costa et al. paragraph leads with measured finding, then pivots to interpretive framework
  - [C3] AP isolation consolidated — Prior Work cross-references Limitations instead of repeating
  - [C5] Transparency/consent concern added to passive discovery paragraph
  - [C6] Artifact inventory removed from third limitation; led with interpretive point
  - [C7] Closing paragraph compressed from 5 to 3 sentences
  - [P1] "That model" replaced with "Shared token provisioning"
  - [P1] Prior Work stress position restructured to land on the gap
  - [P2] Limitations section opened with first-person framing
  - [P4] Future Work meta-organizational opener cut; opens with design rationale
- Status: NEEDS WORK (avg 86)

#### Conclusion
- Issues from grader: 7 (1 HIGH, 6 MEDIUM)
- What changed:
  - [C4] Kaiser citation and AP isolation rationale removed; limits stated as factual boundaries without re-justification (PLATEAU FIX — 3 passes in 78-82 band)
  - [C5] Claims interleaved with boundaries in same paragraph rather than separated
  - [C6] AP isolation reduced to subordinate clause; adoption compressed to single clause; merged 2 paragraphs into 1
  - [P1] Topic string stabilized around three claims (V1, V2, V3) as recurring subjects
  - [P3] Short declarative for V2 (8 words); varied compound patterns across V1/V3
  - [P5] "Discover and use" replaced with "send their first query within twenty-four hours of joining"
- Status: NEEDS WORK (avg 89)

#### Final Pass (pass 3)
- Edits made: 8
- Issues deferred to section teams: 3
- Fixed: Kaiser/Waldvogel+Konings cross-section repetition (Design, Evaluation → cross-references to Background), "Saturn server"→"Saturn beacon" (Discussion ×2), "VLC plugin"→"VLC extension" (Discussion), broken \ref{ch:scenarios} removed (Introduction), opening/closing handoffs added (Implementation→Design, Implementation→Evaluation, Evaluation→Discussion)
- Deferred: "six implementations" vs "seven consumers" count reconciliation, VLC "subtitle translation" in Discussion not established in Implementation, Meli et al. 81% statistic appears in 4 chapters (distinct roles but verbatim repetition)

### Pass 4 — Section Team Revision

**Grader scores:**

| Section | C1 | C2 | C3 | C4 | C5 | C6 | C7 | P1 | P2 | P3 | P4 | P5 | Avg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Introduction | 91 | 88 | 91 | 84 | 82 | 83 | 90 | 88 | 86 | 80 | 87 | 90 | 87 |
| Background | 91 | 86 | 91 | 83 | 82 | 84 | 88 | 87 | 81 | 81 | 87 | 85 | 86 |
| Design | 91 | 87 | 91 | 88 | 90 | 84 | 83 | 88 | 90 | 83 | 87 | 88 | 87 |
| Implementation | 68 | 86 | 88 | 84 | 83 | 82 | 76 | 84 | 83 | 81 | 84 | 76 | 81 |
| Evaluation | 93 | 92 | 90 | 87 | 90 | 83 | 86 | 87 | 86 | 82 | 87 | 90 | 88 |
| Discussion | 93 | 90 | 86 | 85 | 88 | 81 | 84 | 86 | 87 | 83 | 87 | 88 | 87 |
| Conclusion | 91 | 90 | 92 | 84 | 89 | 88 | 95 | 89 | 92 | 85 | 90 | 88 | 89 |

**Sections revised:** Introduction, Background, Design, Implementation, Evaluation, Discussion, Conclusion

**Final pass this cycle:** No — pass 4 is not divisible by 3

**Per-section summary:**

#### Introduction
- Issues from grader: 9 (3 HIGH, 6 MEDIUM)
- What changed:
  - [C4] Rewrote mDNS paragraph to state optimization target ("zero infrastructure") first, then explain why UPnP/SLP fail it
  - [C5] V1 now names what link-local scope prevents: multi-building campuses and routed networks
  - [P3] PLATEAU FIX — Redesigned all three claim paragraphs with different architectures: V1 opens with evidence, V2 opens with question, V3 opens with trade-off. Sentence counts differ (6, 5, 4)
  - [C2] Removed cognitive walkthrough from artifacts list; repositioned as evaluation method
  - [C6] Cut bundled-plans sentence; split structure preview into per-chapter clauses
  - [P1] Paragraph 4 stress position now names "mDNS/DNS-SD" specifically
  - [P2] Personal motivation ("I wanted to break that bottleneck") now in paragraph 1
  - [P4] Split Saturn definition from design rationale/beacon-vs-proxy into separate paragraphs
- Status: NEEDS WORK (avg 87)

#### Background
- Issues from grader: 10 (3 HIGH, 7 MEDIUM)
- What changed:
  - [C4] mDNS section now opens with mechanics before satisfaction claim
  - [C5] Grounded beacon cost: TOML file, one env var, $30 router or spare machine
  - [P2] NEAR-PLATEAU FIX — Rewrote mDNS mechanics from author's perspective throughout; technical paragraphs explain why mechanics matter to the problem
  - [P3] NEAR-PLATEAU FIX — Varied alternatives rhythm: NetBIOS gets 3-word verdict, WS-Discovery opens with concessive clause, UPnP with dependent clause, DLNA shortened to 2 sentences
  - [C2] Added argref V1/V2/V3 labels to gap section's empirical questions
  - [C6] Consolidated forward references; "ephemeral keys and spending limits" appears once per section
  - [C7] Folded TXT Records subsection into parent mDNS section
  - [P1] AI consumers restructured around 3 category subjects with products as evidence
  - [P4] DHCP insight moved to paragraph-opening emphasis position
  - [P5] UPnP: replaced generic "documented history" with US-CERT advisory and specific vulnerability
- Status: NEEDS WORK (avg 86)

#### Design
- Issues from grader: 10 (3 HIGH, 7 MEDIUM)
- What changed:
  - [P3] PLATEAU FIX — Varied concept subsection openings: Endpoints opens with problem, Beacons with question, Ephemeral Keys with evidence (Meli et al.)
  - [C6] PLATEAU FIX — Removed GL.iNet hardware from Beacon-Not-Proxy; replaced with design-level cross-reference to Ch4; eliminated Section 3.3.2 restatement
  - [C7] PLATEAU FIX — Compressed Broadcast Exposure via cross-reference to Section 3.3.4; shortened Administrative centralization; compressed OpenAI API product list. Net -12 lines
  - [C2] Flagged security mitigations as design-time claims evaluated in Ch6
  - [C4] Explained three-role decomposition optimizes for separating credential management, integration logic, and usage
  - [P1] Priority as Policy opens from multi-attribute alternative, lands on Saturn's choice in stress position
  - [P4] Protocol Specification opens with positioning relative to Concepts section
  - [P5] Threat Model 1 leads with concrete action (deploy Ollama, set priority), then names property
- Status: NEEDS WORK (avg 87)

#### Implementation
- Issues from grader: 14 (3 HIGH, 11 MEDIUM)
- What changed:
  - [C1] PLATEAU FIX — Added three figure environments with placeholder filenames (vlc-chat.png, luci-config.png, opencode-saturn.png), each referenced in prose before figure, with descriptive captions
  - [C1] Restructured Shared Foundation: reused dependencies first, then original work
  - [C2] Removed evaluative "value scales with constraints" from VLC section
  - [C3] Replaced "Some readers may object" with subordinate clause framing
  - [C4] dns-sd CLI rationale: serves non-technical users who install by copying single directory
  - [C5] Stated loader-layer confinement forced dynamic registration workaround with stale-reference cost
  - [C6] Summary cross-references Section 4.1 for SDK packages; enumerates all 7 artifacts with languages and mDNS libraries
  - [C7] Cross-referenced ephemeral key specifics to Section 3.3.4; compressed OpenWRT, bridge pattern, OpenCode walkthrough
  - [P1] Dynamic registration paragraph: OpenCode as consistent grammatical subject
  - [P2] Bridge pattern generalization in first person
  - [P3] Router paragraph: short declarative ("Rust was the only realistic choice"), varied openings
  - [P4] Three bug paragraphs varied: first leads with bug, second with consequence, third with fix
  - [P5] OpenCode introduced with concrete scenario instead of abstract labels
  - [P5] All 7 artifacts enumerated in summary with languages and mDNS libraries
- Status: NEEDS WORK (avg 81)

#### Evaluation
- Issues from grader: 11 (2 HIGH, 9 MEDIUM)
- What changed:
  - [C6] PLATEAU FIX — Removed re-introduction of discover()/SaturnService internals and GL.iNet hardware; cross-referenced instead
  - [P3] PLATEAU FIX — Varied assessment templates: Claim 1 opens with limitation, Claim 2 opens with strongest finding, Claim 3 retains philosophical framing
  - [C4] Step-counting optimizes for reproducibility/structural comparison, sacrifices time measurement
  - [C6] Meli et al. statistics replaced with cross-reference to Section 3.3.4
  - [C7] Tightened Nielsen opening paragraph
  - [P1] STRIDE paragraph: unified topic string around ephemeral credentials; discovery paragraph: Saturn as controlling subject
  - [P2] Connected R2 result to society-level benefit (any developer can integrate AI)
  - [P3] Threats to Validity: measurement limitations opens with question; restructured forward reference
  - [C3] Nielsen paragraphs renamed by finding valence: "What works," "What creates friction," "What is missing"
  - [P4] "Complexity centralizes" moved to paragraph-opening emphasis position
- Status: NEEDS WORK (avg 88)

#### Discussion
- Issues from grader: 12 (1 HIGH, 11 MEDIUM)
- What changed:
  - [C6] PLATEAU FIX — Rewrote paragraphs to open with interpretation, reference evidence parenthetically; compressed Syed lock-in + runtime dependency into single trade-off framing; removed VLC Implementation cross-reference
  - [C6] Opening paragraph: evaluation restatement compressed to subordinate reference to Ch6
  - [C3] Reordered: Implications → Limitations → Prior Work → Future Work
  - [C4] Added Saturn design intent clause (TXT credentials, zero-config vs broadcast exposure)
  - [C5] Unicast fallback cost stated explicitly
  - [P5] Concrete hybrid discovery flow example (eduroam mDNS query + saturn.ucsc.edu fallback)
  - [P2] Future Work rewritten with first person ("I would run...")
  - [P3] Limitation paragraphs varied: first keeps bold header, second opens with consequence, third moves bold header mid-sentence
  - [P3] University provisioning: combined two short sentences to break four-consecutive-medium pattern
  - [P4] Final sentence replaced with domain claim ("next generation of students will encounter AI the way they currently encounter Wi-Fi")
  - [P1] Prior Work paragraph 1 ends on "broadcast exposure" for smooth transition
- Status: NEEDS WORK (avg 87)

#### Conclusion
- Issues from grader: 7 (1 HIGH, 6 MEDIUM)
- What changed:
  - [C4] PLATEAU FIX — Opened paragraph 2 with design philosophy ("zero-config over zero-trust") as frame; three claims validate that philosophy
  - [C5] Adoption trade-off integrated into V2 boundary statement
  - [C6] Compressed "single service type" + "heterogeneous AI ecosystems" into one boundary
  - [P1] Replaced weak "These limits" with specific thread pickup from V2's behavioral assumption
  - [P3] Varied claim-caveat rhythm: V1 semicolon pivot, V2 leads with concrete number, V3 comma-but
  - [C1] Added domain implication: "Any network that already supports mDNS can provision AI services today"
  - [P5] Replaced "approaching zero" with concrete $0.15/million tokens figure
- Status: NEEDS WORK (avg 89)
