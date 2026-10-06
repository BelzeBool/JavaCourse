---
name: write-lesson
description: Написать один урок курса «Java с нуля» по плану из PROGRAM.md — все шаги, задачи, тесты, картинки — и довести tools/check_lesson.py до нуля ошибок. Запуск — /write-lesson 1.3 (номер урока из PROGRAM.md).
---

# Написать урок

Аргумент — номер урока, например `1.3`. Работаешь в корне репозитория курса.

## 0. Где урок лежит

Папки разделов и уроков (номер урока → папка). Если папки ещё нет — создай с этим именем.

| Раздел | Папка | Уроки |
|---|---|---|
| 0 | `s00_start` | `l01_how` |
| 1 | `s01_basics` | `l01_first_program`, `l02_variables`, `l03_arithmetic`, `l04_strings`, `l05_conditions`, `l06_loops`, `l07_methods`, `l08_arrays`, `l09_input`, `l10_project` (проект главы) |
| 2 | `s02_oop` | `l01_classes`, `l02_constructors`, `l03_encapsulation`, `l04_static`, `l05_inheritance`, `l06_polymorphism`, `l07_interfaces`, `l08_enum_record`, `l09_project` |
| 3 | `s03_git` | `l01_git`, `l02_github` |
| 4 | `s04_first_mod` | `l01_setup`, `l02_structure`, `l03_item`, `l04_block`, `l05_recipes` |
| 5 | `s05_collections` | `l01_list`, `l02_map`, `l03_set`, `l04_generics`, `l05_optional`, `l06_mod_checkpoint` |
| 6 | `s06_lambdas` | `l01_exceptions`, `l02_lambdas`, `l03_method_refs`, `l04_streams`, `l05_mod_checkpoint` |
| 7 | `s07_serious_mod` | `l01_gradle`, `l02_block_entity`, `l03_mob`, `l04_mixins`, `l05_neoforge`, `l06_final_project` |

Шаги: `tNN_<короткое_английское_имя>`, номера с нулём.

## 1. Прочитай

- `docs/lesson-design.md` — целиком. Это правила.
- В `PROGRAM.md` — план этого урока и **двух предыдущих** (что ученик уже знает, какие задачи были).
- В `docs/concepts.yaml` — какие понятия вводит этот урок (`since`) и какие доступны (все с меньшим `since`).
- Эталон `s01_basics/l02_variables`: минимум `t01_chest` (теория с компонентами), `t02_quiz_quotes`
  (вопрос), `t07_player_card` и `t10_level` (задачи с тестами), `t13_recap` (итог).
- Итог (последний шаг) предыдущего урока, если он уже написан, — чтобы продолжить с того же места.

## 2. Спланируй

Распиши шаги урока (8–14) по ритму из `lesson-design.md` §3: зацепка → идея → вопрос → задача →
следующая идея → … → «почини» → итог. План из `PROGRAM.md` — основа, но улучшай его: одна идея на
шаг, после каждой идеи — действие, не больше двух теорий подряд. Для каждого шага проверь:
какие понятия он использует — все ли уже пройдены? Метафора — из списка в §5 (или добавь новую
в отчёт). Факты Minecraft — верны для 1.21.1? Сомневаешься — не используй.

## 3. Напиши файлы

Для каждого шага: `task.md`, `task-info.yaml`, `src/Main.java`; у задач — `test/Tests.java`.
`lesson-info.yaml` урока: `custom_name: "1.3 Арифметика"` и `content` со всеми шагами по порядку.

- `task.md` начинается с `# <custom_name>` и заканчивается строкой
  `<script src="../../../lesson-kit/kit.js"></script>`.
- Компоненты и их разметка — `lesson-design.md` §6. В чисто-HTML компонентах (k-trace, k-anatomy,
  k-error, k-vars) — ни одной пустой строки внутри.
- Каждая ошибка компилятора в `k-error` — настоящая: `check_lesson.py` сверит её с javac.
  Ошибку времени выполнения помечай `data-javac="skip"`.
- У теории в `src/Main.java` — пример из текста, его можно запустить.
- У вопроса (`choice`): 3–5 вариантов, неверные — типичные заблуждения; `message_correct` объясняет
  почему, `message_incorrect` — как рассуждать, не выдавая ответ; `local_check: true`.
- У задачи (`edu`): эталон в `src/Main.java`, область ученика — между `/*[*/` и `/*]*/`,
  в `task-info.yaml` — `offset: AUTO`, `length: AUTO`, `placeholder_text`.
- Картинки — модуль `tools/img/sNN_lNN_<имя>.py` (шаблон — `tools/img/README.md`), ширина 480,
  потом `python3 tools/images.py sNN_lNN`. В `task.md` — `<img src="images/x.svg" alt="…" width="480"/>`.

## 4. Тесты

`lesson-design.md` §9 и помощники `Check` (`common/src/main/java/course/Check.java`):
`runMain`, `runMainWithInput`, `assertOutput`, `assertDeclared`, `assertCode`, `count`,
`assertNoNumbers`, `call`, `assertCall`, `callOn`, `newObject`.

- С урока 1.7 задачи — это методы: тест вызывает `Check.assertCall(3, Main.class, "stacks", 200)`
  на нескольких входах, включая граничные (0, отрицательные, пустой массив). **Не вызывай методы
  ученика напрямую** (`Main.stacks(200)`): если метода нет, ученик увидит непонятную ошибку
  компиляции в скрытом файле тестов. `Check.call` даст понятное сообщение.
- Один тест — одна мысль. Сообщение: что не так, где, что делать.
- Закрой обходы, убивающие смысл задачи (готовый текст вместо переменной, посчитанное в уме число),
  но не придирайся к стилю.

## 5. Проверь

```bash
python3 tools/check_lesson.py sNN_раздел/lNN_урок
```

Доведи до **нуля ошибок**. Предупреждения разбери: исправь или осознанно оставь (и скажи почему).

Потом **пробы на неправильных решениях** — для каждой задачи 2–3 типичные ошибки новичка:

```bash
python3 tools/try_solution.py <папка задачи> --body 'код тела main с ошибкой'
python3 tools/try_solution.py <папка задачи> wrong.java
```

Каждая проба должна НЕ ПРОЙТИ с понятным сообщением. Если проба проходит или сообщение
непонятное — чини тест. Файлы проб клади во временную папку, не в репозиторий.

Последний шаг — перечитай урок глазами новичка по чек-листу `lesson-design.md` §11
(превью: `build/lesson-<урок>.html`).

## 6. Заверши

- Урок — в `content` файла `section-info.yaml` раздела (новый раздел — ещё и в `course-info.yaml`).
- В `PROGRAM.md` — ✅ у урока и короткая строка, что в нём (как у 1.2).
- Если урок ввёл новую метафору или понятие — допиши в `lesson-design.md` §5 / `docs/concepts.yaml`.
- `python3 tools/check_order.py` — весь курс зелёный.

**Если тебя запустили внутри воркфлоу** с указанием не трогать общие файлы — не меняй
`section-info.yaml`, `course-info.yaml`, `PROGRAM.md`, `docs/*`, `lesson-kit/*`, `common/*`, `tools/*.py`
(свой модуль `tools/img/…` — можно). Нужные правки в них опиши в отчёте.

## Отчёт

Коротко: папка урока, список шагов (тип + название), что проверено (`check_lesson`: ошибок 0,
предупреждения и что с ними), какие пробы сделаны, нужные правки общих файлов, сомнения.
