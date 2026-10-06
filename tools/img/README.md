# Картинки уроков

Один модуль на урок: `tools/img/<раздел>_<урок>_<имя>.py`, например `s01_l03_arithmetic.py`.
`python3 tools/images.py` находит модули сам и рисует каждую картинку в двух темах:
`x.svg` и `x_dark.svg`. Потом запусти `python3 tools/finalize.py` — он внесёт картинки
в `task-info.yaml`.

```python
"""Картинки урока 1.3 «Арифметика»."""
from images import *  # палитра текущей темы и все функции рисования: svg, text, code_line, arrow, chest_px…

L = ROOT / "s01_basics/l03_arithmetic"


def stacks():
    w, h = 480, 240                       # ширина 480 — панель задания узкая
    b = text(24, 40, "200 блоков", 16, INK, 700)
    # ... рисуем
    save(L / "t02_stacks/images/stacks.svg", svg(w, h, b, "Описание картинки словами"))


ALL = [stacks]
```

Правила — в `docs/lesson-design.md`, раздел «Картинки»: ширина 480, шрифт от 13.5,
цвета только из палитры (`INK`, `MUTED`, `BLUE`, `ORANGE`, `GREEN`, `RED`, `PURPLE`, `SURFACE`, `CARD_LINE`…),
код на карточке — `java_tokens(line, on_card=True)`, в «окне IDE» — `java_tokens(line)`.
Готовые детали: `ide_box`, `code_block`, `console`, `badge`, `arrow`, `pixel_art`,
`chest_px` (сундук-переменная), `sign_px` (табличка), `type_tag` (метка типа).
