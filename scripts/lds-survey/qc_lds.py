"""QC for the LDS survey dashboard. Rerun after every data refresh.

    python scripts/lds-survey/qc_lds.py            # full run, includes live-site regression check
    python scripts/lds-survey/qc_lds.py --offline  # skip the live-site comparison

Checks:
  1. LDS 3.0 headline figures recomputed from the raw Qualtrics export vs. the rendered page.
  2. Name / email / phone scan across the rendered DOM of all three pages.
  3. Analyst-jargon scan across visible text of all three pages.
  4. Ongoing + Final pages: headline KPI numbers identical to the live site.
Exit code 1 if any required check fails.
"""
import functools
import glob
import html
import http.server
import os
import re
import socketserver
import subprocess
import sys
import tempfile
import threading
import zipfile

import openpyxl

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DASH = os.path.join(REPO, "static", "lds-survey-dashboard")
LDS3_SRC_DIR = r"C:\Users\USER\Desktop\NDR Files\LDS survey\LDS 3.0"
LIVE = "https://abijan96.github.io/lds-survey-dashboard/"
PAGES = ["index.html", "final-survey.html", "lds3.html"]

NAMES_FILE = os.path.join(os.path.dirname(__file__), "private_names.txt")  # git-ignored, shared with the build script


def load_name_patterns():
    if not os.path.exists(NAMES_FILE):
        raise SystemExit(f"{NAMES_FILE} is missing; the name scan cannot run without it")
    words = set()
    for line in open(NAMES_FILE, encoding="utf-8"):
        line = line.split("=>")[0].strip()
        if line and not line.startswith("#"):
            words.update(line.split())
    return [rf"\b{re.escape(w)}\b" for w in sorted(words)]


NAME_PATTERNS = load_name_patterns()
EMAIL = r"[\w.+-]+@[\w-]+\.[\w.]+"
PHONE = r"\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b"
JARGON = [r"\bLikert\b", r"\bNPS\b", r"(?i)\bpromoters?\b", r"(?i)\bdetractors?\b", r"\bPassives?\b"]

BROWSERS = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]

results = []


def check(name, ok, detail="", required=True):
    results.append((name, ok, detail, required))
    tag = "PASS" if ok else ("FAIL" if required else "WARN")
    print(f"  [{tag}] {name}" + (f"  ({detail})" if detail else ""))


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve(directory):
    handler = functools.partial(QuietHandler, directory=directory)
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{httpd.server_address[1]}/"


def render(url):
    browser = next((b for b in BROWSERS if os.path.exists(b)), None)
    if not browser:
        raise SystemExit("No Chrome/Edge found for headless rendering")
    with tempfile.TemporaryDirectory() as prof:
        out = subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-first-run",
                              f"--user-data-dir={prof}", "--virtual-time-budget=8000", "--dump-dom", url],
                             capture_output=True, timeout=120)
    return out.stdout.decode("utf-8", "replace")


def visible_text(dom):
    t = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", dom)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def kpis(dom):
    pat = r'<div class="kpi-label">(.*?)</div><div class="kpi-value">(.*?)</div><div class="kpi-subtitle">(.*?)</div>'
    return {html.unescape(l): (html.unescape(v), html.unescape(s)) for l, v, s in re.findall(pat, dom)}


def kpi_values(dom):
    return [html.unescape(v).strip() for v in re.findall(r'class="kpi-value[^"]*"[^>]*>([^<]*)<', dom)]


def rec_score(scores):
    if not scores:
        return 0.0
    return (sum(s >= 9 for s in scores) - sum(s <= 6 for s in scores)) / len(scores) * 100


def lds3_expected():
    files = [f for f in glob.glob(os.path.join(LDS3_SRC_DIR, "*.xlsx")) if not os.path.basename(f).startswith("~$")]
    src = max(files, key=os.path.getmtime)
    ws = openpyxl.load_workbook(src, data_only=True).worksheets[0]
    raw = list(ws.iter_rows(values_only=True))
    idx = {n: i for i, n in enumerate(raw[0])}
    rows = [r for r in raw[2:] if r[idx["Status"]] != "Survey Preview"]

    def nums(col):
        return [float(r[idx[col]]) for r in rows if r[idx[col]] not in (None, "")]

    t, f = nums("Q4_1"), nums("Q5_1")
    comments = sum(1 for r in rows if (r[idx["Q17"]] or "").strip())
    agree = sum(1 for r in rows if r[idx["Q3_1"]] == "Agree")
    depts = {}
    for r in rows:
        d = {"ND Research": "NDR"}.get(r[idx["Q1"]], r[idx["Q1"]])
        depts[d] = depts.get(d, 0) + 1
    return {
        "source": os.path.basename(src),
        "n": len(rows),
        "sessions": len({r[idx["Q2"]] for r in rows}),
        "t_score": rec_score(t), "t_avg": sum(t) / len(t), "t_n": len(t),
        "f_score": rec_score(f), "f_avg": sum(f) / len(f),
        "comments": comments, "comment_rate": comments / len(rows) * 100,
        "agree_pct": agree / len(rows) * 100,
        "depts": depts,
    }


def main():
    offline = "--offline" in sys.argv
    httpd, base = serve(DASH)
    doms = {p: render(base + p) for p in PAGES}
    texts = {p: visible_text(d) for p, d in doms.items()}

    print("\n1. LDS 3.0 headline figures (raw export vs rendered page)")
    exp = lds3_expected()
    print(f"     source: {exp['source']}")
    k = kpis(doms["lds3.html"])
    txt = texts["lds3.html"]
    check("Total participants", k.get("Total Participants", ("",))[0] == str(exp["n"]),
          f"page {k.get('Total Participants', ('?',))[0]} vs source {exp['n']}")
    tk = k.get("Training Recommendation Score", ("?", "?"))
    check("Training recommendation score", tk[0] == f"{exp['t_score']:.1f}", f"page {tk[0]} vs source {exp['t_score']:.1f}")
    check("Training average rating", f"{exp['t_avg']:.1f}/10" in tk[1], f"page '{tk[1]}' vs source {exp['t_avg']:.1f}")
    fk = k.get("Facilitator Recommendation Score", ("?", "?"))
    check("Facilitator recommendation score", fk[0] == f"{exp['f_score']:.1f}", f"page {fk[0]} vs source {exp['f_score']:.1f}")
    check("Facilitator average rating", f"{exp['f_avg']:.1f}/10" in fk[1], f"page '{fk[1]}' vs source {exp['f_avg']:.1f}")
    ck = k.get("Comment Rate", ("?", "?"))
    check("Comment rate", ck[0] == f"{exp['comment_rate']:.0f}%" and ck[1].startswith(f"{exp['comments']} of {exp['n']}"),
          f"page {ck[0]} '{ck[1]}' vs source {exp['comment_rate']:.0f}% ({exp['comments']} of {exp['n']})")
    check("Header response/session count", f"{exp['n']} responses across {exp['sessions']} session" in txt)
    check("Takeaway: content relevance %", f"{exp['agree_pct']:.0f}% of participants fully agreed" in txt)
    check("Takeaway: answered count", f"{exp['t_n']} people answered" in txt)
    for dept, n in exp["depts"].items():
        pct = n / exp["n"] * 100
        check(f"Department participation: {dept}", f"{dept}: {n} ({pct:.1f}%)" in txt)
    check("Subtitle derived from data", "Leadership Development Series 3.0 | September 2026 Evaluation Results" in txt
          or re.search(r"Series 3\.0 \| \w+ \d{4}( to \w+ \d{4})? Evaluation", txt) is not None)
    check("No Invalid Date / NaN / undefined in page", not re.search(r"Invalid Date|\bNaN\b|undefined", txt))

    print("\n2. Name / anonymity scan (rendered DOM, all pages)")
    for p in PAGES:
        hits = []
        for pat in NAME_PATTERNS + [EMAIL, PHONE]:
            hits += re.findall(pat, texts[p])
        check(f"{p}: zero names/emails/phones", not hits,
              f"{len(hits)} hit(s): {sorted(set(hits))}" if hits else "")
        src_hits = [w for pat in NAME_PATTERNS for w in re.findall(pat, doms[p])]
        check(f"{p}: zero names in page source/data", not src_hits,
              f"{len(src_hits)} hit(s)" if src_hits else "")

    for f in sorted(os.listdir(DASH)):
        full = os.path.join(DASH, f)
        if f.endswith(".xlsx"):
            with zipfile.ZipFile(full) as z:
                blob = " ".join(z.read(n).decode("utf-8", "replace") for n in z.namelist() if n.endswith(".xml"))
        elif f.endswith((".csv", ".html", ".md", ".json")):
            blob = open(full, "rb").read().decode("utf-8", "replace")
        else:
            continue
        hits = [w for pat in NAME_PATTERNS for w in re.findall(pat, blob)]
        check(f"published file {f}: zero names", not hits, f"{len(hits)} hit(s)" if hits else "")

    print("\n3. Jargon scan (visible text, all pages)")
    for p in PAGES:
        hits = []
        for pat in JARGON:
            hits += re.findall(pat, texts[p])
        check(f"{p}: no analyst jargon", not hits,
              f"{len(hits)} hit(s): {sorted(set(hits))}" if hits else "")
        check(f"{p}: no Invalid Date / NaN / undefined", not re.search(r"Invalid Date|\bNaN\b|undefined", texts[p]))

    if not offline:
        print("\n4. Regression: headline numbers on Ongoing + Final pages unchanged vs live")
        for p in ["index.html", "final-survey.html"]:
            live, local = kpi_values(render(LIVE + p)), kpi_values(doms[p])
            check(f"{p}: KPI values match live", bool(local) and local == live, f"{local}" if local == live else f"local {local} vs live {live}")

    httpd.shutdown()
    failed = [r for r in results if not r[1] and r[3]]
    warned = [r for r in results if not r[1] and not r[3]]
    print(f"\nRESULT: {'PASS' if not failed else 'FAIL'}  "
          f"({sum(r[1] for r in results)} passed, {len(failed)} failed, {len(warned)} warnings)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
