#!/usr/bin/env python3
"""
Прогоняет тесты одной задачи на другом решении и показывает то, что увидит ученик.

Нужен, чтобы проверить тесты: ловят ли они типичные ошибки и понятно ли о них сообщают.
Курс не меняется — всё происходит во временной копии.

    python3 tools/try_solution.py s01_basics/l02_variables/t10_level wrong.java
    python3 tools/try_solution.py s01_basics/l02_variables/t10_level --starter
    python3 tools/try_solution.py s01_basics/l02_variables/t10_level --body 'int level = 12; System.out.println(level);'

  wrong.java  — файл, который подставится вместо src/Main.java;
  --starter   — стартовый код ученика (области ответа заменены на placeholder_text);
  --body '…'  — заменить всё тело main на этот код (удобно для коротких проб).

Печатает сообщения тестов так, как их покажет плагин, и итог: ПРОШЛО или НЕ ПРОШЛО.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_starters as cs  # noqa: E402


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    task_dir = (ROOT / sys.argv[1]).resolve()
    rel = task_dir.relative_to(ROOT)
    info = yaml.safe_load((task_dir / "task-info.yaml").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "course"
        copy.mkdir()
        for name in ("build.gradle.kts", "settings.gradle.kts", "gradle.properties", "gradlew", "gradlew.bat"):
            shutil.copy2(ROOT / name, copy / name)
        skip = shutil.ignore_patterns("build", ".gradle")
        shutil.copytree(ROOT / "gradle", copy / "gradle")
        shutil.copytree(ROOT / "common", copy / "common", ignore=skip)
        shutil.copytree(task_dir, copy / rel, ignore=skip)
        main_java = copy / rel / "src" / "Main.java"
        mode = sys.argv[2]
        if mode == "--starter":
            cs.apply_placeholders(copy / rel, info)
        elif mode == "--body":
            body = sys.argv[3]
            src = main_java.read_text(encoding="utf-8")
            new = re.sub(r"(public static void main\(String\[\] args\) \{\n)[\s\S]*?(\n    \}\n)",
                         lambda m: m.group(1) + "        " + body + m.group(2), src, count=1)
            main_java.write_text(new, encoding="utf-8")
        else:
            shutil.copy2(Path(mode), main_java)
        module = cs.module_name(copy / rel, copy)
        res = subprocess.run([str(copy / "gradlew"), "-p", str(copy), "--console=plain", "-q", f":{module}:test"],
                             capture_output=True, text=True)
        out = res.stdout + res.stderr
        shown = [l.replace("#educational_plugin", "", 1) for l in out.splitlines() if l.startswith("#educational_plugin")]
        compile_errors = list(dict.fromkeys(re.sub(r"^.*?(\w+\.java:\d+: error:)", r"\1", l)
                                            for l in out.splitlines() if re.search(r"\.java:\d+: error:", l)))
        if shown:
            print("Что увидит ученик:")
            print("\n".join("  " + l for l in shown))
        elif compile_errors:
            print("Ошибка компиляции (ученик увидит её в окне Build):")
            print("\n".join("  " + l for l in compile_errors[:10]))
        print("\nИтог:", "ПРОШЛО" if res.returncode == 0 else "НЕ ПРОШЛО")
        return 0


if __name__ == "__main__":
    sys.exit(main())
