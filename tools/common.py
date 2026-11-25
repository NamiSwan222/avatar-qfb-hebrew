"""Shared paths and CSV helpers."""
import csv, io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, 'work')
EN_DIR = os.path.join(WORK, 'en')          # the game's English CSVs (extracted, never committed)
HE_DIR = os.path.join(ROOT, 'translation', 'he')
CSV_DIR = 'Ala/Content/Gameplay/Strings/NonAsset'
TABLES = {'Strings_EN.csv': 'strings.json', 'Subtitles_EN.csv': 'subtitles.json'}
PAK_NAME = 'zzz_tirgumim_he_P.pak'
DEFAULT_GAME = r'D:\SteamLibrary\steamapps\common\Avatar The Last Airbender - Quest for Balance'
UNREALPAK = os.environ.get('UNREALPAK', r'D:\UE\UE_5.8\Engine\Binaries\Win64\UnrealPak.exe')


def read_csv(path):
    with io.open(path, encoding='utf-8-sig', newline='') as f:
        rows = list(csv.reader(f))
    return rows[0], [(r[0], r[1]) for r in rows[1:] if r]


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\r\n')
        w.writerow(header)
        w.writerows(rows)


def load_json(path):
    if not os.path.exists(path):
        return {}
    with io.open(path, encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write('\n')


def english():
    """{table csv name: [(key, english)]}"""
    return {t: read_csv(os.path.join(EN_DIR, t))[1] for t in TABLES}


def hebrew():
    return {t: load_json(os.path.join(HE_DIR, j)) for t, j in TABLES.items()}
