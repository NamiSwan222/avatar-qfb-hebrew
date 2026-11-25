"""Build the Hebrew pack files from translation/he/*.json.

    python tools/build.py [--allow-missing]

Needs work/en (tools/extract.py) and the proxy DLL built by tools/proxy/build.cmd
(work/proxy-target/release/tirgumim_proxy.dll). Writes work/pack/files/, laid out like the game folder:
  Ala/Binaries/Win64/xinput1_3.dll                       launcher-only proxy (inert without -tirgumim_he)
  Ala/Binaries/Win64/tirgumim/he/zzz_tirgumim_he_P.pak    Hebrew string tables + fonts
  Ala/Binaries/Win64/tirgumim/he/redirect.cfg            tells the proxy to show that pak in Content/Paks
Untranslated strings stop the build (unless --allow-missing, for testing: they stay English).
"""
import argparse, os, shutil, subprocess, sys
from common import ROOT, WORK, CSV_DIR, PAK_NAME, english, hebrew, write_csv
import pak, build_fonts

WIN64 = 'Ala/Binaries/Win64'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--allow-missing', action='store_true')
    a = ap.parse_args()
    if not a.allow_missing and subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'coverage.py')]).returncode:
        sys.exit('coverage is not 100%: not building (use --allow-missing for a test build)')
    stage = os.path.join(WORK, 'build', 'pak')
    shutil.rmtree(stage, ignore_errors=True)
    en, he = english(), hebrew()
    for table, rows in en.items():
        write_csv(os.path.join(stage, CSV_DIR, table), ['Key', 'SourceString'],
                  [(k, he[table].get(k) or s) for k, s in rows])
    build_fonts.main(os.path.join(ROOT, 'fonts', 'src'), stage)
    shutil.rmtree(os.path.join(stage, '_work'))
    files = os.path.join(WORK, 'pack', 'files')
    shutil.rmtree(files, ignore_errors=True)
    data = os.path.join(files, WIN64, 'tirgumim', 'he')
    os.makedirs(data)
    pak.build(stage, os.path.join(data, PAK_NAME))
    with open(os.path.join(data, 'redirect.cfg'), 'w', newline='\r\n') as f:
        f.write('root=..\\..\\..\nadd=Ala\\Content\\Paks\\' + PAK_NAME + '\n')
    dll = os.path.join(WORK, 'proxy-target', 'release', 'tirgumim_proxy.dll')
    if not os.path.exists(dll):
        sys.exit(r'build the proxy first: tools\proxy\build.cmd xinput1_3 work\proxy-target')
    shutil.copy(dll, os.path.join(files, WIN64, 'xinput1_3.dll'))
    print('pack files in', files)


if __name__ == '__main__':
    main()
