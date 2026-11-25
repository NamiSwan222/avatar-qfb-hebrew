"""Extract the game's English string tables into work/en (needs UnrealPak from an Unreal Engine install).

    python tools/extract.py [--game "<install folder>"]
"""
import argparse, os, shutil, subprocess, tempfile
from common import DEFAULT_GAME, EN_DIR, CSV_DIR, TABLES, UNREALPAK

ap = argparse.ArgumentParser()
ap.add_argument('--game', default=DEFAULT_GAME)
a = ap.parse_args()
pak = os.path.join(a.game, 'Ala', 'Content', 'Paks', 'pakchunk0-WindowsNoEditor.pak')
tmp = tempfile.mkdtemp()
subprocess.run([UNREALPAK, pak, '-Extract', tmp, '-Filter=*Gameplay/Strings/NonAsset/*_EN.csv'], check=True, capture_output=True)
os.makedirs(EN_DIR, exist_ok=True)
for t in TABLES:
    shutil.copy(os.path.join(tmp, CSV_DIR, t), os.path.join(EN_DIR, t))
    print('extracted', t)
shutil.rmtree(tmp)
