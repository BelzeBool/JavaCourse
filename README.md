# Java с нуля: от первой строчки до своего мода

Курс в формате плагина **JetBrains Academy** для IntelliJ IDEA: теория в панели задания,
задачи с проверкой по кнопке **Check**. Программа целиком — в `PROGRAM.md`.

Сейчас готово: раздел 0 (как устроен курс), урок 1.1 «Первая программа» (9 шагов) и урок 1.2
«Переменные и типы» (13 шагов) — эталон формата уроков.

## Как открыть

1. В IntelliJ IDEA (подойдёт бесплатная Community) установи плагин **JetBrains Academy**:
   Settings → Plugins → Marketplace.
2. Распакуй архив и открой папку курса через **File → Open**. Плагин увидит `course-info.yaml`
   и откроет курс в режиме автора (Course Creator).
3. Чтобы проходить курс как ученик: правый клик по корню проекта →
   **Course Creator → Preview Course**. Откроется отдельное окно, где решения скрыты
   за плейсхолдерами, а кнопка Check запускает тесты.
4. Если IntelliJ спросит про JDK — выбери или скачай **JDK 21**. Он же нужен для модов на Minecraft 1.21.1.

В режиме автора в файлах `Main.java` лежат **эталонные решения** — не подглядывай,
проходи курс через Course Preview.

## Как работать над курсом на своём компьютере (Claude Code)

**macOS**

```bash
xcode-select --install                 # git и python3, если их ещё нет
git clone https://github.com/BelzeBool/JavaCourse.git
cd JavaCourse
pip3 install -r requirements.txt       # pyyaml, markdown-it-py
export JAVA_HOME=$(/usr/libexec/java_home -v 21)   # JDK 21: проще всего скачать в IntelliJ (File → Project Structure → SDK)
python3 tools/check_lesson.py s01_basics/l02_variables   # проверка, что всё работает
claude                                 # Claude Code в папке курса
```

**Windows** (PowerShell): установи [Git for Windows](https://git-scm.com/download/win) и Python 3
([python.org](https://www.python.org/downloads/), галочка «Add to PATH»), дальше те же команды,
только `py -3` вместо `python3` и `gradlew.bat` вместо `./gradlew`; `JAVA_HOME` — путь к JDK 21
(в IntelliJ: File → Project Structure → SDKs).

Claude Code при старте читает `CLAUDE.md` — там правила проекта, команды и порядок работы.
Дальше достаточно сказать, например: «напиши урок 1.3» (навык `/write-lesson`),
«проверь урок 1.3» (навык `/review-lesson`) или «запусти воркфлоу write-lessons для 1.4 и 1.5».

## Для автора

- `tools/finalize.py` — для новых задач: область решения в коде помечается `/*[*/ ... /*]*/`,
  а в `task-info.yaml` пишется `offset: AUTO` / `length: AUTO`. Скрипт сам посчитает позиции.
- `tools/images.py` — генератор всех иллюстраций в едином стиле, в светлой и тёмной версии.
- `common/src/main/java/course/Check.java` — помощники для тестов с понятными
  сообщениями об ошибках на русском.
- `tools/check_starters.py` — проверка всех задач: эталон проходит тесты, стартовый код ученика — нет.
  Нужен Python 3 и PyYAML (`pip install pyyaml`). Та же проверка идёт в GitHub Actions на каждый push.
- `tools/check_lesson.py` — **полная проверка одного урока**: структура, картинки, компоненты,
  ошибки компилятора (сверяет с javac), порядок понятий, тон, превью, тесты. Запускай после каждой правки.
- `tools/try_solution.py` — прогнать тесты задачи на другом решении и увидеть, что покажет плагин ученику.
- `tools/check_order.py` — проверка «курс не скачет»: шаги не используют понятия из будущих уроков
  (карта понятий — `docs/concepts.yaml`).
- `tools/preview.py` — превью всех шагов в браузере без IntelliJ: `build/preview/index.html`,
  светлая и тёмная тема, разная ширина панели. Нужен `pip install markdown-it-py pyyaml`.
- `lesson-kit/kit.js` — компоненты уроков: плашки, «по-русски», разбор строки, пошаговая трассировка.
- `docs/` — материалы для автора:
  - `decisions.md` — принятые решения;
  - `lesson-design.md` — **как писать уроки** (правила, шаблоны, компоненты, тесты, чек-лист);
  - `concepts.yaml` — карта понятий: что в каком уроке вводится;
  - `sources.md`, `plugin-capabilities.md`, `loader-choice.md` — исследования;
  - `agent-client.md` — эксперимент с ИИ-заказчиком.
