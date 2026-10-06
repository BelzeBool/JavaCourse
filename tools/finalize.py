#!/usr/bin/env python3
"""
Готовит задачи к публикации в формате JetBrains Academy.

В исходнике решения область, которую ученик должен написать сам, помечается так:
    /*[*/ ...эталонное решение... /*]*/
Скрипт убирает маркеры и вписывает в task-info.yaml offset/length этой области
вместо `offset: AUTO` / `length: AUTO` (по порядку: N-й маркер -> N-й AUTO-плейсхолдер файла).

Ещё скрипт дописывает в task-info.yaml все файлы из папки images/ задачи (с visible: false):
без этого картинки, особенно тёмные *_dark.svg, не попадут в архив курса.

Запуск: python3 tools/finalize.py   (из корня курса; повторный запуск безопасен)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "/*[*/", "/*]*/"


def process_task(task_dir: Path) -> None:
    info_path = task_dir / "task-info.yaml"
    info = info_path.read_text(encoding="utf-8")
    if "AUTO" not in info:
        return
    lines = info.split("\n")
    out_lines = []
    current_file = None
    regions = {}
    region_index = {}
    for line in lines:
        m = re.match(r"\s*- name: (.+)$", line)
        if m:
            current_file = m.group(1).strip()
        if "offset: AUTO" in line or "length: AUTO" in line:
            if current_file not in regions:
                src = task_dir / current_file
                text = src.read_text(encoding="utf-8")
                found = []
                while START in text:
                    s = text.index(START)
                    text = text[:s] + text[s + len(START):]
                    e = text.index(END, s)
                    text = text[:e] + text[e + len(END):]
                    found.append((s, e - s))
                src.write_text(text, encoding="utf-8")
                regions[current_file] = found
                region_index[current_file] = 0
                if not found:
                    sys.exit(f"{task_dir}: в {current_file} нет маркеров {START} {END}")
            idx = region_index[current_file]
            if idx >= len(regions[current_file]):
                sys.exit(f"{task_dir}: плейсхолдеров больше, чем маркеров в {current_file}")
            offset, length = regions[current_file][idx]
            if "offset: AUTO" in line:
                line = line.replace("AUTO", str(offset))
            else:
                line = line.replace("AUTO", str(length))
                region_index[current_file] += 1
        out_lines.append(line)
    info_path.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"ok  {task_dir.relative_to(ROOT)}")


def sync_images(task_dir: Path) -> None:
    """Каждый файл из images/ (включая тёмные *_dark.svg) должен быть в task-info.yaml, иначе он не попадёт в курс."""
    images = sorted(p for p in (task_dir / "images").glob("*") if p.is_file()) if (task_dir / "images").is_dir() else []
    if not images:
        return
    info_path = task_dir / "task-info.yaml"
    text = info_path.read_text(encoding="utf-8")
    listed = set(re.findall(r"^\s*- name: (.+?)\s*$", text, re.M))
    missing = [f"images/{p.name}" for p in images if f"images/{p.name}" not in listed]
    if not missing:
        return
    lines = text.rstrip("\n").split("\n")
    if "files:" not in lines:
        sys.exit(f"{task_dir}: в task-info.yaml нет списка files")
    # конец блока files: первая строка без отступа после него (или конец файла)
    start = lines.index("files:")
    end = next((i for i in range(start + 1, len(lines)) if lines[i] and not lines[i].startswith(" ")), len(lines))
    add = []
    for name in missing:
        add += [f"  - name: {name}", "    visible: false"]
    lines[end:end] = add
    info_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"img {task_dir.relative_to(ROOT)}: +{len(missing)}")


for info in sorted(ROOT.glob("s*/*/*/task-info.yaml")):
    process_task(info.parent)
    sync_images(info.parent)
