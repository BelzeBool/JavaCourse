#!/usr/bin/env python3
"""
Генератор иллюстраций курса (SVG). Единый стиль для всех уроков:
светлая карточка + тёмные «окна IDE» внутри — читается и в светлой, и в тёмной теме IntelliJ.

Запуск: python3 tools/images.py   (из корня курса)
"""
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
L1 = ROOT / "s01_basics/l01_first_program"
L0 = ROOT / "s00_start/l01_how"

# ---------- палитра и шрифты ----------
CARD, CARD_LINE = "#FBFAF6", "#E2DED3"
INK, MUTED, FAINT = "#1E2330", "#646B7A", "#A3A9B5"
GREEN, GREEN_SOFT = "#4E8A2A", "#E3F0D6"
ORANGE, ORANGE_SOFT = "#C8641B", "#FBE7D6"
BLUE, BLUE_SOFT = "#2F62C8", "#DCE6FA"
RED, RED_SOFT = "#C2303F", "#FADDE1"
PURPLE = "#7A45B5"
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


def java_tokens(line):
    """Простейшая подсветка Java для иллюстраций."""
    import re
    out = []
    pat = re.compile(r'(//.*$)|("(?:\\.|[^"\\])*"?)|\b(public|class|static|void|new|return)\b|\b(\d+)\b|(\w+)(?=\()|(.)')
    for m in pat.finditer(line):
        com, s, kw, num, fn, other = m.groups()
        if com:
            out.append((com, SYN_COM))
        elif s:
            out.append((s, SYN_STR))
        elif kw:
            out.append((kw, SYN_KW))
        elif num:
            out.append((num, SYN_NUM))
        elif fn:
            out.append((fn, SYN_FN))
        else:
            out.append((m.group(0), IDE_TEXT))
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


def save(path, content):
    path.write_text(content, encoding="utf-8")
    print("ok ", path.relative_to(ROOT))


# =====================================================================
# 0.1 Добро пожаловать
# =====================================================================
def roadmap():
    w, h = 680, 210
    b = text(24, 36, "Путь курса", 16, INK, 700)
    b += text(656, 36, "мод-чекпоинты — зелёные", 12, MUTED, anchor="end")
    steps = [("1", "Основы", "языка", False), ("2", "ООП", "классы", False), ("3", "Первый", "мод", True),
             ("4", "Коллекции", "+ мод", True), ("5", "Лямбды", "+ мод", True), ("6", "Свой мод", "финал", True)]
    x0, gap, size, y = 34, 106, 64, 70
    b += f'<line x1="{x0+size/2}" y1="{y+size/2}" x2="{x0+5*gap+size/2}" y2="{y+size/2}" stroke="{CARD_LINE}" stroke-width="6" stroke-linecap="round"/>'
    for i, (n, t1, t2, mod) in enumerate(steps):
        x = x0 + i * gap
        top, side = (GREEN, "#3B6D1F") if mod else ("#8A8F9C", "#6B707C")
        # «блок» в духе Майнкрафта: верхняя грань светлее
        b += f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="8" fill="{side}"/>'
        b += f'<rect x="{x}" y="{y}" width="{size}" height="{size-10}" rx="8" fill="{top}"/>'
        b += text(x + size/2, y + 36, n, 24, "#FFFFFF", 700, anchor="middle")
        b += text(x + size/2, y + size + 24, t1, 14, INK, 600, anchor="middle")
        b += text(x + size/2, y + size + 42, t2, 12, GREEN if mod else MUTED, anchor="middle")
    # «ты здесь»
    b += f'<path d="M{x0+size/2-7},{y-10} l7,8 l7,-8 z" fill="{ORANGE}"/>'
    b += text(x0 + size/2, y - 16, "ты здесь", 12, ORANGE, 700, anchor="middle")
    save(L0 / "t01_welcome/images/roadmap.svg", svg(w, h, b, "Путь курса: основы, ООП, первый мод, коллекции, лямбды, свой мод"))


def ide_layout():
    w, h = 680, 390
    X, Y, W, H = 20, 20, 640, 350
    b = f'<rect x="{X}" y="{Y}" width="{W}" height="{H}" rx="12" fill="{IDE_BG}" stroke="{IDE_LINE}"/>'
    # заголовок окна
    b += f'<rect x="{X}" y="{Y}" width="{W}" height="34" rx="12" fill="{IDE_PANEL}"/><rect x="{X}" y="{Y+22}" width="{W}" height="12" fill="{IDE_PANEL}"/>'
    for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        b += f'<circle cx="{X+20+i*18}" cy="{Y+17}" r="5.5" fill="{c}"/>'
    b += text(X + W/2, Y + 22, "java-mods-course — Main.java", 12, IDE_DIM, anchor="middle")
    top = Y + 34
    # 1. дерево курса
    tw = 170
    b += f'<rect x="{X}" y="{top}" width="{tw}" height="{H-34}" fill="{IDE_PANEL}"/>'
    b += f'<line x1="{X+tw}" y1="{top}" x2="{X+tw}" y2="{Y+H}" stroke="{IDE_LINE}"/>'
    tree = [(0, "▾ Раздел 0. Старт", None), (1, "▾ 0.1 Как устроен курс", None), (2, "Добро пожаловать", True),
            (2, "Первая проверка", False), (0, "▾ Раздел 1. Основы", None), (1, "▸ 1.1 Первая программа", None)]
    for i, (lvl, label, done) in enumerate(tree):
        yy = top + 26 + i * 24
        xx = X + 12 + lvl * 14
        if done is not None:
            col = "#5FB865" if done else IDE_DIM
            b += f'<circle cx="{xx+5}" cy="{yy-4}" r="5" fill="none" stroke="{col}" stroke-width="1.6"/>'
            if done:
                b += f'<path d="M{xx+2.5},{yy-4} l2,2.2 l3.5,-4" fill="none" stroke="{col}" stroke-width="1.6"/>'
            xx += 16
        sel = label == "Первая проверка"
        if sel:
            b += f'<rect x="{X+4}" y="{yy-15}" width="{tw-8}" height="21" rx="5" fill="#2E436E"/>'
        b += text(xx, yy, label, 11.5, "#DFE1E5" if sel else IDE_TEXT)
    # 2. редактор
    ex, ew = X + tw, 250
    b += f'<rect x="{ex}" y="{top}" width="{ew}" height="28" fill="{IDE_BG}"/>'
    b += f'<rect x="{ex+8}" y="{top+4}" width="94" height="24" rx="5" fill="{IDE_PANEL}"/>' + text(ex + 18, top + 20, "Main.java", 11.5, "#DFE1E5")
    b += f'<line x1="{ex}" y1="{top+28}" x2="{ex+ew}" y2="{top+28}" stroke="{IDE_LINE}"/>'
    code = ["public class Main {", "  public static void", "    main(String[] a) {", '    System.out.println(', '      "???");', "  }", "}"]
    b += code_block(ex + 24, top + 54, code, size=11.5, lh=20)
    # плейсхолдер
    b += f'<rect x="{ex+42+6*11.5*CW-2:.0f}" y="{top+54+4*20-14}" width="{5*11.5*CW+4:.0f}" height="19" rx="3" fill="none" stroke="#E8A33D" stroke-width="1.3"/>'
    # 3. панель задания
    px, pw = ex + ew, W - tw - ew
    b += f'<line x1="{px}" y1="{top}" x2="{px}" y2="{Y+H}" stroke="{IDE_LINE}"/>'
    b += f'<rect x="{px}" y="{top}" width="{pw}" height="{H-34}" fill="{IDE_PANEL}" rx="0"/>'
    b += f'<rect x="{px}" y="{Y+H-12}" width="{pw}" height="12" rx="12" fill="{IDE_PANEL}"/>'
    b += text(px + 16, top + 30, "Первая проверка", 15, "#DFE1E5", 700)
    for i, wd in enumerate([180, 196, 150, 0, 188, 120]):
        if wd:
            b += f'<rect x="{px+16}" y="{top+48+i*16}" width="{wd}" height="7" rx="3.5" fill="{IDE_LINE}"/>'
    b += f'<rect x="{px+16}" y="{top+150}" width="{pw-32}" height="44" rx="6" fill="{IDE_BG}" stroke="{IDE_LINE}"/>'
    b += text(px + 28, top + 177, "Поехали!", 12, IDE_TEXT, font=MONO)
    by = Y + H - 50
    b += f'<line x1="{px}" y1="{by-14}" x2="{px+pw}" y2="{by-14}" stroke="{IDE_LINE}"/>'
    b += f'<rect x="{px+16}" y="{by}" width="74" height="30" rx="6" fill="#3574F0"/>' + text(px + 53, by + 20, "Check", 13, "#FFFFFF", 600, anchor="middle")
    b += f'<rect x="{px+100}" y="{by}" width="64" height="30" rx="6" fill="none" stroke="{IDE_DIM}"/>' + text(px + 132, by + 20, "Next", 13, IDE_TEXT, anchor="middle")
    # номера зон
    b += badge(X + tw - 18, top + 18, 1) + badge(ex + ew - 18, top + 46, 2) + badge(px + pw - 20, top + 22, 3)
    save(L0 / "t01_welcome/images/ide-layout.svg", svg(w, h, b, "Окно IntelliJ: дерево курса, редактор, панель задания с кнопками Check и Next"))


def placeholder():
    w, h = 560, 170
    b = ide_box(20, 20, 520, 130, "Main.java")
    lines = ["public class Main {", "    public static void main(String[] args) {", '        System.out.println("???");', "    }"]
    b += code_block(46, 74, lines, size=13, lh=21)
    cx = 46 + 18 + len('        System.out.println("') * 13 * CW
    b += f'<rect x="{cx-3:.0f}" y="{74+2*21-15}" width="{3*13*CW+6:.0f}" height="20" rx="4" fill="#E8A33D" fill-opacity="0.18" stroke="#E8A33D" stroke-width="1.5"/>'
    b += arrow(cx + 70, 74 + 2*21 + 30, cx + 18, 74 + 2*21 + 8, ORANGE, 2)
    b += f'<rect x="{cx+66:.0f}" y="{74+2*21+20}" width="200" height="26" rx="13" fill="{ORANGE}"/>'
    b += text(cx + 166, 74 + 2*21 + 38, "сюда пишешь решение", 13, "#FFFFFF", 600, anchor="middle")
    save(L0 / "t02_first_check/images/placeholder.svg", svg(w, h, b, "Выделенная область ??? в коде — место для решения"))


# =====================================================================
# 1.1 Первая программа
# =====================================================================
def anatomy():
    w, h = 680, 290
    cx, cy, lh = 42, 64, 30
    lines = ["public class Main {", "    public static void main(String[] args) {", '        System.out.println("Привет, Майнкрафт!");', "    }", "}"]
    sizes = [13, 13, 11.5, 13, 13]
    b = ide_box(20, 20, 404, 196)
    b += f'<rect x="32" y="{cy-22}" width="378" height="{4*lh+34}" rx="8" fill="none" stroke="{BLUE}" stroke-width="2" stroke-dasharray="5 4"/>'
    b += f'<rect x="64" y="{cy+lh-21}" width="336" height="{2*lh+30}" rx="7" fill="none" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="5 4"/>'
    b += f'<rect x="91" y="{cy+2*lh-17}" width="296" height="24" rx="5" fill="#4E8A2A" fill-opacity="0.28" stroke="#78B653" stroke-width="1.5"/>'
    for i, ln in enumerate(lines):
        b += code_line(cx, cy + i * lh, java_tokens(ln), sizes[i])
    items = [(BLUE, "1  Класс Main", "весь код живёт внутри", cy - 4),
             (ORANGE, "2  Метод main", "отсюда стартует программа", cy + lh + 18),
             (GREEN, "3  Команда", "печатает строку", cy + 2 * lh + 40)]
    for col, t1, t2, yy in items:
        b += f'<rect x="444" y="{yy-16}" width="6" height="40" rx="3" fill="{col}"/>'
        b += text(460, yy, t1, 15, col, 700)
        b += text(460, yy + 20, t2, 13, MUTED)
    rules = [('"текст"', "в кавычках"), (";", "конец команды"), ("{ }", "всегда в паре")]
    for i, (sym, lab) in enumerate(rules):
        x = 24 + i * 214
        b += f'<rect x="{x}" y="232" width="200" height="40" rx="10" fill="#FFFFFF" stroke="{CARD_LINE}"/>'
        b += text(x + 14, 258, sym, 15, ORANGE, 700, font=MONO)
        b += text(x + 14 + len(sym) * 15 * CW + 10, 257, lab, 13, INK)
    save(L1 / "t01_anatomy/images/anatomy.svg", svg(w, h, b, "Разбор программы: класс, метод main и команда println"))


def run_img():
    w, h = 620, 280
    b = ide_box(20, 20, 580, 118, "Main.java")
    lines = ["public class Main {", "    public static void main(String[] args) {", '        System.out.println("Привет, Майнкрафт!");']
    b += code_block(70, 72, lines, size=13, lh=22)
    # зелёный треугольник в гуттере у строки 2
    ty = 72 + 22 - 5
    b += f'<polygon points="{34},{ty-7} {34},{ty+7} {46},{ty}" fill="#5FB865"/>'
    b += f'<circle cx="40" cy="{ty}" r="14" fill="none" stroke="{ORANGE}" stroke-width="2"/>'
    # всплывающее меню
    mx, my = 58, ty + 10
    b += f'<rect x="{mx}" y="{my}" width="200" height="34" rx="7" fill="{IDE_PANEL}" stroke="{IDE_LINE}"/>'
    b += f'<polygon points="{mx+14},{my+11} {mx+14},{my+23} {mx+24},{my+17}" fill="#5FB865"/>'
    b += text(mx + 34, my + 22, "Run 'Main.main()'", 12.5, "#DFE1E5")
    # окно Run
    b += ide_box(20, 152, 580, 110, "Run: Main")
    b += text(40, 206, "Привет, Майнкрафт!", 13.5, "#DFE1E5", font=MONO)
    b += text(40, 232, "Process finished with exit code 0", 12.5, IDE_DIM, font=MONO)
    b += arrow(380, 210, 236, 202, ORANGE, 2)
    b += text(388, 214, "вот что напечатала программа", 13, ORANGE, 600)
    save(L1 / "t01_anatomy/images/run.svg", svg(w, h, b, "Запуск: зелёный треугольник рядом с main и окно Run с выводом"))


def console(x, y, w, h, rows, cursor_rc, fs=14, title="Консоль"):
    s = ide_box(x, y, w, h, title)
    for i, r in enumerate(rows):
        s += text(x + 16, y + 56 + i * 24, r, fs, "#DFE1E5", font=MONO, extra='xml:space="preserve"')
    r, c = cursor_rc
    s += f'<rect x="{x + 16 + c * fs * CW:.1f}" y="{y + 56 + r*24 - fs + 1}" width="{fs*CW:.1f}" height="{fs+3}" fill="#E8A33D"/>'
    return s


def print_vs_println():
    w, h = 680, 250
    b = ""
    for i, (cmd, rows, cur, note) in enumerate([
        ('print("Алмазы: ")', ["Алмазы: "], (0, 8), "курсор остался в той же строке"),
        ('println("Алмазы: 3")', ["Алмазы: 3", ""], (1, 0), "курсор перешёл на новую строку"),
    ]):
        x = 24 + i * 324
        b += f'<rect x="{x}" y="22" width="308" height="34" rx="8" fill="#FFFFFF" stroke="{CARD_LINE}"/>'
        b += code_line(x + 14, 44, java_tokens(cmd), 13.5)
        b += arrow(x + 154, 60, x + 154, 82, MUTED)
        b += console(x, 88, 308, 104, rows, cur)
        b += f'<rect x="{x}" y="204" width="14" height="14" rx="3" fill="#E8A33D"/>'
        b += text(x + 22, 216, "— " + note, 13, INK)
    save(L1 / "t04_print_println/images/print-vs-println.svg", svg(w, h, b, "print оставляет курсор в строке, println переносит его на новую"))


SWORD = ["......cc", ".....cwc", "....cwc.", "c..cwc..", ".ccwc...", "..hc....", ".h.cc...", "h...c..."]
PICK = ["..cccc..", ".cwwwwc.", "c..hh..c", "...hh...", "..hh....", "..hh....", ".hh.....", ".hh....."]
TORCH = ["...ff...", "..fyyf..", "..fyyf..", "...hh...", "...hh...", "...hh...", "...hh...", "...hh..."]
BREAD = ["........", "..bbbb..", ".bBBBBb.", "bBbBbBBb", "bBBBBBBb", ".bbbbbb.", "........", "........"]


def hotbar():
    w, h = 520, 150
    pal = {"c": "#2E2E2E", "w": "#E9EEF2", "h": "#8B5A2B", "f": "#F2A71B", "y": "#FFE36E", "b": "#9C5B1C", "B": "#D9A04A"}
    b = ""
    names = [("Меч", SWORD), ("Кирка", PICK), ("Факел", TORCH), ("Хлеб", BREAD)]
    x0, s = 90, 72
    b += f'<rect x="{x0-6}" y="18" width="{4*s+12}" height="{s+12}" rx="4" fill="#5A5A5A"/>'
    for i, (n, art) in enumerate(names):
        x = x0 + i * s
        b += f'<rect x="{x+3}" y="27" width="{s-6}" height="{s-6}" fill="#8B8B8B" stroke="#373737" stroke-width="3"/>'
        b += pixel_art(x + 12, 36, art, 6, pal)
        b += text(x + s/2, 120, n, 13, INK, 600, anchor="middle")
    b += f'<rect x="{x0-2}" y="22" width="{s+4}" height="{s+4}" fill="none" stroke="#FFFFFF" stroke-width="4"/>'
    b += f'<rect x="{x0-5}" y="19" width="{s+10}" height="{s+10}" fill="none" stroke="#1E1E1E" stroke-width="2"/>'
    b += text(x0 + s/2, 140, "выбран", 11, ORANGE, 700, anchor="middle")
    save(L1 / "t05_hotbar/images/hotbar.svg", svg(w, h, b, "Хотбар: меч, кирка, факел, хлеб; выбран первый слот"))


def escape_img():
    w, h = 680, 250
    b = text(24, 38, "В коде", 13, MUTED, 600)
    src = r'"Стив: \"Копай!\"\nПапка: C:\\games"'
    fs = 14
    x0, y0 = 24, 54
    b += f'<rect x="{x0}" y="{y0}" width="632" height="44" rx="10" fill="{IDE_BG}"/>'
    # раскраска экранирования
    toks, i = [], 0
    colors = {'\\"': "#F0A35E", "\\n": "#7AA7FF", "\\\\": "#C59BF2"}
    while i < len(src):
        pair = src[i:i+2]
        if pair in colors:
            toks.append((pair, colors[pair])); i += 2
        else:
            toks.append((src[i], SYN_STR)); i += 1
    b += f'<text x="{x0+16}" y="{y0+28}" font-family="{MONO}" font-size="{fs}" font-weight="700" xml:space="preserve">' + \
         "".join(f'<tspan fill="{c}">{escape(t)}</tspan>' for t, c in toks) + "</text>"
    b += text(24, 136, "В консоли", 13, MUTED, 600)
    b += f'<rect x="{x0}" y="148" width="632" height="74" rx="10" fill="{IDE_BG}"/>'
    b += text(x0 + 16, 176, 'Стив: "Копай!"', fs, "#DFE1E5", font=MONO)
    b += text(x0 + 16, 204, r"Папка: C:\games", fs, "#DFE1E5", font=MONO)
    # легенда справа
    leg = [('\\"', "кавычка", "#F0A35E"), ("\\n", "новая строка", "#7AA7FF"), ("\\\\", "обратный слеш", "#C59BF2")]
    for k, (sym, lab, col) in enumerate(leg):
        yy = 170 + k * 20
        b += f'<rect x="{430}" y="{yy-13}" width="34" height="18" rx="4" fill="{col}" fill-opacity="0.22"/>'
        b += text(447, yy, sym, 13, col, 700, font=MONO, anchor="middle")
        b += text(472, yy, "→ " + lab, 13, "#DFE1E5")
    save(L1 / "t06_escape/images/escape.svg", svg(w, h, b, "Экранирование: \\\" даёт кавычку, \\n новую строку, \\\\ обратный слеш"))


CREEPER = ["........", ".##..##.", ".##..##.", "...##...", "..####..", "..####..", "..#..#..", "........"]
CREEPER_TEX = ["abacbaca", "cabacbab", "bacabcab", "acbacbac", "cabcabca", "bacbacab", "abcabcba", "cabacabc"]


def creeper():
    w, h = 600, 270
    px, x0, y0 = 26, 30, 30
    greens = {"a": "#5DB13A", "b": "#4C9A2C", "c": "#6FC44A"}
    b = ""
    for r in range(8):
        for c in range(8):
            col = "#1B1B1B" if CREEPER[r][c] == "#" else greens[CREEPER_TEX[r][c]]
            b += f'<rect x="{x0 + c*px}" y="{y0 + r*px}" width="{px}" height="{px}" fill="{col}"/>'
    b += f'<rect x="{x0}" y="{y0}" width="{8*px}" height="{8*px}" fill="none" stroke="#2F5E1B" stroke-width="2"/>'
    b += arrow(x0 + 8*px + 22, y0 + 4*px, x0 + 8*px + 74, y0 + 4*px, MUTED, 2)
    tx = x0 + 8*px + 92
    b += f'<rect x="{tx-6}" y="{y0-6}" width="250" height="{8*px+12}" rx="10" fill="{IDE_BG}"/>'
    for r, row in enumerate(CREEPER):
        for c, ch in enumerate(row):
            b += text(tx + 20 + c * 26, y0 + r * px + 19, ch, 20, "#F2F2F2" if ch == "#" else "#6FC44A", 700, font=MONO, anchor="middle")
    b += text(x0, h - 14, "# — тёмный пиксель", 13, INK) + text(x0 + 170, h - 14, ". — зелёный", 13, INK)
    save(L1 / "t07_creeper/images/creeper.svg", svg(w, h, b, "Лицо крипера 8×8 и та же картинка из символов"))


def errors():
    w, h = 680, 300
    b = ide_box(20, 20, 640, 112, "Main.java")
    lines = ["    public static void main(String[] args) {", '        System.out.println("Ищу алмазы...")', '        System.out.println("Нашёл 3 алмаза!");']
    b += code_block(56, 72, lines, size=13, lh=22, start=2)
    # волнистая линия в конце 3-й строки
    endx = 56 + 18 + len(lines[1]) * 13 * CW
    yw = 72 + 22 + 5
    wave = " ".join(f"l3,{3 if k % 2 == 0 else -3}" for k in range(6))
    b += f'<path d="M{endx-2:.0f},{yw} {wave}" fill="none" stroke="#F75464" stroke-width="1.6"/>'
    # окно Build
    b += ide_box(20, 146, 640, 132, "Build")
    msg_y = 214
    b += code_line(40, msg_y, [("Main.java", "#7AA7FF"), (":", IDE_TEXT), ("3", "#F0A35E"), (": ", IDE_TEXT), ("error: ", "#F75464"), ("';' expected", "#DFE1E5")], 14)
    b += code_line(40, msg_y + 22, [('        System.out.println("Ищу алмазы...")', IDE_DIM)], 13)
    b += code_line(40, msg_y + 40, [(" " * len('        System.out.println("Ищу алмазы...")') + "^", "#F75464")], 13)
    fw = 14 * CW
    labs = [(40 + 4 * fw, "файл", "#7AA7FF"), (40 + 11 * fw, "строка", "#F0A35E"), (40 + 24 * fw, "что не так", "#F75464")]
    for x, lab, col in labs:
        b += f'<rect x="{x - len(lab)*3.6 - 8:.0f}" y="182" width="{len(lab)*7.2 + 16:.0f}" height="19" rx="9.5" fill="{col}" fill-opacity="0.2"/>'
        b += text(x, 195, lab, 12, col, 700, anchor="middle")
    b += text(470, 258, "^ — место ошибки", 12.5, IDE_TEXT)
    save(L1 / "t08_errors/images/errors.svg", svg(w, h, b, "Ошибка компиляции: файл, номер строки, текст ошибки и указатель на место"))


def comments():
    w, h = 640, 256
    b = ide_box(20, 20, 600, 216, "Main.java")
    rows = [('// System.out.println("A: Верстак");', False),
            ('System.out.println("B: Шахта"); // иду копать', True),
            ('/* System.out.println("C: Ферма");', False),
            ('System.out.println("D: Незер"); */', False),
            ('System.out.println("E: Дом");', True)]
    y = 72
    for i, (ln, runs) in enumerate(rows):
        yy = y + i * 28
        if runs:
            b += f'<circle cx="44" cy="{yy-5}" r="8" fill="#3E8E41"/><path d="M40,{yy-5} l3,3 l5,-6" fill="none" stroke="#fff" stroke-width="1.8"/>'
            toks = java_tokens(ln)
        else:
            b += f'<circle cx="44" cy="{yy-5}" r="8" fill="none" stroke="{IDE_DIM}" stroke-width="1.5"/><line x1="39" y1="{yy-5}" x2="49" y2="{yy-5}" stroke="{IDE_DIM}" stroke-width="1.5"/>'
            toks = [(ln, SYN_COM)]
        b += f'<text x="66" y="{yy}" font-family="{MONO}" font-size="13" xml:space="preserve"' + \
             (' font-style="italic"' if not runs else "") + ">" + \
             "".join(f'<tspan fill="{c}">{escape(t)}</tspan>' for t, c in toks) + "</text>"
    b += text(66, 222, "серое — комментарий: Java его пропускает", 12.5, IDE_TEXT)
    save(L1 / "t09_comments/images/comments.svg", svg(w, h, b, "Комментарии: Java выполняет только строки B и E"))


if __name__ == "__main__":
    roadmap(); ide_layout(); placeholder()
    anatomy(); run_img(); print_vs_println(); hotbar(); escape_img(); creeper(); errors(); comments()
