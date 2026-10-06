"""Картинки раздела 0, урок «Как устроен курс». Ширина 480 — под узкую панель задания."""
from images import *  # noqa: F401,F403 — палитра темы и функции рисования

L0 = ROOT / "s00_start/l01_how"


def roadmap():
    w, h = 480, 300
    b = text(24, 34, "Путь курса", 16, INK, 700)
    b += f'<rect x="300" y="22" width="14" height="14" rx="3" fill="{GREEN}"/>' + text(320, 34, "с модом", 13, MUTED)
    # две строки «блоков»: 1–4 слева направо, 5–7 справа налево — как дорожка
    steps = [("1", "Основы", False), ("2", "ООП", False), ("3", "Git", False), ("4", "Первый мод", True),
             ("5", "Коллекции", True), ("6", "Лямбды", True), ("7", "Свой мод", True)]
    size, gap = 56, 116
    pos = [(40 + i * gap, 70) for i in range(4)] + [(40 + (3 - i) * gap, 190) for i in range(3)]
    # дорожка
    pts = [(x + size / 2, y + size / 2) for x, y in pos]
    d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts[:4])
    d += f" L{pts[4][0]:.0f},{pts[4][1]:.0f}"
    d += "".join(f" L{x:.0f},{y:.0f}" for x, y in pts[4:])
    b += f'<path d="{d}" fill="none" stroke="{CARD_LINE}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>'
    for (n, label, mod), (x, y) in zip(steps, pos):
        top, side = (GREEN, "#3B6D1F") if mod else ("#8A8F9C", "#6B707C")
        b += f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="8" fill="{side}"/>'
        b += f'<rect x="{x}" y="{y}" width="{size}" height="{size - 9}" rx="8" fill="{top}"/>'
        b += text(x + size / 2, y + 33, n, 22, "#FFFFFF", 700, anchor="middle")
        lw = len(label) * 8 + 10  # подложка под подписью, чтобы её не перечёркивала дорожка
        b += f'<rect x="{x + size / 2 - lw / 2:.0f}" y="{y + size + 8}" width="{lw}" height="20" fill="{CARD}"/>'
        b += text(x + size / 2, y + size + 22, label, 13.5, INK, 600, anchor="middle")
    # «ты здесь»
    x0 = pos[0][0]
    b += f'<path d="M{x0 + size / 2 - 7},{60} l7,8 l7,-8 z" fill="{ORANGE}"/>'
    b += text(x0 + size / 2, 54, "ты здесь", 12.5, ORANGE, 700, anchor="middle")
    save(L0 / "t01_welcome/images/roadmap.svg",
         svg(w, h, b, "Путь курса: основы, ООП, Git, первый мод, коллекции, лямбды, свой мод"))


def ide_layout():
    w, h = 480, 330
    X, Y, W, H = 16, 16, 448, 250
    b = f'<rect x="{X}" y="{Y}" width="{W}" height="{H}" rx="12" fill="{IDE_BG}" stroke="{IDE_LINE}"/>'
    b += f'<rect x="{X}" y="{Y}" width="{W}" height="28" rx="12" fill="{IDE_PANEL}"/><rect x="{X}" y="{Y + 16}" width="{W}" height="12" fill="{IDE_PANEL}"/>'
    for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        b += f'<circle cx="{X + 18 + i * 16}" cy="{Y + 14}" r="5" fill="{c}"/>'
    top = Y + 28
    zones = [(X, 120, "1", "Дерево курса"), (X + 120, 168, "2", "Редактор"), (X + 288, 160, "3", "Задание")]
    for x, zw, n, label in zones:
        fill = IDE_PANEL if n != "2" else IDE_BG
        b += f'<rect x="{x}" y="{top}" width="{zw}" height="{H - 28}" fill="{fill}"/>'
        b += f'<line x1="{x}" y1="{top}" x2="{x}" y2="{Y + H}" stroke="{IDE_LINE}"/>' if n != "1" else ""
    # 1. дерево: строки-заглушки с галочкой
    for i, (lvl, wd, done) in enumerate([(0, 80, None), (1, 70, None), (2, 60, True), (2, 64, False), (0, 76, None), (1, 66, None)]):
        yy = top + 24 + i * 22
        xx = X + 12 + lvl * 10
        if done is not None:
            col = "#5FB865" if done else IDE_DIM
            b += f'<circle cx="{xx + 4}" cy="{yy - 3}" r="4.5" fill="none" stroke="{col}" stroke-width="1.5"/>'
            xx += 13
        b += f'<rect x="{xx}" y="{yy - 7}" width="{wd - lvl * 10}" height="7" rx="3.5" fill="{IDE_LINE}"/>'
    # 2. редактор: код
    code = ["class Main {", "  main() {", "    println(", '      "???");', "  }", "}"]
    for i, ln in enumerate(code):
        b += code_line(X + 132, top + 30 + i * 22, java_tokens(ln), 12.5)
    # 3. задание: текст-заглушки и кнопки
    px = X + 288
    b += text(px + 12, top + 26, "Первая проверка", 12.5, "#DFE1E5", 700)
    for i, wd in enumerate([130, 120, 136, 90]):
        b += f'<rect x="{px + 12}" y="{top + 42 + i * 14}" width="{wd}" height="6" rx="3" fill="{IDE_LINE}"/>'
    by = Y + H - 44
    b += f'<rect x="{px + 12}" y="{by}" width="62" height="28" rx="6" fill="#3574F0"/>' + text(px + 43, by + 19, "Check", 12.5, "#FFFFFF", 600, anchor="middle")
    b += f'<rect x="{px + 82}" y="{by}" width="54" height="28" rx="6" fill="none" stroke="{IDE_DIM}"/>' + text(px + 109, by + 19, "Next", 12.5, IDE_TEXT, anchor="middle")
    # номера зон и подписи под окном
    for x, zw, n, label in zones:
        b += badge(x + zw - 18, top + 18, n)
        b += text(x + zw / 2, Y + H + 26, f"{n}. {label}", 13.5, INK, 600, anchor="middle")
    b += text(240, Y + H + 50, "Check — проверить, Next — следующий шаг", 13, MUTED, anchor="middle")
    save(L0 / "t01_welcome/images/ide-layout.svg",
         svg(w, h, b, "Окно IntelliJ: слева дерево курса, в центре редактор, справа задание с кнопками Check и Next"))


def placeholder():
    w, h = 480, 190
    b = ide_box(16, 16, 448, 128, "Main.java")
    lines = ["public class Main {", "    public static void", "      main(String[] args) {", '        System.out.println("???");']
    b += code_block(40, 66, lines, size=13, lh=20)
    cx = 40 + 18 + len('        System.out.println("') * 13 * CW
    b += f'<rect x="{cx - 3:.0f}" y="{66 + 3 * 20 - 15}" width="{3 * 13 * CW + 6:.0f}" height="20" rx="4" fill="#E8A33D" fill-opacity="0.18" stroke="#E8A33D" stroke-width="1.5"/>'
    b += arrow(cx - 30, 158, cx + 8, 66 + 3 * 20 + 8, ORANGE, 2)
    b += f'<rect x="{cx - 196:.0f}" y="150" width="190" height="26" rx="13" fill="{ORANGE}"/>'
    b += text(cx - 101, 168, "сюда пишешь решение", 13, "#FFFFFF", 600, anchor="middle")
    save(L0 / "t02_first_check/images/placeholder.svg",
         svg(w, h, b, "Выделенная область ??? в коде — место для решения"))


ALL = [roadmap, ide_layout, placeholder]
