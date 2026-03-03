# AI Detection Rewrite

## Setup

Read these files first:
- `rewrite_notes.md` — past scores and what worked/didn't
- `detect_results.json` — most recent detection results (if it exists)

Use the notes to understand whether previous rewrites helped, hurt, or had no effect. If the score improved, lean into similar techniques. If it stayed the same or got worse, try something different.

## Run Detection

```bash
python detect.py thesis.pdf
```

This calls the Sapling AI detection API on each chapter. Results go to `detect_results.json`.

**CLI flags:**
- `--no-cache` — force fresh API calls even if content hasn't changed
- `--skip-below 0.3` — skip sections that scored below 0.3 on the previous run and haven't changed

## Read Results

`detect_results.json` has two top-level keys: `meta` and `sections`.

**`meta`** has the run timestamp, average score, and `chars_sent` (how many characters were sent to the API this run — cached sections cost nothing).

**`sections`** is keyed by section name. Each section has:
- `score` — 0–1, lower is better (more human-sounding)
- `chars` — character count sent
- `cached` — if `true`, the score reflects the *previous* text, not the current version. The content hasn't changed since the last run. Treat cached scores as stale if you've made edits since the last run.
- `flagged` — list of sentences scoring above 0.5

Each flagged sentence has:
- `sentence` — the flagged text
- `score` — per-sentence AI probability
- `tex_line` — the line number in `thesis.tex` where this sentence appears. Go directly to this line instead of searching.
- `tex_context` — the flagged line plus one line before and after, so you can write coherent replacements that fit the surrounding text.
- `high_tokens` — specific words the detector flagged as high-probability AI output. Target these words for rephrasing rather than rewriting the entire sentence.

## Rewrite

Open `thesis.tex`. Use `tex_line` to jump directly to flagged sentences. Make sure you are envoking the academic-writing skill.

**Use `high_tokens` to guide rewrites.** These are the specific words the detector thinks are AI-generated. Replace or rephrase these words first — often that's enough to move the score without rewriting the whole sentence.

**Use `tex_context` for coherence.** Read the surrounding lines before editing so your replacement flows naturally with the paragraph.

Prioritize the highest-scoring sections first (check `meta.average` and per-section scores).

Good rewrites:
- Replace vague claims with specific ones (numbers, names, mechanisms)
- Use active voice with a named subject instead of passive
- Cut filler words and unnecessary hedges
- Break formulaic parallel structures
- Ground abstract statements in Saturn's actual behavior or data
- Replace `high_tokens` words with less predictable alternatives

Bad rewrites (don't do these):
- Inserting misspellings or unicode tricks
- Swapping common words for obscure synonyms
- Breaking grammar
- Adding filler to dilute scores
- Changing technical content, claims, or data

Do NOT rewrite sentences that aren't flagged. Do NOT remove citations.

## Log Results

After rewriting, append an entry to `rewrite_notes.md`:

```markdown
## Run N — YYYY-MM-DD

**Average score:** XX% (previous: YY%)

**Per-section scores:**
| Section | Score |
|---|---|
| Introduction | XX% |
| ... | ... |

**What I changed:**
- [section]: description of rewrite and why

**What worked / what to try next time:**
- observation
```

The point of the notes file is simple: the next agent reads it, sees what's been tried, and makes smarter rewrites without repeating failed approaches.

## Do NOT re-run detection

One run per session. Rewrite, log, stop. The next session will run detection again and see if the score improved.
