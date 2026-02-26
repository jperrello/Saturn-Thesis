# UCSC Thesis Formatting Requirements

Source: "Dissertation Preperation and Rules.md" (UCSC Graduate Division, Rev 2012)
LaTeX template: `thesis.tex`

## Manuscript Order (exact)

1. Title page — counted as page i, number NOT displayed
2. Copyright page (or blank) — counted as page ii, number NOT displayed
3. Table of Contents — starts at page iii, number displayed
4. List of Figures / Table of Illustrations (if applicable)
5. Abstract
6. Dedication and/or Acknowledgments
7. Text — Arabic numeral 1, all numbers displayed from here on
8. Footnotes (if at end of thesis, not bottom-of-page)
9. Appendices (if applicable)
10. Supplemental files list (if applicable)
11. Bibliography

## Fonts

- Embedded fonts required (PostScript Type 1)
- Any legible font equivalent to 10pt Arial or 12pt Times New Roman
- No script, italic, or ornamental fonts as body text
- Italics OK for non-English words and quotations
- Same font rules apply to captions, footnotes, citations
- Do not mix fonts inappropriately
- Current: 12pt mathptmx (Times New Roman equivalent) ✓

## Spacing

- Double spacing throughout, EXCEPT:
  - Footnotes
  - Indented block quotations
  - Multi-line bibliographic entries (single within, double between)
  - Captions, tables, appendices of data
- Current: `\doublespacing` via setspace ✓

## Margins (all pages including figures/tables)

| Side   | Minimum |
|--------|---------|
| Left   | 1.5"    |
| Right  | 1.25"   |
| Top    | 1.25"   |
| Bottom | 1.25"   |

- No headers allowed
- Current: geometry package matches exactly ✓

## Pagination

- Preliminary pages: lowercase Roman numerals (i, ii, iii...)
  - Title page = i (NOT displayed)
  - Copyright page = ii (NOT displayed)
  - TOC starts at iii (displayed)
- Main text: Arabic numerals starting at 1 (all displayed)
  - Includes footnotes, appendices, bibliography
- All displayed page numbers: centered bottom, >= 0.75" from paper edge
- No punctuation or words around page number: "4" not "-4-" or "Page 4"
- Current: fancyhdr centered footer, footskip=0.5in (places at 0.75" from edge) ✓

## Title Page Format (Master's)

Must reproduce UCSC sample EXACTLY:
```
UNIVERSITY OF CALIFORNIA
SANTA CRUZ

[TITLE IN UPPERCASE]

A thesis submitted in partial satisfaction
of the requirements for the degree of

MASTER OF SCIENCE

in

COMPUTER SCIENCE

by

Joseph Perrello

March 2026

The Thesis of Joseph Perrello
is approved:

______________________________
Adam Smith, Chair

______________________________
Ram Sundara Raman

______________________________
Peter Biehl
Vice Provost and Dean of Graduate Studies
```

- All signature lines (committee + dean) in ONE continuous approval block
- Degree: "MASTER OF SCIENCE" for CS
- Date: month + year matching conferral quarter (Winter = March)
- Electronic copy: unsigned. Signed copy: email to vlarkin@ucsc.edu
- Computer Science degree designation: Master of Science

## Copyright Page

```
Copyright © by
Joseph Perrello
2026
```

Centered vertically on page. Counted as page ii, number NOT displayed.

## Abstract

- Must include: the word "Abstract", thesis title, and author name — all centered at top
- NOT formatted as a chapter heading (no "Chapter" prefix)
- Must state problem, describe methodology, summarize findings
- Double-spaced, within margin requirements
- No word limit for thesis, but ProQuest truncates at 150 words for master's theses in print indexes

## Figures and Tables

- May be embedded in text or full-page
- Full-page items: same margins as text pages
- Landscape orientation OK, but page number stays at portrait bottom (centered, 0.75" from edge)
- Each must be numbered with a caption
- Full-page figure captions: on facing page preceding the figure
  - Caption page is mirror image (1.5" margin on RIGHT side)
  - Caption single-spaced and centered
  - Both pages numbered; TOC lists the figure page number (not caption page)

## Bibliography

- Headed "Bibliography" or "References"
- Alphabetical order by author last name
- Double-spaced between citations
- May be single-spaced within multi-line entries
- Format must be adequate for professionally published CS material
- Current: `plain` BibTeX style (alphabetical, numbered) with bibsep spacing ✓

## Footnotes

Placement is author's choice (discuss with advisors):
- Bottom of page (current approach)
- End of chapter
- End of text before appendices

## Published Material

If including previously published work:
- Must have committee approval
- Acknowledgment page must state reprint info
- Co-author permissions required
- Same margins as rest of thesis (may require reduction)
- Page numbers replaced with thesis sequence
- General abstract covering entire thesis still required

## Submission

- One electronic PDF via ProQuest/UMI
- Department may require separate copy
- Must be registered or on filing fee during conferral quarter
