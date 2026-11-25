"""Find English FText literals baked into cooked assets (not from the string tables).

    python tools/scan_assets.py <extracted content folder> [out.json]

An FText with "Base" history is serialized as: namespace FString, key FString (editor keys are
32 hex chars), source FString. We look for the key+source pair. Texts that come from the
string tables (StringTableEntry history) don't match, so what's printed is text the CSVs can't reach.
"""
import json, os, re, struct, sys

KEY = re.compile(rb'\x21\x00\x00\x00([0-9A-F]{32})\x00')


def fstring(d, o):
    if o + 4 > len(d):
        return None, o
    n = struct.unpack_from('<i', d, o)[0]
    if 0 < n < 4000 and o + 4 + n <= len(d) and d[o + 4 + n - 1] == 0:
        return d[o + 4:o + 4 + n - 1].decode('latin-1'), o + 4 + n
    if -4000 < n < 0:
        b = d[o + 4:o + 4 - 2 * n]
        if len(b) == -2 * n:
            return b[:-2].decode('utf-16-le', 'replace'), o + 4 - 2 * n
    return None, o


def scan(root):
    found = {}
    for dp, _, names in os.walk(root):
        for n in names:
            if not n.endswith(('.uexp', '.uasset')):
                continue
            p = os.path.join(dp, n)
            d = open(p, 'rb').read()
            for m in KEY.finditer(d):
                s, _ = fstring(d, m.end())
                if s and re.search(r'[A-Za-z]{2}', s):
                    found.setdefault(os.path.relpath(p, root).replace(os.sep, '/'), []).append([m.group(1).decode(), s])
    return found


if __name__ == '__main__':
    f = scan(sys.argv[1])
    for k, v in sorted(f.items()):
        print(k)
        for key, s in v:
            print('   ', key, repr(s[:100]))
    if len(sys.argv) > 2:
        json.dump(f, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(sum(len(v) for v in f.values()), 'texts in', len(f), 'files')
