---
name: structured-arguments
description: "Use this skill when working with labeled thesis arguments — creating, referencing, or weaving definitions (D), views (V), arguments (A), alternative views (AV), counter-arguments (CA), rebuttals, or barriers (B) into the thesis. Trigger when the user mentions argument IDs, cross-references, or wants to build/extend the argument scaffold."
---

# Structured Arguments Skill

Modeled after Belcak et al. (2025) "Small Language Models are the Future of Agentic AI" — a position paper that labels every claim, argument, and counter-argument with short IDs and cross-references them throughout.

## Element Taxonomy

Every element gets a **short ID prefix + number** and explicitly declares what it supports or attacks.

| Prefix | Type | Purpose | Example |
|--------|------|---------|---------|
| **D** | Definition | Working definition anchoring a key term | D1: "Saturn is a zero-configuration..." |
| **V** | View | Core thesis claim (the position) | V1: "Zero-config AI provisioning is feasible" |
| **A** | Argument | Evidence or reasoning supporting a view | A1: "Six implementations prove feasibility" → V1 |
| **AV** | Alternative View | A counterposition from literature or practice | AV1: "Trust-the-network violates zero-trust" → disputes V3 |
| **CA** | Counter-Argument | Specific reasoning backing an alternative view | CA1: "BeyondCorp requires device-level auth" → supports AV1 |
| **B** | Barrier | Practical obstacle to adoption (not a logical counter) | B1: "No ecosystem adoption yet" |
| **S** | Step | Procedural/algorithmic step in a process | S1: "Discover services via mDNS" |

## Rules

1. **Every A must link to at least one V.** State it explicitly: "This argument supports view V1."
2. **Every AV must identify which V it disputes.** "This alternative view challenges V2."
3. **Every CA must link to an AV.** Counter-arguments exist in service of an alternative view.
4. **Rebuttals reference by ID.** "We address counter-argument CA1 with arguments A3 and A7."
5. **Cross-references use IDs inline.** "As shown in argument A2..." not "As shown previously..."
6. **IDs are stable.** Once assigned, an ID never changes meaning. New elements get new numbers.

## Registry

The argument registry lives at `moons/claims/argument-registry.md`. It is the single source of truth for all labeled elements. Before creating a new element, check the registry to avoid ID collisions.

### Registry Format

```markdown
## Definitions
- **D1**: [term] — [one-line definition]

## Views (Thesis Claims)
- **V1**: [one-line claim statement] — discussed in [chapters]
- **V2**: ...

## Arguments
- **A1**: [one-line summary] → supports **V1** — [evidence type: existence proof | literature | measurement | comparison]
- **A2**: ...

## Alternative Views
- **AV1**: [one-line counterposition] → disputes **V1** — [source: literature | practice | reviewer]

## Counter-Arguments
- **CA1**: [one-line reasoning] → supports **AV1** — [source]

## Barriers
- **B1**: [one-line obstacle] — [status: active | diminishing | addressed]
```

## LaTeX Integration

Use these commands in `thesis.tex` for labeled arguments. Define them in the preamble:

```latex
% Structured argument labels
\newcommand{\argref}[1]{\textbf{#1}}  % inline reference: \argref{V1}
\newcommand{\argdef}[2]{\noindent\textbf{#1}\quad #2}  % definition block: \argdef{A1}{SLMs are...}
```

### Rendering Patterns

**Definition block** (like the paper's WD1, WD2):
```latex
\begin{description}
  \item[\argref{D1}] A \emph{Saturn service} is any AI endpoint advertised via \texttt{\_saturn.\_tcp.local.} mDNS records.
\end{description}
```

**View statement** (like V1, V2, V3):
```latex
We contend that:
\begin{description}
  \item[\argref{V1}] Zero-configuration network protocols can provision AI services without end-user configuration;
  \item[\argref{V2}] network-provisioned AI reduces total configuration effort compared to per-user manual setup;
  \item[\argref{V3}] the security trade-offs of broadcast AI discovery are documented and addressable.
\end{description}
```

**Argument block** (like A1, A2):
```latex
\subsubsection{Six implementations prove feasibility}
\begin{description}
  \item[\argref{A1}] Saturn's six independent client implementations demonstrate that mDNS/DNS-SD can provision AI services across languages and platforms. This argument supports view~\argref{V1}.
\end{description}
```

**Cross-reference in prose**:
```latex
As established in argument~\argref{A1}, the protocol works across five mDNS libraries.
We address counter-argument~\argref{CA1} in Section~\ref{sec:rebuttals}.
```

## Workflow

### Creating a New Element

1. Read `moons/claims/argument-registry.md` to find the next available ID.
2. Draft the element with its one-line statement and linkage.
3. Add it to the registry.
4. If the element belongs in a specific chapter, note the chapter in the registry entry.
5. When writing the chapter content, use the LaTeX patterns above.

### Weaving Arguments Into Prose

When writing a thesis section that involves arguments:

1. Identify which V/A/AV/CA elements are relevant to the section.
2. Introduce the view (V) first, then present supporting arguments (A) with evidence.
3. Present alternative views (AV) honestly, then their counter-arguments (CA).
4. Rebut with cross-references to your own arguments.
5. Every cross-reference uses the ID: "see argument A3" not "see above."

### Mapping Saturn's Existing Claims

The three existing claims map directly:

| Existing | New ID | Statement |
|----------|--------|-----------|
| claim-1 | **V1** | Zero-config AI provisioning is feasible via mDNS/DNS-SD |
| claim-2 | **V2** | Network-provisioned AI reduces total configuration effort |
| claim-3 | **V3** | Security trade-offs are known and addressable |

The evidence in `moons/claims/claim-{1,2,3}.md` and `moons/claims/evidence-matrix.md` becomes the source material for specific **A** arguments.
