#!/usr/bin/env python3
"""
Полная проверка одного урока — запускай после каждой правки урока.

    python3 tools/check_lesson.py s01_basics/l03_arithmetic
    python3 tools/check_lesson.py s01_basics/l03_arithmetic --no-gradle   (быстро, без тестов)

Что делает:
  1. finalize только для этого урока (плейсхолдеры AUTO, картинки в task-info.yaml);
  2. структура: lesson-info.yaml ↔ папки, task-info.yaml каждого шага, тесты у задач,
     варианты у вопросов, строка подключения lesson-kit в конце task.md;
  3. картинки: файл есть, есть тёмная версия, есть alt, ширина не больше 560;
  4. компоненты: в чисто-HTML компонентах (k-trace, k-anatomy, k-error, k-vars) нет пустых строк,
     у k-trace правильная таблица;
  5. ошибки компилятора в k-error сверяются с настоящим javac (если его удалось найти);
  6. порядок понятий (tools/check_order.py --only);
  7. стиль: длина теории, длина блоков кода, «ты …л» (прошедшее время с родом про ученика);
  8. превью урока одним файлом: build/lesson-<урок>.html;
  9. тесты в изолированной копии курса: эталон проходит, стартовый код — нет.

Ошибки (✗) надо исправить. Предупреждения (⚠) — посмотреть и решить.
Нужны пакеты: pip install -r requirements.txt
"""
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

KIT_LINE = '<script src="../../../lesson-kit/kit.js"></script>'
HTML_ONLY = ("k-trace", "k-anatomy", "k-error", "k-vars")
TYPES = {"theory", "choice", "edu", "output", "ide"}

errors, warnings = [], []


def err(where, msg):
    errors.append(f"{where}: {msg}")


def warn(where, msg):
    warnings.append(f"{where}: {msg}")


def load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


# ---------- javac ----------
def find_javac():
    cands = []
    if os.environ.get("JAVA_HOME"):
        cands.append(Path(os.environ["JAVA_HOME"]) / "bin" / "javac")
    if sys.platform == "darwin":
        r = run(["/usr/libexec/java_home", "-v", "21"])
        if r.returncode == 0:
            cands.append(Path(r.stdout.strip()) / "bin" / "javac")
    cands += sorted(Path("/usr/lib/jvm").glob("*21*/bin/javac")) if Path("/usr/lib/jvm").exists() else []
    w = shutil.which("javac")
    if w:
        cands.append(Path(w))
    for c in cands:
        if c.exists():
            return str(c)
    return None


def div_blocks(text, cls):
    """Содержимое всех <div class="... cls ..."> с учётом вложенных div."""
    out = []
    pat = re.compile(r'<div\b[^>]*\bclass="[^"]*\b' + re.escape(cls) + r'\b[^"]*"[^>]*>')
    for m in pat.finditer(text):
        depth, i = 1, m.end()
        tag = re.compile(r"<(/?)div\b[^>]*>")
        while depth:
            t = tag.search(text, i)
            if not t:
                break
            depth += -1 if t.group(1) else 1
            i = t.end()
        out.append((m.group(0), text[m.end():t.start() if t else len(text)], text[:m.start()].count("\n") + 1))
    return out


def check_javac(task_dir, text, javac):
    where = f"{task_dir.name}/task.md"
    for opening, inner, line in div_blocks(text, "k-error"):
        if 'data-javac="skip"' in opening:
            continue
        pres = re.findall(r"<pre\b([^>]*)>([\s\S]*?)</pre>", inner)
        code = next((html.unescape(c) for a, c in pres if "k-msg" not in a), None)
        msg = next((html.unescape(c) for a, c in pres if "k-msg" in a), None)
        if code is None or msg is None:
            err(where, f"k-error в строке {line}: нужен <pre>код</pre> и <pre class=\"k-msg\">сообщение</pre>")
            continue
        if javac is None:
            continue
        first = msg.strip().split("\n")[0]
        if not first.startswith("error:"):
            warn(where, f"k-error в строке {line}: сообщение не начинается с «error:» — это точно ошибка компилятора? "
                        f"Если это ошибка во время работы, поставь data-javac=\"skip\"")
            continue
        expected = first[len("error:"):].strip()
        src = code if re.search(r"\bclass\s+\w+", code) else (
            "public class Main {\n    public static void main(String[] args) {\n" + code + "\n    }\n}\n")
        name = re.search(r"public\s+class\s+(\w+)", src)
        fname = (name.group(1) if name else "Main") + ".java"
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / fname).write_text(src, encoding="utf-8")
            r = run([javac, "-encoding", "UTF-8", "-d", tmp, fname], cwd=tmp)
        out = r.stdout + r.stderr
        if r.returncode == 0:
            err(where, f"k-error в строке {line}: javac компилирует этот код без ошибок, а в уроке написано «{first}»")
        elif expected not in out:
            got = next((l.split("error:", 1)[1].strip() for l in out.splitlines() if "error:" in l), out.strip()[:200])
            err(where, f"k-error в строке {line}: javac пишет «error: {got}», а в уроке «{first}»")


# ---------- проверки шага ----------
def check_task(task_dir, javac):
    where = task_dir.name
    info_path = task_dir / "task-info.yaml"
    if not info_path.exists():
        err(where, "нет task-info.yaml")
        return
    info = load(info_path)
    typ = info.get("type")
    if typ not in TYPES:
        err(where, f"неизвестный type: {typ}")
    if not info.get("custom_name"):
        err(where, "нет custom_name")
    files = info.get("files") or []
    names = {f.get("name") for f in files}
    for f in files:
        if not (task_dir / f["name"]).exists():
            err(where, f"в task-info.yaml есть файл {f['name']}, а на диске его нет")
        for p in f.get("placeholders") or []:
            if p.get("offset") == "AUTO" or p.get("length") == "AUTO":
                err(where, "плейсхолдер AUTO не обработан — запусти tools/finalize.py")
    if "src/Main.java" not in names:
        warn(where, "нет src/Main.java — у каждого шага в редакторе должен быть код")
    if typ == "edu":
        if not (task_dir / "test" / "Tests.java").exists():
            err(where, "у задачи нет test/Tests.java")
        if not any(f.get("placeholders") for f in files):
            warn(where, "у задачи нет плейсхолдеров — что пишет ученик?")
    if typ == "output" and not (task_dir / "test" / "output.txt").exists():
        err(where, "у задачи на вывод нет test/output.txt")
    if typ == "choice":
        opts = info.get("options") or []
        right = [o for o in opts if o.get("is_correct")]
        if len(opts) < 3:
            warn(where, "меньше трёх вариантов ответа")
        if not right:
            err(where, "ни один вариант не помечен is_correct: true")
        if not info.get("is_multiple_choice") and len(right) != 1:
            err(where, "вопрос с одним ответом, а верных вариантов не один")
        for k in ("message_correct", "message_incorrect"):
            if not info.get(k):
                err(where, f"нет {k}")
        if info.get("local_check") is not True:
            err(where, "у вопроса должно быть local_check: true")

    md = task_dir / "task.md"
    if not md.exists():
        err(where, "нет task.md")
        return
    text = md.read_text(encoding="utf-8")
    mdw = f"{where}/task.md"
    if text.rstrip().splitlines()[-1].strip() != KIT_LINE:
        err(mdw, f"последняя строка должна быть {KIT_LINE}")
    first = text.lstrip().splitlines()[0] if text.strip() else ""
    if first.startswith("# ") and first[2:].strip() != str(info.get("custom_name", "")).strip():
        warn(mdw, f"заголовок «{first[2:].strip()}» не совпадает с custom_name «{info.get('custom_name')}»")

    # картинки
    for m in re.finditer(r"<img\b[^>]*>", text):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag)
        if not src:
            err(mdw, "у <img> нет src")
            continue
        src = src.group(1)
        f = task_dir / src
        if not f.exists():
            err(mdw, f"картинки {src} нет на диске")
            continue
        dark = f.with_name(f.stem + "_dark" + f.suffix)
        if not dark.exists():
            err(mdw, f"нет тёмной версии {dark.name} — нарисуй её через tools/images.py")
        for img in (src, f"{os.path.dirname(src)}/{dark.name}" if os.path.dirname(src) else dark.name):
            if img not in names:
                err(where, f"{img} нет в task-info.yaml — запусти tools/finalize.py")
        if not re.search(r'alt="[^"]{8,}"', tag):
            err(mdw, f"у картинки {src} нет понятного alt")
        w = re.search(r'width="(\d+)"', tag)
        if w and int(w.group(1)) > 560:
            warn(mdw, f"картинка {src} шире 560 — в узкой панели текст станет мелким")
        vb = re.search(r'viewBox="0 0 (\d+)', f.read_text(encoding="utf-8")[:500]) if f.suffix == ".svg" else None
        if vb and int(vb.group(1)) > 560:
            warn(mdw, f"{src}: рисунок шириной {vb.group(1)} — рисуй под 480")

    # компоненты из чистого HTML: без пустых строк
    for cls in HTML_ONLY:
        for opening, inner, line in div_blocks(text, cls):
            if re.search(r"\n[ \t]*\n", inner):
                err(mdw, f"{cls} в строке {line}: внутри пустая строка — Markdown разорвёт блок")
    for opening, inner, line in div_blocks(text, "k-trace"):
        pre = re.search(r"<pre>([\s\S]*?)</pre>", inner)
        rows = re.findall(r"<tr>([\s\S]*?)</tr>", inner)
        if not pre or len(rows) < 2:
            err(mdw, f"k-trace в строке {line}: нужен <pre>код</pre> и таблица минимум из двух строк")
            continue
        n_lines = len(html.unescape(pre.group(1)).strip("\n").split("\n"))
        head = re.findall(r"<t[hd]\b[^>]*>", rows[0])
        if len(head) < 3:
            err(mdw, f"k-trace в строке {line}: в заголовке таблицы меньше трёх колонок")
        for r in rows[1:]:
            cells = re.findall(r"<td\b[^>]*>([\s\S]*?)</td>", r)
            if len(cells) != len(head):
                err(mdw, f"k-trace в строке {line}: в строке таблицы {len(cells)} ячеек, а в заголовке {len(head)}")
                break
            num = re.sub(r"<[^>]+>", "", cells[0]).strip()
            if not num.isdigit() or not 1 <= int(num) <= n_lines:
                err(mdw, f"k-trace в строке {line}: в первой колонке должен быть номер строки кода 1–{n_lines}, а там «{num}»")
                break

    check_javac(task_dir, text, javac)

    # стиль
    prose = re.sub(r"```[\s\S]*?```", "", text)
    prose = re.sub(r"<pre\b[\s\S]*?</pre>", "", prose)
    prose = re.sub(r"<div class=\"hint\"[\s\S]*?</div>", "", prose)
    words = len(re.findall(r"[А-Яа-яЁёA-Za-z]+", re.sub(r"<[^>]+>", " ", prose)))
    if typ == "theory" and words > 450:
        warn(mdw, f"теория длинная: ~{words} слов (ориентир — до 300–400). Может, это два шага?")
    for m in re.finditer(r"```java\n([\s\S]*?)```", text):
        n = m.group(1).rstrip("\n").count("\n") + 1
        if n > 14:
            warn(mdw, f"блок кода в {n} строк (ориентир — до 12)")
    for m in re.finditer(r"\bты\s+(?:\w+\s+)?([а-яё]+(?:ал|ял|ил|ел|ёл|ул|ыл|ла|ло))\b", text, re.I):
        warn(mdw, f"«{m.group(0)}» — похоже на прошедшее время с родом про ученика. Перефразируй")
    for sent in re.split(r"(?<=[.!?…])\s+|\n\s*\n", re.sub(r"<[^>]+>", " ", prose)):
        if not re.search(r"\b(ты|тебе|тебя|себе)\b", sent, re.I):
            continue
        m = re.search(r"\b(сам|сама|уверен|уверена|готов|готова|должен|должна|рад|рада)\b", sent)
        if m:
            warn(mdw, f"«{m.group(1)}» рядом с «ты» — род про ученика? «{sent.strip()[:90]}»")


# ---------- тесты в изолированной копии ----------
def gradle_check(lesson_dir):
    import check_starters as cs
    rel = lesson_dir.relative_to(ROOT)
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "course"
        copy.mkdir()
        for name in ("build.gradle.kts", "settings.gradle.kts", "gradle.properties", "gradlew", "gradlew.bat"):
            shutil.copy2(ROOT / name, copy / name)
        skip = shutil.ignore_patterns("build", ".gradle")
        shutil.copytree(ROOT / "gradle", copy / "gradle")
        shutil.copytree(ROOT / "common", copy / "common", ignore=skip)
        shutil.copytree(lesson_dir, copy / rel, ignore=skip)
        tasks = list(cs.edu_tasks(copy))
        if not tasks:
            print("  (в уроке нет задач с тестами)")
            return
        modules = [cs.module_name(d, copy) for d, _ in tasks]
        res = cs.gradle(copy, modules)
        bad = cs.failed_modules(res.stdout + res.stderr)
        for m in modules:
            if m in bad:
                err(m, "эталонное решение НЕ проходит тесты")
        if res.returncode != 0 and not bad:
            err(str(rel), "сборка упала:\n" + (res.stdout + res.stderr)[-2500:])
            return
        if bad:
            fails = [l for l in (res.stdout + res.stderr).splitlines() if "#educational_plugin" in l][:20]
            print("\n".join("    " + l for l in fails))
        for task_dir, info in tasks:
            cs.apply_placeholders(task_dir, info)
        res = cs.gradle(copy, modules)
        bad = cs.failed_modules(res.stdout + res.stderr)
        for m in modules:
            if m not in bad:
                err(m, "стартовый код ученика проходит тесты — задача решается без ученика")
        print(f"  тесты: {len(modules)} задач(и) — эталон и старт проверены")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    lesson_dir = (ROOT / args[0]).resolve()
    rel = lesson_dir.relative_to(ROOT)
    if not (lesson_dir / "lesson-info.yaml").exists():
        print(f"Нет {rel}/lesson-info.yaml")
        return 1

    print(f"1. finalize {rel}")
    r = run([sys.executable, str(ROOT / "tools" / "finalize.py"), str(rel)], cwd=ROOT)
    if r.returncode != 0:
        err(str(rel), "finalize: " + (r.stdout + r.stderr).strip())

    print("2–5. структура, картинки, компоненты, javac")
    linfo = load(lesson_dir / "lesson-info.yaml")
    if not linfo.get("custom_name"):
        err(str(rel), "нет custom_name в lesson-info.yaml")
    content = linfo.get("content") or []
    dirs = sorted(p.name for p in lesson_dir.iterdir() if p.is_dir() and (p / "task-info.yaml").exists())
    for d in dirs:
        if d not in content:
            warn(str(rel), f"папка {d} не внесена в lesson-info.yaml")
    javac = find_javac()
    if javac is None:
        warn(str(rel), "javac не найден — ошибки компилятора в k-error не сверены (укажи JAVA_HOME)")
    for t in content:
        if not (lesson_dir / t).is_dir():
            err(str(rel), f"в lesson-info.yaml есть {t}, а папки нет")
            continue
        check_task(lesson_dir / t, javac)
    section_info = load(lesson_dir.parent / "section-info.yaml") if (lesson_dir.parent / "section-info.yaml").exists() else {}
    if lesson_dir.name not in (section_info.get("content") or []):
        warn(str(rel), "урок ещё не внесён в section-info.yaml раздела")

    print("6. порядок понятий")
    r = run([sys.executable, str(ROOT / "tools" / "check_order.py"), "--only", str(rel)], cwd=ROOT)
    for line in r.stdout.splitlines():
        if line.startswith("✗"):
            err("порядок", line[2:])

    print("8. превью")
    r = run([sys.executable, str(ROOT / "tools" / "preview.py"), "--bundle", str(rel)], cwd=ROOT)
    if r.returncode != 0:
        err("превью", (r.stdout + r.stderr).strip()[-500:])
    else:
        print("  " + r.stdout.strip().splitlines()[0])

    if "--no-gradle" not in sys.argv:
        print("9. тесты (изолированная копия курса)")
        gradle_check(lesson_dir)

    print()
    for w in warnings:
        print("⚠", w)
    for e in errors:
        print("✗", e)
    print(f"\nИтог: ошибок {len(errors)}, предупреждений {len(warnings)}.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
