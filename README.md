# Avatar: The Last Airbender – Quest for Balance: Hebrew translation (fan project)

A full Hebrew translation of **Avatar: The Last Airbender – Quest for Balance** (Steam app 1620030): all quest and
NPC dialogue, menus, HUD, tutorials, help, item and skill descriptions, challenge names, and the cutscene
subtitles. About 4,900 strings / 44,000 English words, translated by us (no fan translation existed).

Unofficial fan project, for personal use. Not affiliated with Paramount, Nickelodeon, GameMill or Bamtang.
This repository holds only our tools, our Hebrew text and OFL fonts. No game files, no English text.

## How it works

- The game reads all its text from two CSV string tables inside `pakchunk0`:
  `Ala/Content/Gameplay/Strings/NonAsset/Strings_EN.csv` and `Subtitles_EN.csv` (key, text).
- We build a small extra pak, `zzz_tirgumim_he_P.pak` (`tools/pak.py`, uncompressed, pak format 3), with
  Hebrew versions of those two CSVs plus replacement fonts. Unreal mounts `_P` paks above the game's own,
  so our files win.
- Fonts: a cooked `.ufont` is the raw TTF. Every Latin font slot the game uses (Signika, Cinzel, Herculanum,
  Rajdhani, Noto Sans, Roboto) gets a font with Hebrew + Latin: Noto Sans + Noto Sans Hebrew merged at the
  slot's weight, or David Libre for the title fonts (`tools/build_fonts.py`, sources and licences in
  `fonts/src`, all SIL OFL 1.1).
- Right-to-left: Unreal 4.27 lays out Hebrew right-to-left by itself (ICU bidi), so the text is stored in
  normal logical order.

### Hebrew only from the launcher

Nothing in the game folder is replaced, and our pak is **not** in `Content\Paks`:

- `Ala\Binaries\Win64\xinput1_3.dll` is a proxy (source: `tools/proxy`, Rust). The game imports
  `XINPUT1_3.dll`, so Windows loads this one; every XInput call is forwarded to the real System32 DLL.
- It does nothing unless the game was started with `-tirgumim_he` (or `TIRGUMIM_LANG=he`). The Tirgumim
  launcher starts it through Steam with that argument (the game restarts itself through Steam, which drops
  environment variables).
- With the flag it reads `Ala\Binaries\Win64\tirgumim\he\redirect.cfg` and hooks the game's file calls so that
  `Content\Paks` *appears* to contain `zzz_tirgumim_he_P.pak` (directory listing, attributes and open are
  redirected to `tirgumim\he\`). Nothing is written to the game folder, so after a crash a Steam launch is
  still English.

## Build

Needs Python 3.11+ with `fonttools`, Rust + Visual Studio Build Tools, and (only to extract the English) an
Unreal Engine install for `UnrealPak.exe` (`UNREALPAK` env var, default UE 5.8).

```
python tools/extract.py --game "<install folder>"     # English CSVs -> work/en (not committed)
python tools/coverage.py                                # must say 100%
tools\proxy\build.cmd xinput1_3 %CD%\work\proxy-target
python tools/build.py                                   # -> work/pack/files
npm run make-pack -- <this repo>/pack/pack.config.json --game-dir "<install>" --out out/avatar-qfb-he-<ver>.zip   (in the launcher repo)
```

## Translating

- `translation/he/strings.json` and `subtitles.json`: `{key: Hebrew}`, logical order.
- `glossary.md`: names, places, bending terms, UI terms, token rules.
- `python tools/coverage.py --batch 250` lists what's missing or has broken tokens (`{0}`, `<img id="N">`,
  `<red>`…`</>`) and writes batches to `work/todo/`; `tools/merge.py` merges translated batches back.
- `tools/scan_assets.py` lists English text baked into assets instead of the string tables (mostly editor
  placeholders that the game replaces at runtime).

## Testing helpers

`tools/shot.ps1` (screenshot a game window even when covered), `tools/key.ps1` (send keys to it), and the proxy
logs to `%TEMP%\tirgumim_proxy.log` when started with `-tirgumim_debug`.
