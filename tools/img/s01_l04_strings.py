"""Картинки урока 1.4 «Строки»."""
from xml.sax.saxutils import escape

from images import *  # палитра текущей темы и функции рисования: svg, text, code_line, arrow, badge…

L = ROOT / "s01_basics/l04_strings"


def _cell(x, y, w, h, ch, fill, stroke, size, color, dash=False):
    d = ' stroke-dasharray="5 4"' if dash else ""
    b = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}" stroke="{stroke}" stroke-width="2"{d}/>'
    if ch:
        b += text(x + w / 2, y + h / 2 + size * 0.36, ch, size, color, 700, font=MONO, anchor="middle")
    return b


def _mono(x, y, tokens, size):
    """Строка кода моноширинным шрифтом с точной длиной (textLength): пропуски и подсветка под ними
    совпадают, даже если у ученика другой моноширинный шрифт (Consolas уже, чем JetBrains Mono)."""
    n = sum(len(t) for t, _ in tokens)
    parts = "".join(f'<tspan fill="{c}">{escape(t)}</tspan>' for t, c in tokens)
    return (f'<text x="{x:.1f}" y="{y}" font-family="{MONO}" font-size="{size}" xml:space="preserve" '
            f'textLength="{n * size * CW:.1f}" lengthAdjust="spacingAndGlyphs">{parts}</text>')


def _bracket(x1, x2, y, color):
    """Скобка под клетками: от x1 до x2, с засечками вверх."""
    return (f'<path d="M{x1},{y-7} L{x1},{y} L{x2},{y} L{x2},{y-7}" fill="none" stroke="{color}" stroke-width="2"/>'
            f'<line x1="{(x1+x2)/2}" y1="{y}" x2="{(x1+x2)/2}" y2="{y+6}" stroke="{color}" stroke-width="2"/>')


def cells():
    """t03: строка Creeper как ряд клеток с номерами; клетки 7 нет."""
    w, h = 480, 262
    b = f'<rect x="16" y="14" width="448" height="40" rx="10" fill="{SURFACE}" stroke="{CARD_LINE}"/>'
    b += code_line(32, 40, [("String", BLUE), (" ", INK), ("mob", ORANGE), (" = ", INK),
                            ('"Creeper"', GREEN), (";", INK)], 16)
    s, gap, x0, y = 44, 6, 43, 114
    word = "Creeper"
    cx = [x0 + i * (s + gap) + s / 2 for i in range(len(word) + 1)]
    for i, ch in enumerate(word):
        hot = i in (0, len(word) - 1)
        b += _cell(x0 + i * (s + gap), y, s, s, ch, ORANGE_SOFT if hot else SURFACE,
                   ORANGE if hot else MUTED, 24, GREEN)
        b += text(cx[i], y + s + 22, str(i), 14, MUTED, 600, font=MONO, anchor="middle")
    # клетки 7 нет
    b += _cell(x0 + 7 * (s + gap), y, s, s, "", "none", RED, 24, RED, dash=True)
    b += text(cx[7], y + s + 22, "7", 14, RED, 700, font=MONO, anchor="middle")
    # подписи сверху
    for i in (0, 6):
        b += text(cx[i], 84, f"charAt({i})", 13.5, ORANGE, 700, font=MONO, anchor="middle")
        b += arrow(cx[i], 90, cx[i], y - 4, ORANGE, 2)
    # длина
    right = x0 + 6 * (s + gap) + s
    b += _bracket(x0, right, y + s + 34, INK)
    b += text((x0 + right) / 2, y + s + 60, "length() = 7, номера от 0 до 6", 14, INK, 600, anchor="middle")
    b += text(464, 248, "charAt(7) — клетки нет, программа упадёт", 13.5, RED, 600, anchor="end")
    save(L / "t03_cells/images/cells.svg",
         svg(w, h, b, "Строка Creeper — семь клеток с номерами от 0 до 6. "
                      "charAt(0) — буква C, charAt(6) — буква r, клетки с номером 7 нет"))


def substring_img():
    """t05: minecraft:stone по клеткам; indexOf находит двоеточие, substring вырезает куски."""
    w, h = 480, 236
    word = "minecraft:stone"
    cw, ch_h, x0, y = 28, 36, 30, 72
    colon = word.index(":")
    for i, ch in enumerate(word):
        if i == colon:
            fill, stroke = ORANGE_SOFT, ORANGE
        else:
            fill, stroke = GREEN_SOFT, CARD_LINE
        b_cell = f'<rect x="{x0 + i*cw}" y="{y}" width="{cw}" height="{ch_h}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
        b_cell += text(x0 + i * cw + cw / 2, y + 25, ch, 18, ORANGE if i == colon else GREEN, 700, font=MONO, anchor="middle")
        b_cell += text(x0 + i * cw + cw / 2, y + ch_h + 18, str(i), 13.5, ORANGE if i == colon else MUTED,
                       700 if i == colon else 400, font=MONO, anchor="middle")
        if i == 0:
            b = b_cell
        else:
            b += b_cell
    ccx = x0 + colon * cw + cw / 2
    b += text(ccx, 38, 'indexOf(":") → 9', 14, ORANGE, 700, font=MONO, anchor="middle")
    b += arrow(ccx, 44, ccx, y - 4, ORANGE, 2)
    # первый кусок: клетки 0–8
    by = y + ch_h + 34
    l1, r1 = x0 + 2, x0 + colon * cw - 2
    b += _bracket(l1, r1, by, INK)
    b += text((l1 + r1) / 2, by + 26, "substring(0, 9)", 14, INK, 600, font=MONO, anchor="middle")
    b += text((l1 + r1) / 2, by + 48, '"minecraft"', 16, GREEN, 700, font=MONO, anchor="middle")
    b += text((l1 + r1) / 2, by + 70, "клетка 9 не входит", 13.5, MUTED, anchor="middle")
    # второй кусок: клетки 10–14
    l2, r2 = x0 + (colon + 1) * cw + 2, x0 + len(word) * cw - 2
    b += _bracket(l2, r2, by, INK)
    b += text((l2 + r2) / 2, by + 26, "substring(10)", 14, INK, 600, font=MONO, anchor="middle")
    b += text((l2 + r2) / 2, by + 48, '"stone"', 16, GREEN, 700, font=MONO, anchor="middle")
    b += text((l2 + r2) / 2, by + 70, "до конца строки", 13.5, MUTED, anchor="middle")
    save(L / "t05_substring/images/substring.svg",
         svg(w, h, b, "Строка minecraft:stone по клеткам 0–14. Двоеточие в клетке 9. "
                      "substring(0, 9) — клетки 0–8, это minecraft. substring(10) — клетки 10–14, это stone"))


def format_img():
    """t11: значения встают в пропуски шаблона по порядку."""
    w, h = 480, 236
    tpl = '"Игрок %s, уровень %d, здоровье %.1f"'
    fs = 15
    cw = fs * CW
    x0 = (w - len(tpl) * cw) / 2
    holes = [("%s", "name", '"Steve"'), ("%d", "level", "30"), ("%.1f", "health", "17.5")]
    b = f'<rect x="16" y="16" width="448" height="46" rx="10" fill="{SURFACE}" stroke="{CARD_LINE}"/>'
    centers = []
    pos = 0
    for hole, _, _ in holes:
        i = tpl.index(hole, pos)
        pos = i + len(hole)
        hx = x0 + i * cw
        b += f'<rect x="{hx - 2:.1f}" y="27" width="{len(hole) * cw + 4:.1f}" height="25" rx="4" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.5"/>'
        centers.append(hx + len(hole) * cw / 2)
    b += _mono(x0, 45, java_tokens(tpl, on_card=True), fs)
    bw, by = 100, 112
    for k, ((hole, name, value), c) in enumerate(zip(holes, centers)):
        bx = c - bw / 2
        b += f'<rect x="{bx:.1f}" y="{by}" width="{bw}" height="54" rx="8" fill="{SURFACE}" stroke="{CARD_LINE}"/>'
        b += text(c, by + 21, name, 13.5, ORANGE, 700, font=MONO, anchor="middle")
        b += text(c, by + 43, value, 16, GREEN, 700, font=MONO, anchor="middle")
        b += arrow(c, by - 4, c, 66, ORANGE, 2)
        b += badge(c + 16, 89, k + 1)
    b += text(240, 196, "значения встают в пропуски по порядку:", 13.5, MUTED, anchor="middle")
    parts = [("Игрок ", INK), ("Steve", GREEN), (", уровень ", INK), ("30", GREEN),
             (", здоровье ", INK), ("17.5", GREEN)]
    total = sum(len(t) for t, _ in parts)
    b += _mono((w - total * 14 * CW) / 2, 220, parts, 14)
    save(L / "t11_format/images/format.svg",
         svg(w, h, b, "Шаблон с тремя пропусками %s, %d и %.1f; значения name, level и health "
                      "встают в них по порядку"))


ALL = [cells, substring_img, format_img]
