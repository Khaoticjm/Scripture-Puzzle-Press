"""Crossword clues: for each theme word, find short KJV passages containing it (theme books first), blank the word."""
import json, re, os, sys
here = os.path.dirname(os.path.abspath(__file__))
import os as _os
REPO = _os.environ.get("KJV_DIR", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "kjv"))
DISPLAY = {"Psalms": "Psalm", "SongofSolomon": "Song of Solomon"}
def pretty(b): return re.sub(r"^(\d)", r"\1 ", DISPLAY.get(b, b))

PREF = {
 "creation": [("Genesis", range(1, 4)), ("Psalms", None), ("Job", range(38, 40))],
 "noah": [("Genesis", range(5, 11))],
 "exodus": [("Exodus", None), ("Numbers", None)],
 "women": [("Ruth", None), ("Esther", None), ("Genesis", None), ("Judges", range(4, 6)), ("1Samuel", None), ("2Samuel", None), ("Luke", None), ("Acts", None), ("Proverbs", range(31, 32)), ("Romans", range(16, 17)), ("2Timothy", None)],
 "psalms": [("Psalms", None)],
 "christmas": [("Matthew", range(1, 3)), ("Luke", range(1, 3)), ("Isaiah", range(7, 10))],
 "jesus": [("Matthew", None), ("Mark", None), ("Luke", None), ("John", None)],
 "disciples": [("Matthew", None), ("Mark", None), ("Luke", None), ("John", None), ("Acts", range(1, 3))],
 "spirit": [("Galatians", None), ("John", range(14, 17)), ("1Corinthians", range(12, 14)), ("Ephesians", None), ("Colossians", None), ("Romans", None), ("1Peter", None), ("2Peter", None)],
 "patriarchs": [("Genesis", range(11, 51))],
 "david": [("1Samuel", None), ("2Samuel", None), ("Psalms", None)],
 "prophets": [("1Kings", range(17, 23)), ("2Kings", None), ("Isaiah", None), ("Jeremiah", None), ("Ezekiel", None), ("Jonah", None), ("Hosea", None), ("Joel", None), ("Amos", None), ("Obadiah", None), ("Micah", None), ("Nahum", None), ("Habakkuk", None), ("Zephaniah", None), ("Haggai", None), ("Zechariah", None), ("Malachi", None), ("2Samuel", None)],
 "daniel": [("Daniel", None)],
 "wisdom": [("Proverbs", None), ("Ecclesiastes", None), ("James", None), ("1Kings", range(3, 5))],
 "parables": [("Matthew", None), ("Luke", None), ("Mark", None)],
 "miracles": [("Matthew", None), ("Mark", None), ("Luke", None), ("John", None)],
 "easter": [("Matthew", range(21, 29)), ("Mark", range(11, 17)), ("Luke", range(19, 25)), ("John", range(12, 21)), ("1Corinthians", range(15, 16)), ("Job", range(19, 20))],
 "paul": [("Acts", None), ("Romans", None), ("1Corinthians", None), ("2Corinthians", None), ("Galatians", None), ("Philippians", None), ("2Timothy", None)],
 "armor": [("Ephesians", None), ("1Thessalonians", None), ("2Timothy", None), ("Romans", None), ("2Corinthians", None), ("1Peter", None), ("James", None), ("Joshua", None)],
 "cush": [("Acts", range(8, 9)), ("Jeremiah", range(38, 40)), ("Numbers", range(12, 13)), ("Genesis", range(2, 11)), ("Isaiah", None), ("Psalms", None), ("Zephaniah", None), ("Job", range(28, 29)), ("2Kings", range(19, 20)), ("2Chronicles", range(14, 15)), ("Esther", range(1, 2)), ("Song of Solomon", None)],
 "egypt": [("Genesis", range(37, 51)), ("Exodus", range(1, 15)), ("Isaiah", range(19, 20)), ("Matthew", range(2, 3)), ("Acts", range(7, 8)), ("Hosea", None), ("Ezekiel", None), ("Jeremiah", None)],
 "sheba": [("1Kings", range(10, 11)), ("2Chronicles", range(9, 10)), ("Matthew", range(12, 13)), ("Luke", range(11, 12)), ("1Kings", None)],
 "hagar": [("Genesis", range(16, 18)), ("Genesis", range(21, 22)), ("Genesis", range(25, 26)), ("Galatians", range(4, 5)), ("Genesis", None)],
 "church": [("Mark", range(15, 16)), ("Luke", range(23, 24)), ("Acts", None), ("Romans", range(16, 17)), ("1Corinthians", None)],
 "animals": [("Genesis", None), ("Job", None), ("Leviticus", None), ("Psalms", None), ("Proverbs", None), ("Isaiah", None), ("Deuteronomy", None), ("Matthew", None), ("Jonah", None), ("Numbers", None)],
}

verses = []  # (book, ch, v, text)
for f in sorted(os.listdir(REPO)):
    if not f.endswith(".json") or f == "Books.json": continue
    d = json.load(open(f"{REPO}/{f}"))
    b = f[:-5]
    for c in d["chapters"]:
        for v in c["verses"]:
            verses.append((b, int(c["chapter"]), int(v["verse"]), re.sub(r"\s+", " ", v["text"]).strip()))

def segment(text, word):
    """Shortest natural clause around the word, blanked; marks cut ends with an ellipsis."""
    pat = re.compile(r"\b" + word + r"\b", re.I)
    parts = re.split(r"(?<=[;:.?!])\s+", text)
    idx = next((i for i, p in enumerate(parts) if pat.search(p)), None)
    if idx is None: return None
    a, b = idx, idx
    seg = lambda: " ".join(parts[a:b + 1])
    while len(seg()) < 34 and (a > 0 or b < len(parts) - 1):
        if b < len(parts) - 1: b += 1
        else: a -= 1
    s = seg()
    if len(s) > 125: return None
    lead = a > 0
    tail = b < len(parts) - 1
    s = s.strip()
    if re.search(r"[;:,]$", s): s = s[:-1]; tail = True
    if s and s[0].islower(): lead = True
    if tail and re.search(r"[.?!]$", s): tail = False
    s = pat.sub("{}", s)
    if "{}" not in s: return None
    # avoid clues that are mostly blanks or reveal the word in another form
    if re.search(word[:max(4, len(word) - 1)], s, re.I): return None
    return ("…" if lead else "") + s + ("…" if tail else "")

def in_pref(tid, b, ch):
    for i, (book, chs) in enumerate(PREF[tid]):
        if b == book and (chs is None or ch in chs): return i
    return None

themes = json.load(open(os.path.join(here, "themes.json")))
total = missing = 0
report = []
for t in themes:
    clues = {}
    for w in t["words"]:
        total += 1
        pat = re.compile(r"\b" + w + r"\b", re.I)
        cands = []
        for (b, ch, v, text) in verses:
            if not pat.search(text): continue
            s = segment(text, w)
            if not s: continue
            pref = in_pref(t["id"], b, ch)
            ref = f"{pretty(b)} {ch}:{v}"
            if any(ref == tv["ref"] for tv in t["verses"]): pref = -1
            score = (0 if pref is not None else 1, pref if pref is not None else 99, abs(len(s) - 65) // 15)
            cands.append((score, ref, s))
        cands.sort()
        if cands and cands[0][0][0] == 1:
            # only general-Bible matches: keep them only if short and the word is fairly distinctive
            cands = [c for c in cands if len(c[2]) <= 100][:2]
        else:
            seen=set(); pick=[]
            for c in cands:
                if c[0][0] != 0 or c[1] in seen: continue
                seen.add(c[1]); pick.append(c)
                if len(pick) == 5: break
            cands = pick
        if cands:
            clues[w] = [[c[1], c[2]] for c in cands]
        else:
            missing += 1
    t["clues"] = clues
    report.append((t["name"], len(clues), [w for w in t["words"] if w not in clues]))
json.dump(themes, open(os.path.join(here, "themes.json"), "w"), ensure_ascii=False, separators=(",", ":"))
for name, n, miss in report:
    print(f"{name:22} {n:2} clued; no clue: {' '.join(miss)}")
print("total", total, "missing", missing)
# samples
for t in themes[:20:4]:
    for w in list(t["clues"])[:4]:
        print(f"  {w:12} {t['clues'][w][0][1]}  ({t['clues'][w][0][0]})")
