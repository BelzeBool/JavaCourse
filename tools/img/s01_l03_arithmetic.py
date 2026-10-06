"""Картинки урока 1.3 «Арифметика»."""
from images import *  # noqa: F401,F403 — палитра текущей темы и функции рисования

L = ROOT / "s01_basics/l03_arithmetic"

# булыжник 8×8: светлый, средний и тёмный серый
COBBLE = ["abbacbba", "bccabacb", "abbcbaab", "cabbacbb", "bacbbaca", "abcabbcb", "bbacbabc", "cabbcbab"]
COBBLE_PAL = {"a": "#ABABAB", "b": "#8C8C8C", "c": "#686868"}


def slot(x, y, s, count):
    """Слот инвентаря в стиле Minecraft с блоком булыжника и числом в правом нижнем углу."""
    b = f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="#8B8B8B" stroke="#373737" stroke-width="3"/>'
    b += pixel_art(x + 12, y + 10, COBBLE, 6, COBBLE_PAL)
    b += text(x + s - 5, y + s - 5, count, 18, "#3F3F3F", 700, anchor="end")
    b += text(x + s - 7, y + s - 7, count, 18, "#FFFFFF", 700, anchor="end")
    return b


def bracket(x1, x2, y, color):
    return (f'<path d="M{x1},{y-8} L{x1},{y} L{x2},{y} L{x2},{y-8}" fill="none" stroke="{color}" stroke-width="2.2"/>'
            f'<line x1="{(x1+x2)/2}" y1="{y}" x2="{(x1+x2)/2}" y2="{y+6}" stroke="{color}" stroke-width="2.2"/>')


def stacks():
    w, h = 480, 270
    b = text(240, 36, "150 блоков булыжника", 16, INK, 700, anchor="middle")
    s = 72
    xs = [104, 184, 304]
    for x, n in zip(xs, ["64", "64", "22"]):
        b += slot(x, 54, s, n)
    # полные стаки
    b += bracket(xs[0], xs[1] + s, 146, BLUE)
    cx = (xs[0] + xs[1] + s) / 2
    b += text(cx, 176, "2 полных стака", 14, BLUE, 700, anchor="middle")
    fs = 15
    toks = [("150", INK), (" / ", BLUE), ("64", INK), (" = ", MUTED), ("2", GREEN)]
    b += code_line(cx - len("150 / 64 = 2") * fs * CW / 2, 202, toks, fs)
    # остаток
    b += bracket(xs[2], xs[2] + s, 146, ORANGE)
    cx2 = xs[2] + s / 2
    b += text(cx2, 176, "остаток", 14, ORANGE, 700, anchor="middle")
    toks = [("150", INK), (" % ", ORANGE), ("64", INK), (" = ", MUTED), ("22", GREEN)]
    b += code_line(cx2 - len("150 % 64 = 22") * fs * CW / 2, 202, toks, fs)
    # проверка
    b += f'<line x1="40" y1="224" x2="440" y2="224" stroke="{CARD_LINE}"/>'
    b += text(240, 251, "Проверка: 2 стака по 64 и ещё 22 — снова 150", 14, MUTED, anchor="middle")
    save(L / "t01_mul_div/images/stacks.svg",
         svg(w, h, b, "150 блоков: два полных стака по 64 и ещё 22 блока. 150 / 64 = 2, 150 % 64 = 22"))


def expr_box(x, y, w, tokens, border=None):
    fs = 14.5
    n = sum(len(t) for t, _ in tokens)
    stroke = border or CARD_LINE
    sw = 2 if border else 1
    b = f'<rect x="{x}" y="{y}" width="{w}" height="36" rx="8" fill="{SURFACE}" stroke="{stroke}" stroke-width="{sw}"/>'
    b += code_line(x + (w - n * fs * CW) / 2, y + 23, tokens, fs)
    return b


def order():
    w, h = 480, 300
    S = LIGHT_SYN["str"] if THEME == "light" else SYN_STR

    def tk(*parts):
        # строка в кавычках — цветом строк, числа — цветом значений, знаки — обычным текстом
        out = []
        for p in parts:
            if p.startswith('"'):
                out.append((p, S))
            elif p.strip().isdigit():
                out.append((p, GREEN))
            else:
                out.append((p, INK))
        return out

    cols = [
        (16, "Без скобок", "слева направо", RED,
         [tk('"Стаков: "', " + ", "2", " + ", "3"), tk('"Стаков: 2"', " + ", "3"), tk('"Стаков: 23"')],
         ["приклеили 2", "приклеили 3"]),
        (248, "Со скобками", "сначала скобки", GREEN,
         [tk('"Стаков: "', " + (", "2", " + ", "3", ")"), tk('"Стаков: "', " + ", "5"), tk('"Стаков: 5"')],
         ["2 + 3 = 5", "приклеили 5"]),
    ]
    cw = 216
    b = ""
    for x, title, sub, col, rows, notes in cols:
        b += text(x + cw / 2, 34, title, 16, col, 700, anchor="middle")
        b += text(x + cw / 2, 55, sub, 14, MUTED, anchor="middle")
        ys = [72, 154, 236]
        for i, (y, toks) in enumerate(zip(ys, rows)):
            b += expr_box(x, y, cw, toks, col if i == 2 else None)
        for y, note in zip(ys[:2], notes):
            b += arrow(x + 34, y + 42, x + 34, y + 76, MUTED, 2)
            b += text(x + 48, y + 64, note, 14, INK)
    b += f'<line x1="240" y1="20" x2="240" y2="280" stroke="{CARD_LINE}"/>'
    save(L / "t03_order/images/order.svg",
         svg(w, h, b, "Без скобок Java клеит слева направо и получает «Стаков: 23». "
                      "Со скобками сначала считает 2 + 3 = 5 и получает «Стаков: 5»"))


def spawn():
    w, h = 480, 312
    # сетка карты
    b = ""
    for gx in range(20, 301, 20):
        b += f'<line x1="{gx}" y1="20" x2="{gx}" y2="260" stroke="{CARD_LINE}" stroke-width="1"/>'
    for gy in range(20, 261, 20):
        b += f'<line x1="20" y1="{gy}" x2="300" y2="{gy}" stroke="{CARD_LINE}" stroke-width="1"/>'
    # масштаб: 1 блок = 1.1 px; спавн (10, 30), Стив (−150, 210): по X 160 блоков, по Z 180
    sx, sy = 276, 44
    px, py = sx - 176, sy + 198
    # катеты и гипотенуза
    b += f'<line x1="{px}" y1="{py}" x2="{sx}" y2="{py}" stroke="{BLUE}" stroke-width="3"/>'
    b += f'<line x1="{sx}" y1="{py}" x2="{sx}" y2="{sy}" stroke="{ORANGE}" stroke-width="3"/>'
    b += f'<line x1="{px}" y1="{py}" x2="{sx}" y2="{sy}" stroke="{GREEN}" stroke-width="3" stroke-dasharray="7 5"/>'
    b += f'<rect x="{sx-12}" y="{py-12}" width="12" height="12" fill="none" stroke="{MUTED}" stroke-width="1.5"/>'
    b += f'<rect x="{(px+sx)/2-24}" y="{py-28}" width="48" height="20" rx="4" fill="{CARD}"/>'
    b += text((px + sx) / 2, py - 13, "по X", 14, BLUE, 700, anchor="middle")
    b += f'<rect x="{sx-50}" y="{(py+sy)/2-10}" width="42" height="20" rx="4" fill="{CARD}"/>'
    b += text(sx - 10, (py + sy) / 2 + 5, "по Z", 14, ORANGE, 700, anchor="end")
    b += f'<rect x="{(px+sx)/2-112}" y="{(py+sy)/2-22}" width="84" height="20" rx="4" fill="{CARD}"/>'
    b += text((px + sx) / 2 - 30, (py + sy) / 2 - 7, "по прямой", 14, GREEN, 700, anchor="end")
    # точки
    b += f'<circle cx="{sx}" cy="{sy}" r="9" fill="{GREEN}" stroke="{SURFACE}" stroke-width="2"/>'
    b += f'<circle cx="{px}" cy="{py}" r="9" fill="{ORANGE}" stroke="{SURFACE}" stroke-width="2"/>'
    # подписи
    b += text(sx + 18, sy - 2, "Спавн", 15, INK, 700)
    b += text(sx + 18, sy + 19, "X = 10, Z = 30", 14, MUTED, font=MONO)
    b += text(px, py + 40, "Стив", 15, INK, 700, anchor="middle")
    b += text(px, py + 60, "X = −150, Z = 210", 14, MUTED, font=MONO, anchor="middle")
    # оси
    b += arrow(330, 150, 384, 150, INK, 1.8)
    b += text(392, 155, "X: восток", 14, INK)
    b += arrow(330, 150, 330, 204, INK, 1.8)
    b += text(342, 202, "Z: юг", 14, INK)
    save(L / "t10_spawn/images/spawn.svg",
         svg(w, h, b, "Карта сверху: спавн в X = 10, Z = 30, Стив в X = −150, Z = 210. "
                      "Путь по X, путь по Z и прямая линия между ними — треугольник"))


def overflow():
    w, h = 480, 250
    b = text(240, 34, "Какие числа помещаются в int", 16, INK, 700, anchor="middle")
    y = 140
    x1, x2 = 40, 420
    b += f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{BLUE}" stroke-width="4"/>'
    for x in (x1, 230, x2):
        b += f'<line x1="{x}" y1="{y-9}" x2="{x}" y2="{y+9}" stroke="{BLUE}" stroke-width="3"/>'
    b += text(x1 - 6, y + 32, "−2 147 483 648", 14, INK, 600, font=MONO)
    b += text(230, y + 32, "0", 14, INK, 600, font=MONO, anchor="middle")
    b += text(x2 + 6, y + 32, "2 147 483 647", 14, INK, 600, font=MONO, anchor="end")
    # за правым краем — не помещается
    b += f'<line x1="{x2}" y1="{y}" x2="460" y2="{y}" stroke="{RED}" stroke-width="3" stroke-dasharray="5 4"/>'
    # дуга «+1»: с правого края на левый
    b += (f'<path d="M{x2},{y-14} C{x2},{y-86} {x1},{y-86} {x1},{y-18}" fill="none" '
          f'stroke="{ORANGE}" stroke-width="2.4"/>')
    b += f'<polygon points="{x1},{y-12} {x1-6},{y-24} {x1+6},{y-24}" fill="{ORANGE}"/>'
    b += text(230, y - 34, "ещё +1 — и число на другом краю", 14, ORANGE, 700, anchor="middle")
    b += text(240, y + 72, "Результат больше края не помещается и «перескакивает»", 14, MUTED, anchor="middle")
    b += text(240, y + 92, "на другой конец: 2 400 000 000 превращается в −1 894 967 296", 14, MUTED, anchor="middle")
    save(L / "t11_overflow/images/overflow.svg",
         svg(w, h, b, "Числовая прямая int от −2 147 483 648 до 2 147 483 647. "
                      "Шаг за правый край приводит на левый: так появляется отрицательное число"))


ALL = [stacks, order, spawn, overflow]
