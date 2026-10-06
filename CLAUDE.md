# Курс «Java с нуля: от первой строчки до своего мода»

Мы с Безей (автор курса, учит Java с нуля, цель — моды для Minecraft, потом Kotlin и Android)
делаем собственный курс для плагина **JetBrains Academy** в IntelliJ IDEA: теория в панели задания,
задачи с кнопкой **Check** и JUnit-тестами. Всё на русском, всё в тематике Minecraft.

## Перед работой прочитай

1. `docs/decisions.md` — что уже решено (Minecraft **1.21.1**, **JDK 21**, классический `public class Main`,
   macOS + Windows, свой темп, глава про Git, загрузчик модов ещё не выбран).
2. `docs/lesson-design.md` — **как писать уроки**: правила, ритм урока, шаблоны шагов,
   сквозные метафоры, компоненты, задачи, тесты, чек-лист. Это главный документ.
3. `PROGRAM.md` — программа курса: какие уроки есть, план шагов каждого урока, статус (✅ — готов).
4. Эталонный урок — `s01_basics/l02_variables` (урок 1.2). Новые уроки делай так же.

## Главные правила

- **Язык и тон:** русский, к ученику на «ты», коротко, без воды. Никаких глаголов прошедшего времени
  с родом про ученика («ты нашёл» → «у тебя есть», «нашлось»); не «сам/сама» про ученика.
- **Не скакать:** шаг использует только понятия из пройденных уроков. Карта — `docs/concepts.yaml`,
  проверка — `tools/check_order.py`. Забегание вперёд — только осознанно, с `<!-- preview: id — зачем -->`.
- **Одна идея — один шаг.** После каждой идеи — вопрос или задача. Не больше двух теорий подряд.
- **Факты Minecraft — для версии 1.21.1.** Сообщения компилятора — только настоящие (проверяются автоматически).
- **Панель задания узкая (~480 px):** картинки шириной 480, таблицы максимум в 2–3 короткие колонки,
  длинные сравнения — списком.
- **Не меняй** решения из `docs/decisions.md`, эталонные решения чужих уроков и общие файлы
  (`lesson-kit/kit.js`, `common/.../Check.java`, `docs/concepts.yaml`, `tools/*`) без причины.
  Если нужно — меняй осознанно и прогоняй проверки всего курса.

## Устройство репозитория

| Путь | Что там |
|---|---|
| `course-info.yaml`, `sNN_*/section-info.yaml`, `lNN_*/lesson-info.yaml` | структура курса для плагина |
| `sNN_*/lNN_*/tNN_*/` | шаг: `task.md`, `task-info.yaml`, `src/Main.java` (эталон), `test/Tests.java`, `images/` |
| `common/src/main/java/course/Check.java` | помощники для тестов (сообщения на русском, номера строк) |
| `lesson-kit/kit.js` | компоненты уроков: плашки, «по-русски», разбор строки, трассировка, ошибки |
| `tools/images.py` + `tools/img/*.py` | картинки: общий стиль + один модуль на урок; светлая и тёмная версии |
| `tools/check_lesson.py` | **полная проверка одного урока** — запускай после любой правки |
| `tools/finalize.py` | плейсхолдеры `/*[*/ … /*]*/` → offset/length, картинки → task-info.yaml |
| `tools/check_order.py`, `tools/check_starters.py`, `tools/preview.py` | порядок понятий; эталон/старт всего курса; превью |
| `docs/` | решения, руководство, карта понятий, исследования, агент-заказчик |
| `.claude/skills/` | навыки `write-lesson` и `review-lesson` |
| `.claude/workflows/write-lessons.js` | воркфлоу: автор → два рецензента → исправления |

## Команды

```bash
pip3 install -r requirements.txt                     # один раз: pyyaml, markdown-it-py
python3 tools/check_lesson.py s01_basics/l03_arithmetic   # проверить урок (всё, включая тесты)
python3 tools/check_lesson.py s01_basics/l03_arithmetic --no-gradle   # быстро, без тестов
python3 tools/images.py s01_l03                       # перерисовать картинки урока
python3 tools/preview.py                              # превью всего курса: build/preview/index.html
python3 tools/preview.py --bundle s01_basics/l03_arithmetic   # один урок одним файлом: build/lesson-l03_arithmetic.html
python3 tools/check_order.py && python3 tools/check_starters.py && ./gradlew :common:test   # весь курс
```

Тесты Gradle требуют JDK 21 (или новее). На macOS: `JAVA_HOME=$(/usr/libexec/java_home -v 21)`.

## Как написать урок

Навык **`/write-lesson 1.3`** — пошаговая инструкция. Коротко:

1. План шагов урока — в `PROGRAM.md`. Понятия урока — в `docs/concepts.yaml`, метафоры —
   в `docs/lesson-design.md` (раздел 5).
2. Папка `sNN_<раздел>/lNN_<урок>/` с `lesson-info.yaml` и шагами `tNN_<имя>/`.
3. В эталонном `src/Main.java` область ученика — между `/*[*/` и `/*]*/`, в `task-info.yaml` —
   `offset: AUTO`, `length: AUTO`.
4. Картинки — модуль `tools/img/sNN_lNN_<имя>.py` (шаблон в `tools/img/README.md`).
5. `python3 tools/check_lesson.py <папка урока>` до нуля ошибок; предупреждения — разобрать.
6. Внести урок в `section-info.yaml`, поставить ✅ в `PROGRAM.md`, закоммитить.

Проверить чужой или свой урок придирчиво — навык **`/review-lesson 1.3`**.
Несколько уроков сразу — воркфлоу `write-lessons` (если в твоём Claude Code есть Workflow):
`запусти воркфлоу write-lessons для уроков 1.4 и 1.5`.

## Git

- Сообщения коммитов — на русском, по сути: «Урок 1.3 «Арифметика»: 11 шагов, 5 задач».
- `build/` и `.gradle/` не коммитим (они в `.gitignore`).
- Перед коммитом: `python3 tools/check_order.py` и `check_lesson.py` для изменённых уроков.

## Что сейчас в работе

Смотри раздел «Что сделать дальше» в конце `PROGRAM.md` и ✅ в списке уроков.
