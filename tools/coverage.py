"""Coverage check: every English string needs a Hebrew one with the same markup tokens.

    python tools/coverage.py                 report; exit 1 if anything is missing or broken
    python tools/coverage.py --batch 250     also split what's missing into work/todo/batch-NNN.json

Tokens that must survive translation: {0}, <img id="N">, <red>, </>. Strings that may stay as they
are (numbers, symbols) are listed in translation/keep.json.
"""
import argparse, collections, json, os, re, sys
from common import WORK, ROOT, english, hebrew, load_json, save_json

TOKEN = re.compile(r'\{\d+\}|<img id="\d+">|<red>|</>')
HEB = re.compile(r'[֐-׿]')


def tokens(s):
    return collections.Counter(TOKEN.findall(s))


def check():
    keep = load_json(os.path.join(ROOT, 'translation', 'keep.json'))
    en, he = english(), hebrew()
    missing, broken, total, done = [], [], 0, 0
    for table, rows in en.items():
        for key, src in rows:
            total += 1
            if not src.strip() or src in keep.get('values', []) or key in keep.get('keys', []):
                done += 1
                continue
            t = he[table].get(key)
            if not t:
                missing.append((table, key, src))
            elif tokens(t) != tokens(src):
                broken.append((table, key, src, t, 'tokens'))
            elif not HEB.search(t):
                broken.append((table, key, src, t, 'no Hebrew'))
            else:
                done += 1
    extra = [(t, k) for t, rows in en.items() for k in set(he[t]) - {k for k, _ in rows}]
    return total, done, missing, broken, extra


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--batch', type=int)
    a = ap.parse_args()
    total, done, missing, broken, extra = check()
    for t, k, s, h, why in broken:
        print(f'BROKEN ({why}) {t} {k}\n  en: {s!r}\n  he: {h!r}')
    for t, k in extra:
        print(f'UNUSED key in translation: {t} {k}')
    print(f'coverage: {done}/{total} = {100 * done / total:.2f}%  missing {len(missing)}  broken {len(broken)}')
    if a.batch:
        todo = os.path.join(WORK, 'todo')
        os.makedirs(todo, exist_ok=True)
        for f in os.listdir(todo):
            os.remove(os.path.join(todo, f))
        items = missing + [(t, k, s) for t, k, s, _, _ in broken]
        for i in range(0, len(items), a.batch):
            b = {}
            for t, k, s in items[i:i + a.batch]:
                b.setdefault(t, {})[k] = s
            save_json(os.path.join(todo, f'batch-{i // a.batch:03d}.json'), b)
        print(f'{(len(items) + a.batch - 1) // a.batch} batches in work/todo')
    sys.exit(0 if not missing and not broken else 1)


if __name__ == '__main__':
    main()
