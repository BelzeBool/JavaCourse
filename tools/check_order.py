#!/usr/bin/env python3
"""
Проверка «курс не скачет»: в каждом шаге используются только понятия, которые уже пройдены.

Для каждого шага берётся код:
  - все .java-файлы из src/ (эталонное решение и готовый код вокруг него);
  - блоки кода из task.md: ```java ... ``` и <pre>...</pre> (в том числе внутри компонентов k-*).
Код очищается (комментарии, содержимое строк, шапка Main/main) и сверяется с docs/concepts.yaml:
если понятие вводится в более позднем уроке, это ошибка.

Осознанное забегание вперёд разрешается комментарием в task.md: <!-- preview: arith, mul-div — зачем -->

Запуск: python3 tools/check_order.py        (нужен PyYAML)
        python3 tools/check_order.py -v     (ещё и показать, какие понятия есть в каждом шаге)
"""
import html
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def lesson_key(task_dir: Path):
    """s01_basics/l02_variables/t03 → (1, 2)."""
    rel = task_dir.relative_to(ROOT).parts
    sec = re.match(r"s(\d+)", rel[0])
    les = re.match(r"l(\d+)", rel[1])
    return int(sec.group(1)), int(les.group(1))


def parse_since(s):
    a, b = str(s).split(".")
    return int(a), int(b)


def clean(code: str) -> str:
    code = re.sub(r'"""[\s\S]*?"""', '""', code)                 # текстовые блоки
    code = re.sub(r"/\*[\s\S]*?\*/", " ", code)                  # /* ... */
    out = []
    for line in code.split("\n"):
        # строки и символы: содержимое убираем, кавычки оставляем
        line = re.sub(r'"(?:\\.|[^"\\])*"', '""', line)
        line = re.sub(r"'(?:\\.|[^'\\])*'", "''", line)
        line = re.sub(r"//.*$", "", line)
        out.append(line)
    code = "\n".join(out)
    # шапка программы — «заклинание» из урока 1.1
    code = re.sub(r"\b(public\s+)?(final\s+)?class\s+Main\s*\{", " ", code)
    code = re.sub(r"\b(public\s+)?static\s+void\s+main\s*\(\s*(final\s+)?String\s*(\[\s*\]|\.\.\.)\s*\w+\s*\)\s*(throws\s+\w+\s*)?\{",
                  " ", code)
    return code


def task_code(task_dir: Path):
    """Возвращает список (откуда, код)."""
    parts = []
    src = task_dir / "src"
    if src.is_dir():
        for f in sorted(src.rglob("*.java")):
            parts.append((str(f.relative_to(task_dir)), f.read_text(encoding="utf-8")))
    md = task_dir / "task.md"
    if md.exists():
        text = md.read_text(encoding="utf-8")
        for m in re.finditer(r"```java\s*\n([\s\S]*?)```", text):
            parts.append(("task.md", m.group(1)))
        for m in re.finditer(r"<pre\b[^>]*>([\s\S]*?)</pre>", text):
            inner = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
            if re.search(r"error:|warning:", inner) and "\n" not in inner.strip():
                continue  # сообщение компилятора, а не код
            parts.append(("task.md", inner))
    return parts


def previews(task_dir: Path):
    md = task_dir / "task.md"
    if not md.exists():
        return set()
    found = set()
    for m in re.finditer(r"<!--\s*preview:\s*([^>]*?)-->", md.read_text(encoding="utf-8")):
        ids = re.split(r"\s+[—-]\s+", m.group(1), maxsplit=1)[0]  # после « — » можно написать пояснение
        found |= {x.strip() for x in ids.split(",") if x.strip()}
    return found


def main():
    verbose = "-v" in sys.argv
    concepts = yaml.safe_load((ROOT / "docs" / "concepts.yaml").read_text(encoding="utf-8"))["concepts"]
    for c in concepts:
        c["re"] = re.compile(c["find"], re.M)
        c["since_key"] = parse_since(c["since"])
    ids = {c["id"] for c in concepts}

    problems, checked = [], 0
    for info in sorted(ROOT.glob("s*/l*/*/task-info.yaml")):
        task_dir = info.parent
        key = lesson_key(task_dir)
        allowed = previews(task_dir)
        for unknown in allowed - ids:
            problems.append(f"{task_dir.relative_to(ROOT)}: в <!-- preview --> неизвестное понятие «{unknown}»")
        used = {}
        for origin, code in task_code(task_dir):
            cleaned = clean(code)
            for c in concepts:
                if c["re"].search(cleaned):
                    used.setdefault(c["id"], (c, origin))
        checked += 1
        if verbose:
            print(f"{task_dir.relative_to(ROOT)} [{key[0]}.{key[1]}]: {', '.join(sorted(used)) or '—'}")
        for cid, (c, origin) in used.items():
            if c["since_key"] > key and cid not in allowed:
                problems.append(f"{task_dir.relative_to(ROOT)} ({origin}): «{c['name']}» — это урок {c['since']}, "
                                f"а шаг в уроке {key[0]}.{key[1]}. Убери или пометь <!-- preview: {cid} -->")
        for cid in allowed:
            c = next((c for c in concepts if c["id"] == cid), None)
            if c and cid not in used:
                problems.append(f"{task_dir.relative_to(ROOT)}: <!-- preview: {cid} --> лишний — понятие в коде не встречается")

    for p in problems:
        print("✗", p)
    print(f"Проверено шагов: {checked}. " + ("Порядок понятий в порядке." if not problems else f"Проблем: {len(problems)}."))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
