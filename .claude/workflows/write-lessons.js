export const meta = {
  name: 'write-lessons',
  description: 'Написать уроки курса: автор → два рецензента (педагогика, правильность) → исправления',
  whenToUse: 'Написать один или несколько уроков по плану из PROGRAM.md. args: ["1.3", "1.4"] или [{id: "1.3", dir: "s01_basics/l03_arithmetic", notes: "..."}]',
  phases: [
    { title: 'Автор', detail: 'пишет урок по навыку write-lesson до нуля ошибок check_lesson' },
    { title: 'Рецензия', detail: 'два независимых рецензента: педагогика и правильность с пробами' },
    { title: 'Исправления', detail: 'проверяет замечания, исправляет подтверждённые' },
  ],
}

const lessons = (Array.isArray(args) ? args : [args]).filter(Boolean)
  .map(x => (typeof x === 'string' ? { id: x } : x))

const AUTHOR_SCHEMA = {
  type: 'object',
  properties: {
    dir: { type: 'string', description: 'папка урока, например s01_basics/l03_arithmetic' },
    steps: { type: 'array', items: { type: 'string' }, description: 'шаги: "t01_x (theory): Название"' },
    check_errors: { type: 'integer', description: 'ошибок check_lesson.py в конце' },
    warnings_left: { type: 'array', items: { type: 'string' } },
    probes: { type: 'array', items: { type: 'string' }, description: 'пробы неправильных решений и что показали' },
    shared_changes: { type: 'array', items: { type: 'string' }, description: 'какие правки нужны в общих файлах' },
    doubts: { type: 'array', items: { type: 'string' } },
  },
  required: ['dir', 'steps', 'check_errors', 'shared_changes'],
}

const REVIEW_SCHEMA = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          severity: { type: 'string', enum: ['blocker', 'major', 'minor'] },
          where: { type: 'string' },
          problem: { type: 'string' },
          evidence: { type: 'string', description: 'как проверено: команда и результат' },
          fix: { type: 'string' },
        },
        required: ['severity', 'where', 'problem', 'fix'],
      },
    },
    checked: { type: 'string', description: 'что именно проверено' },
  },
  required: ['findings', 'checked'],
}

const FIX_SCHEMA = {
  type: 'object',
  properties: {
    applied: { type: 'array', items: { type: 'string' } },
    rejected: {
      type: 'array',
      items: { type: 'object', properties: { finding: { type: 'string' }, why: { type: 'string' } }, required: ['finding', 'why'] },
    },
    check_errors: { type: 'integer' },
    shared_changes: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  },
  required: ['applied', 'rejected', 'check_errors', 'summary'],
}

const RULES = 'Работаешь внутри воркфлоу параллельно с другими уроками. Не коммить. ' +
  'Не меняй общие файлы: section-info.yaml, course-info.yaml, PROGRAM.md, CLAUDE.md, docs/*, lesson-kit/*, common/*, tools/*.py ' +
  '(свой модуль tools/img/<урок>.py — можно) и другие уроки. Нужные правки общих файлов опиши в shared_changes.'

const results = await pipeline(
  lessons,
  l => agent(
    `Напиши урок ${l.id} курса${l.dir ? ` в папке ${l.dir}` : ''}. Первым делом прочитай .claude/skills/write-lesson/SKILL.md ` +
    `и выполни его от начала до конца, включая пробы неправильных решений. ${RULES} ` +
    `После тебя урок проверят два рецензента — сделай так, чтобы им было не к чему придраться. ${l.notes || ''}`,
    { label: `автор ${l.id}`, phase: 'Автор', schema: AUTHOR_SCHEMA },
  ),
  (a, l) => parallel([
    () => agent(
      `Проверь урок ${l.id} (папка ${a.dir}) по навыку .claude/skills/review-lesson/SKILL.md. ` +
      `Твоя зона — пункты A (ученик с нуля: понятность, «не скакать», ритм, метафоры, условия задач) и D (тон, вёрстка, картинки). ` +
      `Пункты B и C проверяет другой рецензент. Ничего не правь.`,
      { label: `рецензия ${l.id}: педагогика`, phase: 'Рецензия', schema: REVIEW_SCHEMA },
    ),
    () => agent(
      `Проверь урок ${l.id} (папка ${a.dir}) по навыку .claude/skills/review-lesson/SKILL.md. ` +
      `Твоя зона — пункты B (правильность: запускай код, сверяй ответы вопросов, факты Minecraft 1.21.1) и C (тесты: ` +
      `для каждой задачи минимум три пробы через tools/try_solution.py — старт, типичная ошибка, правильное-но-другое решение). ` +
      `Пункты A и D проверяет другой рецензент. Ничего не правь.`,
      { label: `рецензия ${l.id}: правильность`, phase: 'Рецензия', schema: REVIEW_SCHEMA },
    ),
  ]).then(rs => ({ author: a, findings: rs.filter(Boolean).flatMap(r => r.findings) })),
  (r, l) => agent(
    `Доведи урок ${l.id} (папка ${r.author.dir}) после рецензии. Ниже замечания двух рецензентов. ` +
    `Для каждого проверь, верно ли оно (запусти, если можно). Подтвердилось — исправь; blocker и major — обязательно. ` +
    `Не подтвердилось — отклони и объясни почему. ${RULES} ` +
    `В конце: python3 tools/check_lesson.py ${r.author.dir} — ноль ошибок.\n\n` +
    `Замечания:\n${JSON.stringify(r.findings, null, 1)}\n\n` +
    `Автор просил правки общих файлов: ${JSON.stringify(r.author.shared_changes || [])}`,
    { label: `исправления ${l.id}`, phase: 'Исправления', schema: FIX_SCHEMA },
  ).then(f => ({ lesson: l.id, dir: r.author.dir, steps: r.author.steps, author: r.author, findings: r.findings, fix: f })),
)

return results.filter(Boolean)
