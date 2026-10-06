"""Картинки урока 1.1 «Первая программа». Ширина 480 — под узкую панель задания."""
from images import *  # noqa: F401,F403 — палитра темы и функции рисования

L1 = ROOT / "s01_basics/l01_first_program"


def anatomy():
    w, h = 480, 350
    cx, cy, lh = 36, 62, 30
    lines = ["public class Main {", "    public static void main(String[] args) {",
             '        System.out.println("Привет!");', "    }", "}"]
    b = ide_box(16, 16, 448, 182)
    b += f'<rect x="26" y="{cy - 22}" width="428" height="{4 * lh + 32}" rx="8" fill="none" stroke="{BLUE}" stroke-width="2" stroke-dasharray="5 4"/>'
    b += f'<rect x="52" y="{cy + lh - 21}" width="392" height="{2 * lh + 28}" rx="7" fill="none" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="5 4"/>'
    b += f'<rect x="80" y="{cy + 2 * lh - 17}" width="{len(lines[2].strip()) * 12.5 * CW + 14:.0f}" height="24" rx="5" fill="#4E8A2A" fill-opacity="0.28" stroke="#78B653" stroke-width="1.5"/>'
    for i, ln in enumerate(lines):
        b += code_line(cx, cy + i * lh, java_tokens(ln), 12.5)
    b += badge(442, cy - 4, 1, BLUE) + badge(430, cy + lh + 4, 2, ORANGE) + badge(362, cy + 2 * lh - 5, 3, GREEN)
    items = [(BLUE, "1  Класс Main", "весь код живёт внутри"),
             (ORANGE, "2  Метод main", "отсюда стартует программа"),
             (GREEN, "3  Команда", "печатает строку")]
    for i, (col, t1, t2) in enumerate(items):
        yy = 230 + i * 38
        b += f'<rect x="24" y="{yy - 15}" width="6" height="32" rx="3" fill="{col}"/>'
        b += text(40, yy, t1, 14.5, col, 700) + text(40, yy + 17, t2, 13, MUTED)
    rules = [('"текст"', "в кавычках"), (";", "конец команды"), ("{ }", "всегда в паре")]
    for i, (sym, lab) in enumerate(rules):
        yy = 222 + i * 38
        b += f'<rect x="270" y="{yy}" width="194" height="30" rx="8" fill="{SURFACE}" stroke="{CARD_LINE}"/>'
        b += text(284, yy + 20, sym, 14, ORANGE, 700, font=MONO)
        b += text(284 + len(sym) * 14 * CW + 10, yy + 20, lab, 13, INK)
    save(L1 / "t01_anatomy/images/anatomy.svg", svg(w, h, b, "Разбор программы: класс, метод main и команда println"))


def run_img():
    w, h = 480, 270
    b = ide_box(16, 16, 448, 112, "Main.java")
    lines = ["public class Main {", "    public static void main(", '        System.out.println("Привет!");']
    b += code_block(66, 68, lines, size=13, lh=21)
    ty = 68 + 21 - 5
    b += f'<polygon points="30,{ty - 7} 30,{ty + 7} 42,{ty}" fill="#5FB865"/>'
    b += f'<circle cx="36" cy="{ty}" r="13" fill="none" stroke="{ORANGE}" stroke-width="2"/>'
    mx, my = 54, ty + 10
    b += f'<rect x="{mx}" y="{my}" width="190" height="32" rx="7" fill="{IDE_PANEL}" stroke="{IDE_LINE}"/>'
    b += f'<polygon points="{mx + 14},{my + 10} {mx + 14},{my + 22} {mx + 24},{my + 16}" fill="#5FB865"/>'
    b += text(mx + 32, my + 21, "Run 'Main.main()'", 12.5, "#DFE1E5")
    b += ide_box(16, 144, 448, 108, "Run: Main")
    b += text(34, 198, "Привет!", 14, "#DFE1E5", font=MONO)
    b += text(34, 224, "Process finished with exit code 0", 12, IDE_DIM, font=MONO)
    b += arrow(250, 194, 112, 194, ORANGE, 2)
    b += text(258, 198, "вот что напечатала программа", 13, ORANGE, 600)
    save(L1 / "t01_anatomy/images/run.svg", svg(w, h, b, "Запуск: зелёный треугольник рядом с main и окно Run с выводом"))


def print_vs_println():
    w, h = 480, 250
    b = ""
    for i, (cmd, rows, cur, note) in enumerate([
        ('print("Алмазы: ")', ["Алмазы: "], (0, 8), "курсор остался в строке"),
        ('println("Алмазы: 3")', ["Алмазы: 3", ""], (1, 0), "курсор на новой строке"),
    ]):
        x = 16 + i * 228
        b += f'<rect x="{x}" y="20" width="220" height="34" rx="8" fill="{SURFACE}" stroke="{CARD_LINE}"/>'
        b += code_line(x + 12, 42, java_tokens(cmd, on_card=True), 13)
        b += arrow(x + 110, 58, x + 110, 80, MUTED)
        b += console(x, 86, 220, 104, rows, cur)
        b += f'<rect x="{x}" y="206" width="14" height="14" rx="3" fill="#E8A33D"/>'
        b += text(x + 22, 218, note, 13, INK)
    save(L1 / "t04_print_println/images/print-vs-println.svg",
         svg(w, h, b, "print оставляет курсор в строке, println переносит его на новую"))


SWORD = ["......cc", ".....cwc", "....cwc.", "c..cwc..", ".ccwc...", "..hc....", ".h.cc...", "h...c..."]
PICK = ["..cccc..", ".cwwwwc.", "c..hh..c", "...hh...", "..hh....", "..hh....", ".hh.....", ".hh....."]
TORCH = ["...ff...", "..fyyf..", "..fyyf..", "...hh...", "...hh...", "...hh...", "...hh...", "...hh..."]
BREAD = ["........", "..bbbb..", ".bBBBBb.", "bBbBbBBb", "bBBBBBBb", ".bbbbbb.", "........", "........"]


def hotbar():
    w, h = 480, 160
    pal = {"c": "#2E2E2E", "w": "#E9EEF2", "h": "#8B5A2B", "f": "#F2A71B", "y": "#FFE36E", "b": "#9C5B1C", "B": "#D9A04A"}
    b = ""
    x0, s = 96, 72
    b += f'<rect x="{x0 - 6}" y="18" width="{4 * s + 12}" height="{s + 12}" rx="4" fill="#5A5A5A"/>'
    for i, (n, art) in enumerate([("Меч", SWORD), ("Кирка", PICK), ("Факел", TORCH), ("Хлеб", BREAD)]):
        x = x0 + i * s
        b += f'<rect x="{x + 3}" y="27" width="{s - 6}" height="{s - 6}" fill="#8B8B8B" stroke="#373737" stroke-width="3"/>'
        b += pixel_art(x + 12, 36, art, 6, pal)
        b += text(x + s / 2, 122, n, 14, INK, 600, anchor="middle")
    b += f'<rect x="{x0 - 2}" y="22" width="{s + 4}" height="{s + 4}" fill="none" stroke="#FFFFFF" stroke-width="4"/>'
    b += f'<rect x="{x0 - 5}" y="19" width="{s + 10}" height="{s + 10}" fill="none" stroke="#1E1E1E" stroke-width="2"/>'
    b += text(x0 + s / 2, 143, "выбран", 12.5, ORANGE, 700, anchor="middle")
    save(L1 / "t05_hotbar/images/hotbar.svg", svg(w, h, b, "Хотбар: меч, кирка, факел, хлеб; выбран первый слот"))


def escape_img():
    w, h = 480, 300
    b = text(20, 34, "В коде", 13.5, MUTED, 600)
    src = r'"Стив: \"Копай!\"\nПапка: C:\\games"'
    fs = 14
    b += f'<rect x="16" y="46" width="448" height="44" rx="10" fill="{IDE_BG}"/>'
    toks, i = [], 0
    colors = {'\\"': "#F0A35E", "\\n": "#7AA7FF", "\\\\": "#C59BF2"}
    while i < len(src):
        pair = src[i:i + 2]
        if pair in colors:
            toks.append((pair, colors[pair]))
            i += 2
        else:
            toks.append((src[i], SYN_STR))
            i += 1
    b += f'<text x="30" y="74" font-family="{MONO}" font-size="{fs}" font-weight="700" xml:space="preserve">' + \
         "".join(f'<tspan fill="{c}">{escape(t)}</tspan>' for t, c in toks) + "</text>"
    b += text(20, 122, "В консоли", 13.5, MUTED, 600)
    b += f'<rect x="16" y="134" width="448" height="74" rx="10" fill="{IDE_BG}"/>'
    b += text(30, 163, 'Стив: "Копай!"', fs, "#DFE1E5", font=MONO)
    b += text(30, 191, r"Папка: C:\games", fs, "#DFE1E5", font=MONO)
    leg = [('\\"', "кавычка", "#F0A35E"), ("\\n", "новая строка", "#7AA7FF"), ("\\\\", "слеш \\", "#C59BF2")]
    for k, (sym, lab, col) in enumerate(leg):
        x = 16 + k * 152
        b += f'<rect x="{x}" y="226" width="144" height="54" rx="8" fill="{SURFACE}" stroke="{CARD_LINE}"/>'
        b += f'<rect x="{x + 12}" y="238" width="34" height="22" rx="4" fill="{col}" fill-opacity="0.22"/>'
        b += text(x + 29, 254, sym, 14, col, 700, font=MONO, anchor="middle")
        b += text(x + 54, 254, lab, 13, INK)
    save(L1 / "t06_escape/images/escape.svg",
         svg(w, h, b, "Экранирование: \\\" даёт кавычку, \\n новую строку, \\\\ обратный слеш"))


CREEPER = ["........", ".##..##.", ".##..##.", "...##...", "..####..", "..####..", "..#..#..", "........"]
CREEPER_TEX = ["abacbaca", "cabacbab", "bacabcab", "acbacbac", "cabcabca", "bacbacab", "abcabcba", "cabacabc"]


def creeper():
    w, h = 480, 250
    px, x0, y0 = 22, 20, 20
    greens = {"a": "#5DB13A", "b": "#4C9A2C", "c": "#6FC44A"}
    b = ""
    for r in range(8):
        for c in range(8):
            col = "#1B1B1B" if CREEPER[r][c] == "#" else greens[CREEPER_TEX[r][c]]
            b += f'<rect x="{x0 + c * px}" y="{y0 + r * px}" width="{px}" height="{px}" fill="{col}"/>'
    b += f'<rect x="{x0}" y="{y0}" width="{8 * px}" height="{8 * px}" fill="none" stroke="#2F5E1B" stroke-width="2"/>'
    b += arrow(x0 + 8 * px + 12, y0 + 4 * px, x0 + 8 * px + 46, y0 + 4 * px, MUTED, 2)
    tx = x0 + 8 * px + 58
    b += f'<rect x="{tx}" y="{y0}" width="{w - tx - 16}" height="{8 * px}" rx="10" fill="{IDE_BG}"/>'
    for r, row in enumerate(CREEPER):
        for c, ch in enumerate(row):
            b += text(tx + 24 + c * 25, y0 + r * px + 17, ch, 18, "#F2F2F2" if ch == "#" else "#6FC44A", 700, font=MONO, anchor="middle")
    b += text(x0, h - 26, "# — тёмный пиксель", 13.5, INK) + text(x0 + 180, h - 26, ". — зелёный", 13.5, INK)
    save(L1 / "t07_creeper/images/creeper.svg", svg(w, h, b, "Лицо крипера 8×8 и та же картинка из символов"))


def errors():
    w, h = 480, 300
    b = ide_box(16, 16, 448, 104, "Main.java")
    lines = ['    System.out.println("Ищу алмазы...")', '    system.out.println("Нашёл 3 алмаза!");']
    b += code_block(46, 66, lines, size=12.5, lh=22, start=3)
    endx = 46 + 18 + len(lines[0]) * 12.5 * CW
    yw = 66 + 5
    wave = " ".join(f"l3,{3 if k % 2 == 0 else -3}" for k in range(6))
    b += f'<path d="M{endx - 2:.0f},{yw} {wave}" fill="none" stroke="#F75464" stroke-width="1.6"/>'
    b += ide_box(16, 136, 448, 146, "Build")
    msg_y = 214
    b += code_line(32, msg_y, [("Main.java", "#7AA7FF"), (":", IDE_TEXT), ("3", "#F0A35E"), (": ", IDE_TEXT),
                               ("error: ", "#F75464"), ("';' expected", "#DFE1E5")], 13.5)
    b += code_line(32, msg_y + 24, [('System.out.println("Ищу алмазы...")', IDE_DIM)], 12.5)
    b += code_line(32, msg_y + 42, [(" " * len('System.out.println("Ищу алмазы...")') + "^", "#F75464")], 12.5)
    fw = 13.5 * CW
    labs = [(32 + 3.6 * fw, "файл", "#7AA7FF"), (32 + 11 * fw, "строка", "#F0A35E"), (32 + 23 * fw, "что не так", "#F75464")]
    for x, lab, col in labs:
        b += f'<rect x="{x - len(lab) * 3.6 - 8:.0f}" y="176" width="{len(lab) * 7.2 + 16:.0f}" height="19" rx="9.5" fill="{col}" fill-opacity="0.2"/>'
        b += text(x, 189, lab, 12, col, 700, anchor="middle")
    b += text(448, 274, "^ — место ошибки", 12, IDE_TEXT, anchor="end")
    save(L1 / "t08_errors/images/errors.svg",
         svg(w, h, b, "Ошибка компиляции: файл, номер строки, текст ошибки и указатель на место"))


def comments():
    w, h = 480, 250
    b = ide_box(16, 16, 448, 214, "Main.java")
    rows = [('// System.out.println("A: Верстак");', False),
            ('System.out.println("B: Шахта"); // иду копать', True),
            ('/* System.out.println("C: Ферма");', False),
            ('System.out.println("D: Незер"); */', False),
            ('System.out.println("E: Дом");', True)]
    y = 66
    for i, (ln, runs) in enumerate(rows):
        yy = y + i * 28
        if runs:
            b += f'<circle cx="36" cy="{yy - 5}" r="8" fill="#3E8E41"/><path d="M32,{yy - 5} l3,3 l5,-6" fill="none" stroke="#fff" stroke-width="1.8"/>'
            toks = java_tokens(ln)
        else:
            b += f'<circle cx="36" cy="{yy - 5}" r="8" fill="none" stroke="{IDE_DIM}" stroke-width="1.5"/><line x1="31" y1="{yy - 5}" x2="41" y2="{yy - 5}" stroke="{IDE_DIM}" stroke-width="1.5"/>'
            toks = [(ln, SYN_COM)]
        b += f'<text x="54" y="{yy}" font-family="{MONO}" font-size="12.5" xml:space="preserve"' + \
             (' font-style="italic"' if not runs else "") + ">" + \
             "".join(f'<tspan fill="{c}">{escape(t)}</tspan>' for t, c in toks) + "</text>"
    b += text(54, 214, "серое — комментарий: Java его пропускает", 13, IDE_TEXT)
    save(L1 / "t09_comments/images/comments.svg", svg(w, h, b, "Комментарии: Java выполняет только строки B и E"))


ALL = [anatomy, run_img, print_vs_println, hotbar, escape_img, creeper, errors, comments]
