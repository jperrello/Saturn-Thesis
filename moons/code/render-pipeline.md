# Render Pipeline

`evaluation/render.py` — converts aggregated grader reports into publication-ready LaTeX table fragments and PDF figures.

## Input

Reads `evaluation/results/reports/report-*.json` (latest by timestamp, or pass explicit path as argv[1]). The JSON is keyed by grader filename (e.g. `"discovery-latency.ts"`) with each value being the grader's full output object.

## Output

### Tables (`evaluation/tables/*.tex`)

**Existing (4 tables):**

| File | Source grader | Content |
|---|---|---|
| `discovery-latency.tex` | discovery-latency | Percentile table (median, p95, p99, min, max) |
| `config-steps.tex` | step-counter | Per-category step counts (mean/median) |
| `config-artifacts.tex` | artifact-counter | Artifact breakdown (mean per category) |
| `config-success.tex` | success-rate | Success rate, mean duration, N trials |

**Planned (not yet generated):**

| File | Source grader | Content |
|---|---|---|
| `interop-matrix.tex` | interop-matrix | 5x5 pass/fail grid with checkmarks |
| `failover-time.tex` | failover-time | Percentile table (median, p95, min, max) |
| `security-exposure.tex` | exposure-analyzer | Saturn vs static comparison table |
| `security-windows.tex` | exposure-window | Key capture/reuse summary |

### Figures (`evaluation/figures/*.pdf`)

| File | Source grader | Chart type |
|---|---|---|
| `discovery-latency.pdf` | discovery-latency | Box plot of latencies |
| `failover-time.pdf` | failover-time | Box plot of detection + recovery times |
| `config-comparison.pdf` | step-counter | Bar chart of step counts by category |
| `security-comparison.pdf` | exposure-analyzer | Grouped bar: Saturn vs static properties |

## Usage

```bash
python evaluation/render.py                           # latest report
python evaluation/render.py path/to/report.json       # specific report
```

## Design

- matplotlib only, no pandas/seaborn
- Idempotent — re-running overwrites previous output
- Graceful on missing data — skips absent grader keys silently
- Academic style: serif font, no grid lines, muted grayscale-safe palette
- Tables are `\input{}`-able fragments (no `\begin{table}` wrapper — the thesis controls float placement)
