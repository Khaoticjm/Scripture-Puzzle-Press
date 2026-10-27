import json, os, re
here = os.path.dirname(os.path.abspath(__file__))
themes = json.load(open(os.path.join(here, "themes.json")))
for t in themes:
    for v in t["verses"]:
        v.pop("t", None)
tpl = open(os.path.join(here, "template.html")).read()
page = tpl.replace("__THEMES__", json.dumps(themes, ensure_ascii=False, separators=(",", ":")))
root = os.path.dirname(here)
os.makedirs(os.path.join(root, "build"), exist_ok=True)
open(os.path.join(root, "build", "artifact.html"), "w").write(page)
head = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
standalone = head + page.replace('<div class="app"', '</head><body>\n<div class="app"', 1) + "\n</body></html>\n"
open(os.path.join(root, "index.html"), "w").write(standalone)
js = re.findall(r"<script>(.*?)</script>", page, re.S)[0]
open(os.path.join(root, "build", "check.js"), "w").write(js)
print("built index.html", len(standalone), "bytes")
