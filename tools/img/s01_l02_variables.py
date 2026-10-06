"""Картинки урока 1.2 «Переменные и типы». Ширина 480 — под узкую панель задания."""
from images import *  # noqa: F401,F403 — палитра темы и функции рисования

L2 = ROOT / "s01_basics/l02_variables"


def chest():
    # ширина 480: панель задания в IDE узкая, картинка не должна уменьшаться
    w, h = 480, 300
    cx, cy, s = 28, 68, 110
    b = sign_px(cx + s / 2, 20, "diamonds")
    b += chest_px(cx, cy, s, "5")
    b += type_tag(cx - 12, cy + s - 14, "int")
    items = [(BLUE, "Тип: int", "что можно класть: только целые числа"),
             (ORANGE, "Имя: diamonds", "табличка, по ней ищем сундук"),
             (GREEN, "Значение: 5", "что лежит внутри сейчас")]
    for i, (col, t1, t2) in enumerate(items):
        yy = 56 + i * 54
        b += f'<rect x="172" y="{yy-17}" width="6" height="42" rx="3" fill="{col}"/>'
        b += text(188, yy, t1, 15, col, 700)
        b += text(188, yy + 21, t2, 13.5, MUTED)
    y0 = 266
    b += f'<rect x="16" y="{y0-27}" width="448" height="42" rx="10" fill="{SURFACE}" stroke="{CARD_LINE}"/>'
    b += code_line(34, y0, [("int", BLUE), (" ", INK), ("diamonds", ORANGE), (" = ", INK), ("5", GREEN), (";", INK)], 18)
    b += text(448, y0 - 1, "так в коде", 13, MUTED, anchor="end")
    save(L2 / "t01_chest/images/chest.svg",
         svg(w, h, b, "Переменная — сундук с табличкой: тип int, имя diamonds, внутри значение 5"))


def assign():
    w, h = 480, 330
    fs = 20
    cw = fs * CW
    x0 = 240 - 12 * cw / 2
    b = f'<rect x="120" y="16" width="240" height="46" rx="10" fill="{SURFACE}" stroke="{CARD_LINE}"/>'
    b += code_line(x0, 46, [("xp", ORANGE), (" = ", INK), ("xp", ORANGE), (" + ", INK), ("5", GREEN), (";", INK)], fs)
    b += f'<line x1="{x0:.0f}" y1="54" x2="{x0+2*cw:.0f}" y2="54" stroke="{ORANGE}" stroke-width="3"/>'
    b += f'<line x1="{x0+5*cw:.0f}" y1="54" x2="{x0+11*cw:.0f}" y2="54" stroke="{BLUE}" stroke-width="3"/>'
    b += f'<rect x="40" y="78" width="16" height="4" rx="2" fill="{ORANGE}"/>' + text(62, 85, "сюда — результат", 13.5, ORANGE, 600)
    b += f'<rect x="262" y="78" width="16" height="4" rx="2" fill="{BLUE}"/>' + text(284, 85, "считается первым", 13.5, BLUE, 600)
    s, y = 88, 160
    b += sign_px(16 + s / 2, y - 44, "xp", 64) + chest_px(16, y, s, "10")
    b += arrow(110, y + 44, 150, y + 44, ORANGE, 2.2)
    b += badge(130, y + 22, 1)
    b += f'<rect x="156" y="{y+12}" width="168" height="64" rx="10" fill="{SURFACE}" stroke="{CARD_LINE}"/>'
    b += text(240, y + 38, "10 + 5", 19, INK, 700, font=MONO, anchor="middle")
    b += text(240, y + 64, "= 15", 19, GREEN, 700, font=MONO, anchor="middle")
    b += badge(240, y + 2, 2)
    b += arrow(330, y + 44, 370, y + 44, ORANGE, 2.2)
    b += badge(350, y + 22, 3)
    b += sign_px(376 + s / 2, y - 44, "xp", 64) + chest_px(376, y, s, "15")
    for x, t1, t2 in [(60, "1. достать", "из xp: 10"), (240, "2. посчитать", "10 + 5 = 15"), (420, "3. положить", "15 вместо 10")]:
        b += text(x, y + s + 30, t1, 13.5, INK, 700, anchor="middle")
        b += text(x, y + s + 49, t2, 13.5, MUTED, anchor="middle")
    save(L2 / "t08_change/images/assign.svg",
         svg(w, h, b, "xp = xp + 5: достать 10 из сундука, посчитать 15 и положить обратно вместо 10"))


ALL = [chest, assign]
