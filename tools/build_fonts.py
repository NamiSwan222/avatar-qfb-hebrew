"""Build the replacement fonts (Latin + Hebrew, all SIL OFL) for the game's font slots.

    python tools/build_fonts.py fonts/src <out folder>

Writes <out>/<game path>.ufont for every slot in SLOTS. A cooked .ufont is the raw TTF, so each
slot just gets our TTF. Body fonts: Noto Sans + Noto Sans Hebrew merged at the slot's weight.
Title fonts (Cinzel, Herculanum): David Libre.
"""
import io, os, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.merge import Merger

F = 'Ala/Content/Art/UXD/Fonts/'
SLOTS = {
    F + 'Signika/Signika-Light.ufont': ('noto', 300),
    F + 'Signika/Signika-Regular.ufont': ('noto', 400),
    F + 'Signika/Signika-Medium.ufont': ('noto', 500),
    F + 'Signika/Signika-SemiBold.ufont': ('noto', 600),
    F + 'Signika/Signika-Bold.ufont': ('noto', 700),
    F + 'NotoSans/NotoSans-Regular.ufont': ('noto', 400),
    'Ala/Content/Art/UXD/Blueprints/Utils/Rajdhani-SemiBold.ufont': ('noto', 600),
    F + 'Cinzel/Cinzel-Regular.ufont': ('david', 'Medium'),
    F + 'Cinzel/Cinzel-Bold.ufont': ('david', 'Bold'),
    F + 'Cinzel/Cinzel-Black.ufont': ('david', 'Bold'),
    F + 'Herculanum/HerculanumLTPro.ufont': ('david', 'Medium'),
    F + 'Herculanum/HerculanumLTPro-Bold.ufont': ('david', 'Bold'),
    'Engine/Content/EngineFonts/Faces/RobotoRegular.ufont': ('noto', 400),
    'Engine/Content/EngineFonts/Faces/RobotoLight.ufont': ('noto', 300),
    'Engine/Content/EngineFonts/Faces/RobotoBold.ufont': ('noto', 700),
}


def static(path, wght, tmp):
    f = TTFont(path)
    axes = {a.axisTag: a.defaultValue for a in f['fvar'].axes}
    axes['wght'] = wght
    inst = instancer.instantiateVariableFont(f, axes)
    inst.save(tmp)
    return tmp


def noto(src, wght, work):
    a = static(os.path.join(src, 'notosans__NotoSans.ttf'), wght, os.path.join(work, f'latin{wght}.ttf'))
    h = static(os.path.join(src, 'notosanshebrew__NotoSansHebrew.ttf'), wght, os.path.join(work, f'heb{wght}.ttf'))
    for p in (a, h):  # the merger needs matching tables; drop the ones that differ and aren't needed
        t = TTFont(p)
        for tag in ('STAT', 'MVAR', 'HVAR', 'meta', 'DSIG'):
            if tag in t:
                del t[tag]
        t.save(p)
    m = Merger().merge([a, h])
    name = m['name']
    for rec in name.names:
        if rec.nameID in (1, 3, 4, 6, 16):
            rec.string = f'Tirgumim Noto {wght}' if rec.nameID != 6 else f'TirgumimNoto-{wght}'
    out = os.path.join(work, f'noto{wght}.ttf')
    m.save(out)
    return out


def main(src, out):
    work = os.path.join(out, '_work')
    os.makedirs(work, exist_ok=True)
    built = {}
    for slot, (kind, arg) in SLOTS.items():
        key = (kind, arg)
        if key not in built:
            built[key] = noto(src, arg, work) if kind == 'noto' else os.path.join(src, f'davidlibre__DavidLibre-{arg}.ttf')
        dst = os.path.join(out, slot)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(built[key], 'rb') as f, open(dst, 'wb') as g:
            g.write(f.read())
        print(slot, '<-', os.path.basename(built[key]))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
