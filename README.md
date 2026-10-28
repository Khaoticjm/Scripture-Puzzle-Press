<p align="center"><img src="assets/logo.svg" width="96" alt="Scripture Puzzle Press logo"></p>

# Scripture Puzzle Press

A SPHINX Global Enterprises product. Scripture Puzzle Press builds print-ready Bible puzzle books for Amazon KDP. It runs entirely in the browser as one HTML file, with no server and no install.

## What it makes

- **Five puzzle types:** word searches, crosswords with King James verse clues, word scrambles, verse cryptograms and verse fill-ins.
- **25 themes**, including an *Africa in the Bible* collection: Cush & Ethiopia, Egypt in Scripture, the Queen of Sheba, Hagar & the God Who Sees, and Africa in the Early Church.
- **A complete KDP interior:**
  - title page, copyright page and contents
  - answer key packed in measured columns, starting on a right-hand page
  - even page count with a 24-page minimum
  - mirrored margins for the binding edge
- **A full-wrap paperback cover** sized from the page count using KDP's spine formula: 0.002252 in per page for white paper, 0.0025 in for cream, and 0.125 in bleed. On-screen guides show trim, bleed, safe zone, spine folds and the barcode area.
- **Trim sizes and layout options:** 8.5 × 11 in or 6 × 9 in, a large-print mode, three difficulty levels, and Kemetic or Classic page ornaments.
- **Edition numbers:** the same edition number and settings always reproduce the same book.

Every verse and crossword clue is copied from the King James Version text, never typed by hand.

## The Stretch Forth series

The app ships with one-click presets for the series, named for Psalm 68:31 ("Ethiopia shall soon stretch out her hands unto God"). Each volume uses five themes, and the five volumes together use all 25 themes once.

| Volume | Title | Themes |
|---|---|---|
| Vol. 1 | Cush & Ethiopia | Cush & Ethiopia, Creation, Noah, Psalms, The Prophets |
| Vol. 2 | Out of Egypt | Egypt in Scripture, The Patriarchs, The Exodus, Daniel, The Nativity |
| Vol. 3 | The Queen of Sheba | The Queen of Sheba, Proverbs & Wisdom, David & Goliath, Life of Jesus, Animals |
| Vol. 4 | Hagar & the God Who Sees | Hagar, Women of the Bible, The Twelve, Fruit of the Spirit, The Parables |
| Vol. 5 | Simon of Cyrene | Africa in the Early Church, Miracles, The Resurrection, Paul's Journeys, Armour of God |
| Special Edition | From Cush to Calvary | All 25 themes |

At 3 sets per theme, each volume has 75 puzzles and runs 92–106 pages, which is enough for spine text. The series name and volume print on the title page, copyright page, front cover, spine and back-cover description.

## Use it

Open `index.html` in Chrome or Edge, or enable GitHub Pages on this repo (Settings → Pages → deploy from `main`, root folder).

1. Choose themes, puzzle types, difficulty, trim and print size.
2. Check the **Page proofs**. The "KDP ready" badge confirms the page-count rules are met.
3. Click **Print / Save as PDF** for the interior, with margins set to **None**.
4. Switch to **Cover** and click **Download cover PDF**. It builds the full-colour cover at 300 dpi and the exact KDP size without the print dialog. **Print cover / Save as PDF** remains as a fallback (turn on Background graphics).

5. Open **KDP listing** for the book's title, subtitle, series, volume number and description, each with a copy button. The description matches the volume and its real puzzle count. The series description for KDP's series page is there too.

Upload the cover only after the interior is final: any change to the page count changes the spine width.

## Project layout

```
index.html          The app (generated; this is what users open)
assets/logo.svg     Scripture Puzzle Press mark
src/template.html   App source: markup, styles and generator code
src/themes_spec.py  Theme word lists and verse references
src/build_data.py   Pulls verse text from the KJV dataset by reference
src/build_clues.py  Builds crossword clues from KJV verses (word blanked out)
src/themes.json     Generated verse and clue data
src/assemble.py     Injects the data into the template and writes index.html
```

## Rebuild

Python 3 is required. The KJV text comes from [aruljohn/Bible-kjv](https://github.com/aruljohn/Bible-kjv) (MIT licence). It is used only at build time and is not stored in this repo.

```bash
git clone --depth 1 https://github.com/aruljohn/Bible-kjv kjv   # or set KJV_DIR
python3 src/build_data.py     # verses -> src/themes.json
python3 src/build_clues.py    # crossword clues -> src/themes.json (about a minute)
python3 src/assemble.py       # -> index.html
```

To add a theme, append it to `THEMES` in `src/themes_spec.py`. Add preferred clue books for it to `PREF` in `src/build_clues.py`, then run the three steps above.

## Notes

- Scripture quotations are from the King James Version, which is in the public domain.
- Where a verse ends mid-sentence, its closing comma, semicolon or colon becomes a period.
- Word-search filler letters, scrambles and cipher alphabets are checked against a blocklist, so no offensive word appears by accident.

© SPHINX Global Enterprises Corp.
