# Runs each thesis section through Sapling's AI-detection API.
# Workflow: PDF -> pdftotext -> split by chapter regex -> cache check -> API call
#   -> flag sentences scoring >50% AI -> fuzzy-match back to thesis.tex lines
#   -> print summary + write detect_results.json

import subprocess, json, sys, os, re, urllib.request, hashlib, argparse
from datetime import datetime, timezone

API = "https://api.sapling.ai/api/v1/aidetect"
API_VERSION = "20251027"
CACHE_FILE = "detect_cache.json"

# Regex patterns to locate each section in the pdftotext output.
# Used by chunk() to split the full text into per-section bodies.
# Bibliography acts as a stop marker — everything after it is dropped.
SECTIONS = [
    ("Abstract", r"Abstract\s*\n"),
    ("Acknowledgments", r"Acknowledgments?\s*\n"),
    ("Introduction", r"Chapter\s+1\s*\n\s*Introduction"),
    ("Background", r"Chapter\s+2\s*\n\s*Background"),
    ("Design", r"Chapter\s+3\s*\n\s*Design"),
    ("Implementation", r"Chapter\s+4\s*\n\s*Implementation"),
    ("Evaluation", r"Chapter\s+5\s*\n\s*Evaluation"),
    ("Discussion", r"Chapter\s+6\s*\n\s*Discussion"),
    ("Conclusion", r"Chapter\s+7\s*\n\s*Conclusion"),
    ("Appendix A", r"Appendix\s+A\b"),
    ("Appendix B", r"Appendix\s+B\b"),
    ("Appendix C", r"Appendix\s+C\b"),
    ("Appendix D", r"Appendix\s+D\b"),
    ("Bibliography", r"Bibliography\s*\n"),
]

# Matches pseudocode lines (indented code, keywords, ASCII box-drawing).
# Used in strip_noise() to remove non-prose content that skews AI scores.
PSEUDOCODE_RE = re.compile(
    r"^(\s{4,}.*|.*\b(PROCEDURE|IF|THEN|ELSE|WHILE|FOR|RETURN|END)\b.*|[+\-|=]{3,}.*)$",
    re.MULTILINE,
)
PAGE_NUM_RE = re.compile(r"^\d+$", re.MULTILINE)


# Read API key from SAPLING_API_KEY env var, falling back to .env file
def key() -> str:
    k = os.environ.get("SAPLING_API_KEY", "")
    if k:
        return k
    env = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env):
        for line in open(env):
            line = line.strip()
            if line.startswith("SAPLING_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


# Convert PDF to plain text via poppler's pdftotext
def extract(pdf: str) -> str:
    r = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True)
    if r.returncode != 0:
        print("pdftotext failed — install poppler: brew install poppler")
        sys.exit(1)
    return r.stdout


def strip_preamble(text: str) -> str:
    # drop everything before Abstract (title page, copyright, TOC, LoF, LoT)
    m = re.search(r"Abstract\s*\n", text, re.IGNORECASE)
    if m:
        return text[m.start():]
    return text


# Remove pseudocode blocks and bare page numbers that would skew AI scores
def strip_noise(text: str) -> str:
    text = PSEUDOCODE_RE.sub("", text)
    text = PAGE_NUM_RE.sub("", text)
    return text


# Split extracted text into (section_name, body) pairs.
# Finds the LAST match of each SECTIONS regex (handles TOC duplicates),
# sorts by position, then slices between consecutive boundaries.
# Drops Bibliography and everything after it. Strips pseudocode from Appendix A.
# Skips sections <100 chars. Caps each body at 200k chars (API limit).
def chunk(text: str) -> list[tuple[str, str]]:
    text = strip_preamble(text)

    # find last occurrence of each section header (skips TOC entries)
    starts = []
    for name, pat in SECTIONS:
        last = None
        for last in re.finditer(pat, text, re.IGNORECASE):
            pass
        if last:
            starts.append((name, last.start()))
    starts.sort(key=lambda x: x[1])

    chunks = []
    for i, (name, pos) in enumerate(starts):
        if name == "Bibliography":
            break
        end = starts[i + 1][1] if i + 1 < len(starts) else len(text)
        body = text[pos:end].strip()
        if name == "Appendix A":
            body = strip_noise(body)
        if len(body) > 100:
            chunks.append((name, body[:200000]))
    return chunks


# POST text to Sapling AI detection API. Returns raw JSON response with
# overall score, per-sentence scores, and per-token probabilities.
def detect(text: str, api_key: str) -> dict | None:
    req = urllib.request.Request(API, method="POST")
    req.add_header("Content-Type", "application/json")
    payload = json.dumps({
        "key": api_key,
        "text": text,
        "sent_scores": True,
        "score_string": True,
        "version": API_VERSION,
    }).encode()
    try:
        with urllib.request.urlopen(req, payload) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  API error: {e}")
        return None


# --- LaTeX line mapping ---
# These functions fuzzy-match flagged sentences from the PDF back to thesis.tex
# line numbers, bridging the gap between pdftotext output and source LaTeX.

# Normalize text for fuzzy comparison: strip LaTeX commands (\textbf{...} -> ...),
# fix PDF ligatures (fi/fl), collapse whitespace, lowercase.
def normalize(text: str) -> str:
    t = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", text)  # \cmd{content} -> content
    t = re.sub(r"\\[a-zA-Z]+", "", t)  # bare \commands
    t = re.sub(r"[{}~]", " ", t)
    t = t.replace("fi", "fi").replace("fl", "fl")  # PDF ligatures
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t


# Find which thesis.tex line a flagged sentence came from.
# Takes the first 8 normalized words as a search needle, scans all tex lines.
# Falls back to progressively shorter windows (6, 5, 4 words) if no match.
# Returns (1-indexed line number, surrounding context lines) or (None, None).
def find_tex_line(sentence: str, tex_lines: list[str], tex_norm: list[str]) -> tuple[int | None, list[str] | None]:
    words = normalize(sentence).split()
    if len(words) < 3:
        return None, None
    window = words[:min(8, len(words))]
    needle = " ".join(window)

    for i, norm in enumerate(tex_norm):
        if needle in norm:
            start = max(0, i - 1)
            end = min(len(tex_lines), i + 2)
            return i + 1, [tex_lines[j] for j in range(start, end)]

    for width in [6, 5, 4]:
        if len(words) < width:
            continue
        needle = " ".join(words[:width])
        for i, norm in enumerate(tex_norm):
            if needle in norm:
                start = max(0, i - 1)
                end = min(len(tex_lines), i + 2)
                return i + 1, [tex_lines[j] for j in range(start, end)]

    return None, None


# Zip the API's parallel token/probability arrays into (token, prob) pairs.
# These identify which specific words the model thinks are AI-generated.
def extract_high_tokens(result: dict) -> list[tuple[str, float]] | dict:
    tokens = result.get("tokens", [])
    probs = result.get("token_probs", [])
    if not tokens or not probs or len(tokens) != len(probs):
        return {}
    return list(zip(tokens, probs))


# Given a flagged sentence, find which high-probability tokens (>=0.8) appear in it.
# Returns up to 10 sorted tokens — the specific words driving the AI score.
def high_tokens_for_sentence(sentence: str, token_prob_pairs: list[tuple[str, float]], threshold: float = 0.8) -> list[str]:
    words = set()
    if not token_prob_pairs:
        return []
    norm_sent = normalize(sentence)
    for token, prob in token_prob_pairs:
        if prob < threshold:
            continue
        clean = token.strip()
        if len(clean) < 3:
            continue
        if normalize(clean) in norm_sent:
            words.add(clean)
    return sorted(words)[:10]


# Filter out false-positive "sentences" that aren't real prose:
# bare numbers, single capitalized words, chapter headers, URLs,
# short fragments (<15 chars), citation page ranges, years.
def is_noise(txt: str) -> bool:
    if re.fullmatch(r"[\d.]+", txt):
        return True
    if re.fullmatch(r"[A-Z][a-z]+", txt):
        return True
    if re.fullmatch(r"Chapter\s+\d+", txt, re.IGNORECASE):
        return True
    if re.fullmatch(r"https?://\S+", txt):
        return True
    if len(txt) < 15:
        return True
    if re.search(r"pages?\s+\d+[–-]\d+", txt):
        return True
    if re.fullmatch(r"\d{4}\.", txt):
        return True
    return False


# --- Caching ---
# SHA-256 hash of each section body is stored alongside results in detect_cache.json.
# On subsequent runs, unchanged sections skip the API call entirely.

def load_cache() -> dict:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            return json.load(f)
    return {}


def save_cache(cache: dict) -> None:
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def hash_body(body: str) -> str:
    return hashlib.sha256(body.encode()).hexdigest()


# Orchestrates the full pipeline: extract PDF -> chunk -> cache/detect -> flag -> report.
# Flags: --no-cache forces fresh API calls, --skip-below N skips sections under N%.
def main() -> None:
    parser = argparse.ArgumentParser(description="AI detection for thesis sections")
    parser.add_argument("pdf", nargs="?", default="thesis.pdf")
    parser.add_argument("--no-cache", action="store_true", help="Force fresh API calls")
    parser.add_argument("--skip-below", type=float, default=0,
                        help="Skip sections scoring below threshold on previous run (if content unchanged)")
    args = parser.parse_args()

    api_key = key()
    if not api_key:
        print("Set SAPLING_API_KEY in .env or env var")
        sys.exit(1)

    # load thesis.tex for line mapping
    tex_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thesis.tex")
    tex_lines = []
    tex_norm = []
    if os.path.exists(tex_path):
        with open(tex_path) as f:
            tex_lines = [l.rstrip("\n") for l in f.readlines()]
        tex_norm = [normalize(l) for l in tex_lines]

    text = extract(args.pdf)
    chunks = chunk(text)

    if not chunks:
        print("No sections found — sending full text")
        chunks = [("Full Text", text[:200000])]

    cache = {} if args.no_cache else load_cache()
    total_chars = 0
    sections = {}

    for name, body in chunks:
        h = hash_body(body)
        cached = False

        # skip-below: if content unchanged and previous score below threshold
        if args.skip_below > 0 and name in cache and cache[name].get("hash") == h:
            prev = cache[name].get("score", 1.0)
            if prev < args.skip_below:
                print(f"\n--- {name} (skipped, previous score {prev*100:.1f}% < {args.skip_below*100:.0f}%) ---")
                sections[name] = cache[name].get("result", {"score": prev, "chars": len(body), "cached": True, "flagged": []})
                continue

        # check cache
        if not args.no_cache and name in cache and cache[name].get("hash") == h:
            print(f"\n--- {name} ({len(body)} chars, cached) ---")
            result_data = cache[name].get("result", {})
            print(f"  Score: {result_data.get('score', 0)*100:.1f}% (cached)")
            sections[name] = result_data
            sections[name]["cached"] = True
            continue

        print(f"\n--- {name} ({len(body)} chars) ---")
        total_chars += len(body)
        result = detect(body, api_key)
        if not result:
            continue

        s = result.get("score", -1)
        print(f"  Score: {s*100:.1f}% ({'AI' if s > 0.5 else 'Human'})")

        token_pairs = extract_high_tokens(result)

        flagged = []
        for sent in result.get("sentence_scores", []):
            txt = sent["sentence"].strip()
            if sent["score"] <= 0.5:
                continue
            if is_noise(txt):
                continue
            tex_line, tex_context = find_tex_line(txt, tex_lines, tex_norm)
            htokens = high_tokens_for_sentence(txt, token_pairs)
            entry = {
                "sentence": txt,
                "score": round(sent["score"], 3),
            }
            if tex_line:
                entry["tex_line"] = tex_line
            if tex_context:
                entry["tex_context"] = tex_context
            if htokens:
                entry["high_tokens"] = htokens
            flagged.append(entry)

        section_result = {
            "score": round(s, 4),
            "chars": len(body),
            "cached": False,
            "flagged": flagged,
        }

        # store score_string if returned
        if result.get("score_string"):
            section_result["score_string"] = result["score_string"]

        sections[name] = section_result

        # update cache
        cache[name] = {"hash": h, "score": s, "result": section_result}

    save_cache(cache)

    # summary
    print("\n========== SUMMARY ==========")
    scores = []
    for name in sections:
        s = sections[name].get("score", 0)
        cached = sections[name].get("cached", False)
        tag = " (cached)" if cached else ""
        print(f"  {name:20s} {s*100:5.1f}%{tag}")
        scores.append(s)

    avg = sum(scores) / len(scores) if scores else 0
    print(f"  {'AVERAGE':20s} {avg*100:5.1f}%")
    print(f"  Chars sent this run: {total_chars:,}")

    total_flagged = sum(len(sec.get("flagged", [])) for sec in sections.values())
    if total_flagged:
        print(f"\n  Flagged sentences: {total_flagged}")

    out = {
        "meta": {
            "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "pdf": args.pdf,
            "api_version": API_VERSION,
            "average": round(avg, 4),
            "chars_sent": total_chars,
        },
        "sections": sections,
    }
    with open("detect_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to detect_results.json")


if __name__ == "__main__":
    main()
