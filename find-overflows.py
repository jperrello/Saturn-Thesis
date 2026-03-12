#!/usr/bin/env python3
"""Parse thesis.log for overfull hbox warnings and show the source lines."""

import re
import sys
from pathlib import Path

LOG = Path("thesis.log")
if not LOG.exists():
    print("thesis.log not found — compile first with pdflatex thesis.tex")
    sys.exit(1)

log = LOG.read_text(errors="replace")
lines = log.splitlines()

# Track which file is "active" by following ( and ) in the log
file_stack = []
current_file = "thesis.tex"

results = []

i = 0
while i < len(lines):
    line = lines[i]

    # Track file opens/closes to know which .tex file we're in
    for ch in line:
        if ch == '(':
            # look ahead for filename
            rest = line[line.index('(', line.index(ch)):] if ch in line else ""
            break

    # Simpler approach: look for file entry patterns
    for m in re.finditer(r'\((\./[^\s()]+\.tex)', line):
        current_file = m.group(1)

    # Detect overfull hbox
    m = re.match(r'Overfull \\hbox \(([0-9.]+)pt too wide\) in paragraph at lines (\d+)--(\d+)', line)
    if m:
        overflow_pt = float(m.group(1))
        line_start = int(m.group(2))
        line_end = int(m.group(3))

        # Grab the next 1-2 lines which show the offending content
        context = []
        for j in range(i + 1, min(i + 3, len(lines))):
            if lines[j].strip() and not lines[j].startswith('Overfull') and not lines[j].startswith('['):
                context.append(lines[j].strip())
            else:
                break

        results.append({
            "file": current_file,
            "lines": f"{line_start}--{line_end}",
            "overflow": overflow_pt,
            "context": " ".join(context),
        })

    i += 1

# Group by file
from collections import defaultdict
by_file = defaultdict(list)
for r in results:
    by_file[r["file"]].append(r)

# Severity coloring
def severity(pt):
    if pt > 20:
        return "🔴"
    if pt > 5:
        return "🟡"
    return "🟢"

total = len(results)
print(f"\n{'='*70}")
print(f"  OVERFULL HBOX REPORT — {total} warnings found")
print(f"{'='*70}\n")

for f in sorted(by_file.keys()):
    items = by_file[f]
    print(f"📄 {f} ({len(items)} warnings)")
    print(f"  {'─'*60}")
    for r in sorted(items, key=lambda x: -x["overflow"]):
        # Clean up the font encoding noise from the context
        clean = re.sub(r'\\OT1/[a-z/]+/\d+(\.\d+)?\s*', '', r["context"])
        clean = re.sub(r'\[\]', '', clean)
        clean = clean.strip()
        # Truncate long lines
        if len(clean) > 80:
            clean = clean[:77] + "..."

        print(f"  {severity(r['overflow'])} Line {r['lines']:>10s}  ({r['overflow']:6.1f}pt over)")
        if clean:
            print(f"     └─ {clean}")
    print()

# Summary
severe = sum(1 for r in results if r["overflow"] > 20)
moderate = sum(1 for r in results if 5 < r["overflow"] <= 20)
minor = sum(1 for r in results if r["overflow"] <= 5)
print(f"Summary: 🔴 {severe} severe (>20pt)  🟡 {moderate} moderate (5-20pt)  🟢 {minor} minor (<5pt)")
print(f"\nTo fix: wrap long code in \\mbox{{}} or use \\allowbreak, add \\- for hyphenation hints,")
print(f"or use \\texttt{{\\small ...}} for inline code that overflows.")
