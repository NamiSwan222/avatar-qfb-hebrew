"""Merge translated batch files into translation/he/*.json.

    python tools/merge.py work/done/batch-000.json [...]
Each file: {"Strings_EN.csv": {key: hebrew}, "Subtitles_EN.csv": {...}}
"""
import os, sys
from common import HE_DIR, TABLES, load_json, save_json

for path in sys.argv[1:]:
    b = load_json(path)
    for table, items in b.items():
        out = os.path.join(HE_DIR, TABLES[table])
        cur = load_json(out)
        cur.update({k: v for k, v in items.items() if v})
        save_json(out, dict(sorted(cur.items())))
    print('merged', path)
