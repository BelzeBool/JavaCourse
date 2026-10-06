#!/usr/bin/env python3
"""
Генератор иллюстраций курса (SVG). Единый стиль для всех уроков:
светлая карточка + тёмные «окна IDE» внутри — читается и в светлой, и в тёмной теме IntelliJ.

Запуск: python3 tools/images.py                  — все картинки, светлые и тёмные
        python3 tools/images.py chest assign     — только эти функции
        python3 tools/images.py s01_l03          — только картинки из модуля tools/img/s01_l03*.py

Картинки новых уроков — в отдельных модулях tools/img/<раздел>_<урок>_<имя>.py (по одному на урок),
чтобы уроки можно было рисовать независимо. Шаблон модуля — tools/img/README.md.
Тема задаётся переменной окружения IMG_THEME (light/dark); без неё скрипт сам запускает себя дважды.
"""
import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent

# ---------- палитра и шрифты ----------
# Две темы: светлая карточка для светлой IDE и тёмная для тёмной. Плагин сам покажет x_dark.svg
# вместо x.svg, если IDE в тёмной теме (см. docs/plugin-capabilities.md).
# Смысловые цвета одинаковы во всём курсе: тип — синий, имя — оранжевый, значение — зелёный,
# ошибка — красный, связь с модами — фиолетовый.
THEMES = {
    "light": dict(CARD="#FBFAF6", CARD_LINE="#E2DED3", SURFACE="#FFFFFF", INK="#1E2330", MUTED="#646B7A", FAINT="#A3A9B5",
                  GREEN="#4E8A2A", GREEN_SOFT="#E3F0D6", ORANGE="#C8641B", ORANGE_SOFT="#FBE7D6",
                  BLUE="#2F62C8", BLUE_SOFT="#DCE6FA", RED="#C2303F", RED_SOFT="#FADDE1", PURPLE="#7A45B5"),
    "dark": dict(CARD="#313438", CARD_LINE="#45484E", SURFACE="#26282C", INK="#DFE1E5", MUTED="#A0A4AD", FAINT="#6F737A",
                 GREEN="#7CC45A", GREEN_SOFT="#25361C", ORANGE="#F0A35E", ORANGE_SOFT="#40301F",
                 BLUE="#7AA2F7", BLUE_SOFT="#22304D", RED="#F2737F", RED_SOFT="#45232A", PURPLE="#C29BF0"),
}
THEME = os.environ.get("IMG_THEME", "light")
globals().update(THEMES[THEME])
# «окно IDE» (тёмная тема, как Darcula / New UI Dark)
IDE_BG, IDE_PANEL, IDE_LINE = "#1E1F22", "#2B2D30", "#393B40"
IDE_TEXT, IDE_DIM = "#BCBEC4", "#6F737A"
SYN_KW, SYN_STR, SYN_COM, SYN_NUM, SYN_FN = "#CF8E6D", "#6AAB73", "#7A7E85", "#2AACB8", "#56A8F5"

MONO = "'JetBrains Mono','Cascadia Mono',Consolas,'DejaVu Sans Mono',monospace"
SANS = "'Segoe UI','Inter','Helvetica Neue','DejaVu Sans',Arial,sans-serif"
CW = 0.6  # ширина символа моноширинного шрифта в долях font-size


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{escape(title, {chr(34): "&quot;"})}">\n'
            f'<title>{escape(title)}</title>\n'
            f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="14" fill="{CARD}" stroke="{CARD_LINE}"/>\n'
            f'{body}\n</svg>\n')


def text(x, y, s, size=14, color=INK, weight=400, font=SANS, anchor="start", italic=False, extra=""):
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}" text-anchor="{anchor}"{st} {extra}>{escape(s)}</text>')


def code_line(x, y, tokens, size=14):
    """tokens: список (текст, цвет). Рисует строку моноширинным шрифтом через tspan."""
    parts = "".join(f'<tspan fill="{c}">{escape(t)}</tspan>' for t, c in tokens)
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" xml:space="preserve">'
            f'{parts}</text>')


# подсветка для кода на светлой поверхности карточки (как IntelliJ Light)
LIGHT_SYN = dict(kw="#0033B3", str="#067D17", com="#8C8C8C", num="#1750EB", fn="#00627A", txt="#080808")


def java_tokens(line, on_card=False):
    """Простейшая подсветка Java для иллюстраций.
    on_card=True — код лежит прямо на карточке, а не в тёмном «окне IDE»: в светлой теме берём светлую схему."""
    import re
    if on_card and THEME == "light":
        kw_c, str_c, com_c, num_c, fn_c, txt_c = (LIGHT_SYN[k] for k in ("kw", "str", "com", "num", "fn", "txt"))
    else:
        kw_c, str_c, com_c, num_c, fn_c, txt_c = SYN_KW, SYN_STR, SYN_COM, SYN_NUM, SYN_FN, IDE_TEXT
    out = []
    pat = re.compile(r'(//.*$)|("(?:\\.|[^"\\])*"?)|\b(public|class|static|void|new|return)\b|\b(\d+)\b|(\w+)(?=\()|(.)')
    for m in pat.finditer(line):
        com, s, kw, num, fn, other = m.groups()
        if com:
            out.append((com, com_c))
        elif s:
            out.append((s, str_c))
        elif kw:
            out.append((kw, kw_c))
        elif num:
            out.append((num, num_c))
        elif fn:
            out.append((fn, fn_c))
        else:
            out.append((m.group(0), txt_c))
    return out


def ide_box(x, y, w, h, label=None):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{IDE_BG}" stroke="{IDE_LINE}"/>'
    if label:
        s += f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="10" fill="{IDE_PANEL}"/>'
        s += f'<rect x="{x}" y="{y+18}" width="{w}" height="10" fill="{IDE_PANEL}"/>'
        s += f'<line x1="{x}" y1="{y+28}" x2="{x+w}" y2="{y+28}" stroke="{IDE_LINE}"/>'
        s += text(x + 14, y + 19, label, 12, IDE_TEXT, 500)
    return s


def code_block(x, y, lines, size=14, lh=22, numbers=True, start=1):
    s = ""
    for i, ln in enumerate(lines):
        yy = y + i * lh
        if numbers:
            s += text(x, yy, str(start + i), size - 2, IDE_DIM, font=MONO, anchor="end")
        s += code_line(x + 18, yy, java_tokens(ln), size)
    return s


def badge(x, y, n, color=ORANGE):
    return (f'<circle cx="{x}" cy="{y}" r="12" fill="{color}"/>'
            + text(x, y + 5, str(n), 13, "#FFFFFF", 700, anchor="middle"))


def arrow(x1, y1, x2, y2, color=MUTED, width=1.6, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    a1 = (x2 - 9 * math.cos(ang - 0.45), y2 - 9 * math.sin(ang - 0.45))
    a2 = (x2 - 9 * math.cos(ang + 0.45), y2 - 9 * math.sin(ang + 0.45))
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{d}/>'
            f'<polygon points="{x2},{y2} {a1[0]:.1f},{a1[1]:.1f} {a2[0]:.1f},{a2[1]:.1f}" fill="{color}"/>')


def pixel_art(x, y, rows, px, palette):
    s = ""
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch in palette:
                s += f'<rect x="{x + c*px}" y="{y + r*px}" width="{px}" height="{px}" fill="{palette[ch]}"/>'
    return s


def console(x, y, w, h, rows, cursor_rc, fs=14, title="Консоль"):
    """Окно консоли с текстом и курсором: rows — строки, cursor_rc — (строка, столбец) курсора."""
    s = ide_box(x, y, w, h, title)
    for i, r in enumerate(rows):
        s += text(x + 16, y + 56 + i * 24, r, fs, "#DFE1E5", font=MONO, extra='xml:space="preserve"')
    r, c = cursor_rc
    s += f'<rect x="{x + 16 + c * fs * CW:.1f}" y="{y + 56 + r*24 - fs + 1}" width="{fs*CW:.1f}" height="{fs+3}" fill="#E8A33D"/>'
    return s


def save(path, content):
    if THEME == "dark":
        path = path.with_name(path.stem + "_dark" + path.suffix)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("ok ", path.relative_to(ROOT))


# =====================================================================
# Общие детали: сундук-переменная, табличка, метка типа (уроки про переменные и дальше)
# =====================================================================
WOOD, WOOD_DARK, WOOD_EDGE, LATCH = "#A8722F", "#7A4E1C", "#3B2410", "#D7D7D7"


def chest_px(x, y, s, value=None, value_color=None, old=None):
    """Сундук в духе Minecraft размером s×s. В «окошке» — значение переменной."""
    b = f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="4" fill="{WOOD}" stroke="{WOOD_EDGE}" stroke-width="3"/>'
    lid = s * 0.32
    b += f'<rect x="{x}" y="{y}" width="{s}" height="{lid:.0f}" rx="4" fill="{WOOD_DARK}" stroke="{WOOD_EDGE}" stroke-width="3"/>'
    for k in (1, 2, 3):  # доски
        yy = y + lid + (s - lid) * k / 4
        b += f'<line x1="{x+4}" y1="{yy:.0f}" x2="{x+s-4}" y2="{yy:.0f}" stroke="{WOOD_DARK}" stroke-width="2"/>'
    b += f'<rect x="{x+s/2-7:.0f}" y="{y+lid-8:.0f}" width="14" height="16" fill="{LATCH}" stroke="{WOOD_EDGE}" stroke-width="2"/>'
    if value is not None:
        wx, wy, ww, wh = x + s * 0.18, y + lid + 14, s * 0.64, s - lid - 26
        b += f'<rect x="{wx:.0f}" y="{wy:.0f}" width="{ww:.0f}" height="{wh:.0f}" rx="5" fill="{SURFACE}" stroke="{WOOD_EDGE}" stroke-width="2"/>'
        fs = 30 if len(value) <= 3 else 20
        b += text(x + s / 2, wy + wh / 2 + fs * 0.36, value, fs, value_color or GREEN, 700, font=MONO, anchor="middle")
        if old is not None:
            b += text(wx + 10, wy + 18, old, 13, MUTED, 600, font=MONO)
            b += f'<line x1="{wx+6:.0f}" y1="{wy+13:.0f}" x2="{wx+10+len(old)*13*CW+4:.0f}" y2="{wy+13:.0f}" stroke="{RED}" stroke-width="2"/>'
    return b


def sign_px(cx, y, label, w=None):
    """Табличка с именем переменной над сундуком."""
    w = w or max(96, len(label) * 15 * CW + 28)
    b = f'<rect x="{cx-3}" y="{y+30}" width="6" height="18" fill="{WOOD_DARK}"/>'
    b += f'<rect x="{cx-w/2:.0f}" y="{y}" width="{w:.0f}" height="34" rx="3" fill="#C8A165" stroke="{WOOD_EDGE}" stroke-width="2.5"/>'
    b += text(cx, y + 23, label, 15, "#4A2A08", 700, font=MONO, anchor="middle")
    return b


def type_tag(x, y, label):
    w = len(label) * 13 * CW + 16
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="22" rx="5" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.5"/>'
            + text(x + w / 2, y + 16, label, 13, BLUE, 700, font=MONO, anchor="middle"))


ALL = []  # картинки уроков — в модулях tools/img/*.py


def lesson_modules(only=()):
    """Модули картинок уроков: tools/img/*.py, у каждого список ALL.
    Сломанный модуль чужого урока не мешает рисовать свой: он пропускается с предупреждением."""
    mods = []
    for f in sorted((Path(__file__).resolve().parent / "img").glob("*.py")):
        wanted = not only or any(f.stem.startswith(o) for o in only)
        spec = importlib.util.spec_from_file_location(f"img_{f.stem}", f)
        m = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(m)
        except Exception as e:  # noqa: BLE001 — модуль соседнего урока может быть недописан
            if wanted:
                raise
            print(f"⚠ пропускаю tools/img/{f.name}: {e}", file=sys.stderr)
            continue
        mods.append((f.stem, m))
    return mods


if __name__ == "__main__":
    if "IMG_THEME" not in os.environ:
        for theme in ("light", "dark"):
            subprocess.run([sys.executable, __file__, *sys.argv[1:]], env={**os.environ, "IMG_THEME": theme}, check=True)
        sys.exit(0)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import images as lib  # модули уроков импортируют этот же модуль — палитра одна
    only = set(sys.argv[1:])
    jobs = [("images", fn) for fn in lib.ALL] + [(stem, fn) for stem, m in lesson_modules(only) for fn in m.ALL]
    for stem, fn in jobs:
        if not only or fn.__name__ in only or any(stem.startswith(o) for o in only):
            fn()
