import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from themes_spec import THEMES
import os as _os
REPO = _os.environ.get("KJV_DIR", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "kjv"))
BOOKS = {}
def book(name):
    if name not in BOOKS:
        d = json.load(open(f"{REPO}/{name}.json"))
        BOOKS[name] = {c["chapter"]: {v["verse"]: v["text"] for v in c["verses"]} for c in d["chapters"]}
    return BOOKS[name]
DISPLAY = {"Psalms": "Psalm"}
def pretty(b):
    b = DISPLAY.get(b, b)
    return re.sub(r"^(\d)", r"\1 ", b)
out, problems = [], []
for tid, name, words, refs in THEMES:
    w = words.split()
    dup = {x for x in w if w.count(x) > 1}
    bad = [x for x in w if not re.fullmatch(r"[A-Z]+", x)]
    if dup or bad: problems.append((tid, "words", dup, bad))
    verses = []
    for r in refs:
        m = re.fullmatch(r"(\S+) (\d+):(\d+)(?:-(\d+))?", r)
        b, ch, v1, v2 = m.group(1), m.group(2), int(m.group(3)), int(m.group(4) or m.group(3))
        parts = [book(b)[ch][str(v)] for v in range(v1, v2 + 1)]
        text = " ".join(p.strip() for p in parts)
        text = re.sub(r"\s+", " ", text).strip()
        trimmed = False
        if re.search(r"[,;:]$", text):
            text = text[:-1] + "."; trimmed = True
        if text[0].islower():
            text = text[0].upper() + text[1:]
        ref = f"{pretty(b)} {ch}:{v1}" + (f"–{v2}" if v2 != v1 else "")
        letters = len(re.sub(r"[^A-Za-z]", "", text))
        verses.append({"ref": ref, "text": text, "n": letters, **({"t": 1} if trimmed else {})})
    out.append({"id": tid, "name": name, "words": w, "verses": verses})
for t in out:
    print(f"\n== {t['name']} ({len(t['words'])} words, {len(t['verses'])} verses)")
    for v in t["verses"]:
        print(f"  [{v['n']:3}]{'*' if v.get('t') else ' '} {v['ref']}: {v['text']}")
print("\nPROBLEMS:", problems)
json.dump(out, open(os.path.join(os.path.dirname(__file__), "themes.json"), "w"), ensure_ascii=False, separators=(",", ":"))
