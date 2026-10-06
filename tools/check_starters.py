#!/usr/bin/env python3
"""
Проверяет главное правило задач: эталон проходит тесты, а стартовый код ученика — нет.

1. Запускает `./gradlew test` на эталонах (как лежат в src/) — всё должно быть зелёным.
2. Копирует курс во временную папку, в каждой задаче типа edu заменяет области
   из task-info.yaml на placeholder_text (так задачу видит ученик) и запускает тесты снова.
   Каждая такая задача обязана упасть — на компиляции или на тестах.

Запуск: python3 tools/check_starters.py   (из корня курса; нужен PyYAML)
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKIP = {".git", ".gradle", ".idea", "build"}


def module_name(task_dir: Path, root: Path) -> str:
    rel = task_dir.relative_to(root)
    return "-".join(re.sub(r"[^A-Za-z0-9_]", "_", p) for p in rel.parts)


def edu_tasks(root: Path):
    for info_path in sorted(root.glob("s*/*/*/task-info.yaml")):
        info = yaml.safe_load(info_path.read_text(encoding="utf-8"))
        if info.get("type") == "edu":
            yield info_path.parent, info


def apply_placeholders(task_dir: Path, info: dict) -> None:
    for f in info.get("files", []):
        placeholders = f.get("placeholders") or []
        if not placeholders:
            continue
        path = task_dir / f["name"]
        text = path.read_text(encoding="utf-8")
        for p in sorted(placeholders, key=lambda p: p["offset"], reverse=True):
            if p["offset"] == "AUTO":
                sys.exit(f"{task_dir}: сначала запусти tools/finalize.py")
            text = text[:p["offset"]] + p["placeholder_text"] + text[p["offset"] + p["length"]:]
        path.write_text(text, encoding="utf-8")


def gradle(root: Path, modules):
    args = [str(root / "gradlew"), "-p", str(root), "--continue", "--console=plain", "-q"]
    args += [f":{m}:test" for m in modules]
    return subprocess.run(args, capture_output=True, text=True)


def failed_modules(output: str):
    return set(re.findall(r"Execution failed for task ':([^:]+):", output))


def main() -> int:
    tasks = list(edu_tasks(ROOT))
    modules = [module_name(d, ROOT) for d, _ in tasks]
    ok = True

    print("1/2 Эталоны должны проходить тесты…")
    res = gradle(ROOT, modules)
    bad = failed_modules(res.stdout + res.stderr)
    for m in modules:
        print(("  ok   " if m not in bad else "  FAIL ") + m)
    if res.returncode != 0:
        ok = False
        if not bad:
            print(res.stdout[-3000:], res.stderr[-3000:])

    print("2/2 Стартовый код должен НЕ проходить тесты…")
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "course"
        shutil.copytree(ROOT, copy, ignore=lambda d, names: [n for n in names if n in SKIP])
        for task_dir, info in edu_tasks(copy):
            apply_placeholders(task_dir, info)
        res = gradle(copy, modules)
        bad = failed_modules(res.stdout + res.stderr)
        for m in modules:
            if m in bad:
                print("  ok   " + m)
            else:
                ok = False
                print("  FAIL " + m + " — стартовый код проходит тесты, задача решается без ученика")

    print("Всё в порядке." if ok else "Есть проблемы, см. выше.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
