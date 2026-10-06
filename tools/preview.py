#!/usr/bin/env python3
"""
Превью курса в браузере — без IntelliJ.

Собирает все шаги курса в HTML-страницы, похожие на панель задания плагина JetBrains Academy:
- task.md → HTML (GitHub Flavored Markdown, как в плагине);
- первый заголовок шага убирается и заменяется названием шага (так делает плагин);
- <div class="hint"> превращаются в свёрнутые подсказки;
- &shortcut:ActionId; заменяются на сочетания клавиш macOS / Windows;
- картинки *_dark.svg подставляются в тёмной теме;
- подключается lesson-kit/kit.js — интерактивные компоненты работают как в IDE;
- для вопросов (choice) работают варианты ответа и кнопка Check;
- под заданием показан код в редакторе глазами ученика: области ответа заменены на плейсхолдеры.

Запуск:  python3 tools/preview.py           (нужны пакеты: pip install markdown-it-py pyyaml)
Открыть: build/preview/index.html

Один файл на урок (удобно переслать или открыть на телефоне):
         python3 tools/preview.py --bundle s01_basics/l02_variables   → build/lesson-l02_variables.html

Превью — приближение. Последнее слово за Course Preview в IntelliJ.
"""
import base64
import html
import json
import os
import re
import shutil
import sys
from pathlib import Path

import yaml
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "preview"

# Сочетания для частых действий IntelliJ (macOS / Windows и Linux)
SHORTCUTS = {
    "EditorDuplicate": ("⌘D", "Ctrl+D"),
    "ReformatCode": ("⌥⌘L", "Ctrl+Alt+L"),
    "CommentByLineComment": ("⌘/", "Ctrl+/"),
    "CommentByBlockComment": ("⌥⌘/", "Ctrl+Shift+/"),
    "MoveLineUp": ("⌥⇧↑", "Alt+Shift+↑"),
    "MoveLineDown": ("⌥⇧↓", "Alt+Shift+↓"),
    "MoveStatementUp": ("⌘⇧↑", "Ctrl+Shift+↑"),
    "MoveStatementDown": ("⌘⇧↓", "Ctrl+Shift+↓"),
    "RunClass": ("⌃⇧R", "Ctrl+Shift+F10"),
    "Run": ("⌃R", "Shift+F10"),
    "Debug": ("⌃D", "Shift+F9"),
    "ToggleLineBreakpoint": ("⌘F8", "Ctrl+F8"),
    "StepOver": ("F8", "F8"),
    "StepInto": ("F7", "F7"),
    "Resume": ("⌥⌘R", "F9"),
    "GotoDeclaration": ("⌘B", "Ctrl+B"),
    "ShowIntentionActions": ("⌥↩", "Alt+Enter"),
    "ExtractMethod": ("⌥⌘M", "Ctrl+Alt+M"),
    "RenameElement": ("⇧F6", "Shift+F6"),
    "EditorSelectWord": ("⌥↑", "Ctrl+W"),
    "CodeCompletion": ("⌃Space", "Ctrl+Space"),
    "ParameterInfo": ("⌘P", "Ctrl+P"),
    "QuickJavaDoc": ("F1", "Ctrl+Q"),
    "Find": ("⌘F", "Ctrl+F"),
    "SearchEverywhere": ("⇧⇧", "Shift Shift"),
    "SaveAll": ("⌘S", "Ctrl+S"),
    "$Undo": ("⌘Z", "Ctrl+Z"),
    "ActivateRunToolWindow": ("⌘4", "Alt+4"),
    "ActivateProjectToolWindow": ("⌘1", "Alt+1"),
    "ActivateCommitToolWindow": ("⌘0", "Alt+0"),
    "CheckinProject": ("⌘K", "Ctrl+K"),
    "Vcs.Push": ("⇧⌘K", "Ctrl+Shift+K"),
    "Vcs.UpdateProject": ("⌘T", "Ctrl+T"),
    "Vcs.ShowTabbedFileHistory": ("—", "—"),
}

TYPE_ICON = {"theory": "📖", "choice": "❓", "edu": "🛠", "output": "📤", "ide": "🎮"}
TYPE_NAME = {"theory": "Теория", "choice": "Вопрос", "edu": "Задача", "output": "Задача на вывод", "ide": "Действие"}

md = MarkdownIt("commonmark", {"html": True}).enable("table").enable("strikethrough")


def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


# ---------- структура курса ----------
def course_tree():
    course = load_yaml(ROOT / "course-info.yaml")
    tree = []
    for sec in course.get("content", []):
        sdir = ROOT / sec
        sinfo = load_yaml(sdir / "section-info.yaml")
        lessons = []
        for les in sinfo.get("content", []):
            ldir = sdir / les
            linfo = load_yaml(ldir / "lesson-info.yaml")
            tasks = []
            for t in linfo.get("content", []):
                tdir = ldir / t
                tinfo = load_yaml(tdir / "task-info.yaml")
                tasks.append({"dir": tdir, "id": t, "info": tinfo,
                              "name": tinfo.get("custom_name", t), "type": tinfo.get("type", "theory")})
            lessons.append({"dir": ldir, "id": les, "name": linfo.get("custom_name", les), "tasks": tasks})
        tree.append({"dir": sdir, "id": sec, "name": sinfo.get("custom_name", sec), "lessons": lessons})
    return course, tree


# ---------- подсветка Java (как в kit.js, но на Python) ----------
KW = set(("abstract boolean break byte case catch char class continue default do double else enum extends final "
          "finally float for if implements import instanceof int interface long new package private protected public "
          "record return short static super switch this throw throws try var void while true false null").split())
TOKEN = re.compile(r'(//.*$)|("(?:\\.|[^"\\])*"?)|(\'(?:\\.|[^\'\\])*\'?)|(\b\d+(?:\.\d+)?[LlFfDd]?\b)'
                   r'|([A-Za-z_]\w*)(?=\s*\()|([A-Za-z_]\w*)|([\s\S])', re.M)


def highlight_java(code):
    out = []
    for m in TOKEN.finditer(code):
        com, s1, s2, num, fn, word, other = m.groups()
        e = html.escape(m.group(0), quote=False)
        if com:
            out.append(f'<span class="pv-com">{e}</span>')
        elif s1 or s2:
            out.append(f'<span class="pv-str">{e}</span>')
        elif num:
            out.append(f'<span class="pv-num">{e}</span>')
        elif fn:
            out.append(f'<span class="pv-{"kw" if fn in KW else "fn"}">{e}</span>')
        elif word:
            out.append(f'<span class="pv-kw">{e}</span>' if word in KW else e)
        else:
            out.append(e)
    return "".join(out)


# ---------- обработка HTML как в плагине ----------
def cut_out_header(h):
    """Плагин убирает первый заголовок, если он единственный своего уровня и стоит в самом начале."""
    for tag in ("h1", "h2", "h3"):
        found = re.findall(rf"<{tag}[ >]", h)
        if len(found) == 1:
            m = re.match(rf"\s*<{tag}[^>]*>.*?</{tag}>\s*", h, re.S)
            if m:
                return h[m.end():]
            return h
    return h


def replace_divs(h, cls, fn):
    """Находит <div class="... cls ..."> с учётом вложенных div и заменяет fn(attrs, inner)."""
    pat = re.compile(r'<div\b([^>]*\bclass="[^"]*\b' + re.escape(cls) + r'\b[^"]*"[^>]*)>')
    pos = 0
    while True:
        m = pat.search(h, pos)
        if not m:
            return h
        depth, i = 1, m.end()
        tag = re.compile(r"<(/?)div\b[^>]*>")
        while depth:
            t = tag.search(h, i)
            if not t:
                return h
            depth += -1 if t.group(1) else 1
            i = t.end()
        inner = h[m.end():t.start()]
        rep = fn(m.group(1), inner)
        h = h[:m.start()] + rep + h[i:]
        pos = m.start() + len(rep)


def wrap_hints(h):
    def hint(attrs, inner):
        title = re.search(r'title="([^"]*)"', attrs)
        title = title.group(1) if title else "Подсказка"
        return f'<details class="pv-hint"><summary>💡 {title}</summary><div class="pv-hint-body">{inner}</div></details>'
    return replace_divs(h, "hint", hint)


def highlight_code(h):
    def block(m):
        lang = m.group(1) or ""
        code = html.unescape(m.group(2))
        body = highlight_java(code) if lang in ("java", "") else html.escape(code, quote=False)
        return f'<pre class="pv-code-block">{body}</pre>'
    h = re.sub(r'<pre><code(?: class="language-(\w+)")?>(.*?)</code></pre>', block, h, flags=re.S)
    h = re.sub(r"<code>(.*?)</code>", lambda m: '<span class="pv-code">' + m.group(1) + "</span>", h, flags=re.S)
    return h


def shortcuts(h):
    def rep(m):
        mac, win = SHORTCUTS.get(m.group(1), (m.group(1), m.group(1)))
        return f'<kbd class="pv-kbd" title="&amp;shortcut:{m.group(1)};">{mac}</kbd> <span class="pv-kbd-alt">(Windows: <kbd class="pv-kbd">{win}</kbd>)</span>'
    return re.sub(r"&(?:amp;)?shortcut:([\w.$]+);", rep, h)


def rewrite_links(h, task_dir, page_of):
    def course_link(m):
        target = (ROOT / m.group(1)).resolve()
        for p, page in page_of.items():
            if p == target or p.parent == target or p.parent.parent == target:
                return f'href="{os.path.relpath(page, OUT / task_dir.relative_to(ROOT))}"'
        return 'href="#" title="не найдено"'
    h = re.sub(r'href="course://([^"]+)"', course_link, h)
    h = re.sub(r'href="psi_element://([^"]+)"', r'href="#" class="pv-psi" title="В IDE откроется документация: \1"', h)
    return h


def images(h, task_dir, out_dir, inline=False):
    """Копирует картинки рядом со страницей (или встраивает их в HTML при inline=True)."""
    def data_uri(f):
        mime = "image/svg+xml" if f.suffix == ".svg" else "image/" + f.suffix.lstrip(".")
        return f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode()

    def rep(m):
        src = m.group(2)
        if src.startswith(("http:", "https:", "data:")):
            return m.group(0)
        f = task_dir / src
        if not f.exists():
            return f'{m.group(1)}src="{src}" data-pv-missing="1"'
        dark = f.with_name(f.stem + "_dark" + f.suffix)
        if inline:
            extra = f' data-pv-dark="{data_uri(dark)}" data-pv-light="{data_uri(f)}"' if dark.exists() else ""
            return f'{m.group(1)}src="{data_uri(f)}"{extra}'
        dst = out_dir / src
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dst)
        extra = ""
        if dark.exists():
            shutil.copy2(dark, dst.with_name(dark.name))
            extra = f' data-pv-dark="{os.path.dirname(src) + "/" if os.path.dirname(src) else ""}{dark.name}"'
        return f'{m.group(1)}src="{src}"{extra}'
    return re.sub(r'(<img\b[^>]*?)src="([^"]+)"', rep, h)


def kit_script(h, out_dir):
    rel = os.path.relpath(OUT / "lesson-kit" / "kit.js", out_dir)
    return re.sub(r'<script src="[^"]*lesson-kit/kit\.js"></script>', f'<script src="{rel}"></script>', h)


# ---------- код в редакторе глазами ученика ----------
def student_files(task):
    files = []
    for f in task["info"].get("files", []) or []:
        if not f.get("visible", True):
            continue
        path = task["dir"] / f["name"]
        if not path.exists() or path.suffix not in (".java", ".txt", ".json", ".kt", ".md"):
            continue
        text = path.read_text(encoding="utf-8")
        marks = []
        for p in sorted(f.get("placeholders") or [], key=lambda p: p["offset"]):
            if p["offset"] == "AUTO":
                continue
            marks.append((p["offset"], p["length"], p.get("placeholder_text", "")))
        out, pos = [], 0
        for off, ln, ph in marks:
            out.append(highlight_java(text[pos:off]))
            out.append(f'<span class="pv-ph" title="Здесь пишет ученик">{html.escape(ph)}</span>')
            pos = off + ln
        out.append(highlight_java(text[pos:]))
        files.append((f["name"], "".join(out)))
    return files


def choice_block(info):
    if info.get("type") != "choice":
        return ""
    multi = info.get("is_multiple_choice", False)
    kind = "checkbox" if multi else "radio"
    opts = "".join(
        f'<label class="pv-opt"><input type="{kind}" name="o" data-ok="{1 if o.get("is_correct") else 0}"> {html.escape(str(o["text"]))}</label>'
        for o in info.get("options", []))
    data = html.escape(json.dumps({"ok": info.get("message_correct", "Верно!"),
                                   "no": info.get("message_incorrect", "Неверно")}, ensure_ascii=False))
    header = html.escape(info.get("quiz_header") or ("Выбери все подходящие" if multi else "Выбери один ответ"))
    return (f'<div class="pv-choice" data-msg="{data}"><div class="pv-choice-h">{header}</div>{opts}'
            f'<div class="pv-bar"><button class="pv-check">Check</button><span class="pv-result"></span></div></div>')


PAGE = """<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<script>
(function(){{var q=new URLSearchParams(location.search),t=q.get('theme')||localStorage.getItem('pv-theme')||'light',w=q.get('w')||localStorage.getItem('pv-w')||'480';
localStorage.setItem('pv-theme',t);localStorage.setItem('pv-w',w);document.documentElement.className='pv-'+t;document.documentElement.style.setProperty('--pv-w',w+'px');}})();
</script>
<style>{css}</style></head>
<body>
<div class="pv-top"><a href="{index}">☰ Курс</a><span class="pv-crumbs">{crumbs}</span>
<span class="pv-right">{prev} {next}
<button onclick="pvSet('theme', document.documentElement.className=='pv-dark'?'light':'dark')">◐ Тема</button>
<select onchange="pvSet('w', this.value)">{widths}</select></span></div>
<div class="pv-panel">
<div class="pv-steps">{steps}</div>
<h1 class="pv-title">{icon} {name}</h1>
<div class="pv-content">
{content}
</div>
{choice}
{check}
</div>
{editor}
<script>
function pvSet(k,v){{var q=new URLSearchParams(location.search);q.set(k,v);localStorage.setItem('pv-'+k,v);location.search=q.toString();}}
(function(){{var dark=document.documentElement.className=='pv-dark';
document.querySelectorAll('img[data-pv-dark]').forEach(function(i){{if(dark)i.src=i.getAttribute('data-pv-dark');}});
document.querySelectorAll('.pv-right select option').forEach(function(o){{if(o.value==localStorage.getItem('pv-w'))o.selected=true;}});
var c=document.querySelector('.pv-choice');if(c){{var msg=JSON.parse(c.getAttribute('data-msg'));
c.querySelector('.pv-check').onclick=function(){{var ok=true;c.querySelectorAll('input').forEach(function(i){{if((i.checked?1:0)!=+i.getAttribute('data-ok'))ok=false;}});
var r=c.querySelector('.pv-result');r.textContent=ok?msg.ok:msg.no;r.className='pv-result '+(ok?'pv-ok':'pv-no');}};}}
}})();
</script>
</body></html>"""

CSS = """
html.pv-light{--bg:#F7F8FA;--fg:#000;--muted:#6C707E;--line:#DFE1E5;--code:#FFFFFF;--link:#2F5FD0;--kw:#0033B3;--str:#067D17;--num:#1750EB;--com:#8C8C8C;--fn:#00627A;--ph:#E8A33D;--top:#FFFFFF}
html.pv-dark{--bg:#2B2D30;--fg:#DFE1E5;--muted:#9DA0A8;--line:#393B40;--code:#1E1F22;--link:#548AF7;--kw:#CF8E6D;--str:#6AAB73;--num:#2AACB8;--com:#7A7E85;--fn:#56A8F5;--ph:#E8A33D;--top:#1E1F22}
body{margin:0;background:var(--bg);color:var(--fg);font:13px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI','Inter',sans-serif}
a{color:var(--link);text-decoration:none}a:hover{text-decoration:underline}
.pv-top{position:sticky;top:0;z-index:5;display:flex;gap:12px;align-items:center;flex-wrap:wrap;padding:8px 14px;background:var(--top);border-bottom:1px solid var(--line);font-size:12px}
.pv-crumbs{color:var(--muted)}.pv-right{margin-left:auto;display:flex;gap:8px;align-items:center}
.pv-top button,.pv-top select{font:inherit;background:var(--code);color:var(--fg);border:1px solid var(--line);border-radius:5px;padding:3px 8px}
.pv-panel{box-sizing:border-box;width:var(--pv-w);max-width:100%;margin:16px auto;padding:4px 16px 16px;border-left:1px solid var(--line);border-right:1px solid var(--line)}
.pv-title{font-size:1.45em;margin:.6em 0 .7em}
.pv-steps{display:flex;flex-wrap:wrap;gap:3px;margin-top:10px}
.pv-steps a{display:inline-block;width:22px;height:6px;border-radius:3px;background:var(--line)}
.pv-steps a.pv-cur{background:var(--link)}
img{display:block;max-width:100%;height:auto}
pre{white-space:pre-wrap}
table{border-collapse:collapse}td,th{border:1px solid var(--line);padding:.375em .8125em}
.pv-code{font-family:'JetBrains Mono',Menlo,Consolas,monospace;background:var(--code);font-size:12px;padding:2px 6px;margin:0 3px;border-radius:5px}
.pv-code-block{display:block;font-family:'JetBrains Mono',Menlo,Consolas,monospace;background:var(--code);font-size:12.5px;line-height:1.5;padding:8px 10px;border-radius:5px;white-space:pre-wrap}
.pv-kw{color:var(--kw)}.pv-str{color:var(--str)}.pv-num{color:var(--num)}.pv-com{color:var(--com);font-style:italic}.pv-fn{color:var(--fn)}
.pv-hint{margin:14px 0}.pv-hint summary{cursor:pointer;color:var(--fg)}.pv-hint-body{padding:2px 0 2px 20px}
.alert{position:relative;padding:.75rem 1.25rem;margin-bottom:1rem;border:1px solid transparent;border-radius:.375rem}
html.pv-light .alert-primary{background:#E6EEF7;border-color:#d2d8f9}html.pv-light .alert-warning{background:#F5F0E6;border-color:#E0CEA8}html.pv-light .alert-danger{background:#f5e6e7;border-color:#e0a8a9}
html.pv-dark .alert-primary{background:#25324D;border-color:#35528A}html.pv-dark .alert-warning{background:#3D3223;border-color:#7A5427}html.pv-dark .alert-danger{background:#402629;border-color:#7A3A40}
.pv-kbd{font:11px 'JetBrains Mono',Menlo,monospace;border:1px solid var(--line);border-bottom-width:2px;border-radius:4px;padding:0 4px;background:var(--code)}
.pv-kbd-alt{color:var(--muted);font-size:.9em}
.pv-psi{border-bottom:1px dotted var(--link)}
.pv-choice{margin:16px 0;padding:10px 12px;border:1px solid var(--line);border-radius:8px;background:var(--code)}
.pv-choice-h{font-weight:600;margin-bottom:6px}.pv-opt{display:block;padding:3px 0;cursor:pointer}
.pv-bar{display:flex;gap:10px;align-items:center;margin-top:10px}
.pv-bar button,.pv-check{background:#3574F0;color:#fff;border:0;border-radius:6px;padding:6px 16px;font:inherit;cursor:pointer}
.pv-result.pv-ok{color:#5FB865}.pv-result.pv-no{color:#F75464}
.pv-checkinfo{margin-top:18px;padding-top:10px;border-top:1px solid var(--line);color:var(--muted);font-size:12px}
.pv-editor{box-sizing:border-box;width:var(--pv-w);max-width:100%;margin:0 auto 40px}
.pv-file{margin:8px 0 16px}.pv-file-h{font-size:12px;color:var(--muted);margin-bottom:4px}
.pv-file pre{margin:0;background:var(--code);border:1px solid var(--line);border-radius:6px;padding:10px;font:12.5px/1.5 'JetBrains Mono',Menlo,Consolas,monospace;white-space:pre;overflow-x:auto}
.pv-ph{outline:1.5px solid var(--ph);background:rgba(232,163,61,.15);border-radius:3px}
[data-pv-missing]{outline:3px dashed #F75464}
.pv-index{max-width:760px;margin:20px auto;padding:0 16px}.pv-index h2{margin-top:1.4em}.pv-index li{margin:.2em 0}
"""


def render_step(t, out_dir, page_of, inline=False):
    md_path = t["dir"] / "task.md"
    src = md_path.read_text(encoding="utf-8") if md_path.exists() else "<p><i>Нет task.md</i></p>"
    h = md.render(src)
    h = cut_out_header(h)
    h = wrap_hints(h)
    h = highlight_code(h)
    h = shortcuts(h)
    h = rewrite_links(h, t["dir"], page_of)
    h = images(h, t["dir"], out_dir, inline)
    if inline:
        h = re.sub(r'<script src="[^"]*lesson-kit/kit\.js"></script>', "", h)
    else:
        h = kit_script(h, out_dir)
    return h


BUNDLE = """<!doctype html>
<html lang="ru" class="pv-light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>{css}
.pv-step{{box-sizing:border-box;width:var(--pv-w,480px);max-width:100%;margin:22px auto 0;padding:4px 16px 18px;border:1px solid var(--line);border-radius:10px;background:var(--bg)}}
.pv-stepno{{font-size:11px;color:var(--muted);margin-top:10px;letter-spacing:.06em;text-transform:uppercase}}
.pv-step details.pv-ed>summary{{cursor:pointer;color:var(--muted);font-size:12px;margin-top:14px}}
.pv-intro{{box-sizing:border-box;width:var(--pv-w,480px);max-width:100%;margin:18px auto 0;color:var(--muted);font-size:12.5px}}
body{{padding-bottom:60px}}
</style></head><body>
<div class="pv-top"><b>{title}</b><span class="pv-right">
<button id="pv-theme">◐ Тема</button>
<select id="pv-w"><option value="400">панель 400 px</option><option value="480" selected>панель 480 px</option><option value="600">панель 600 px</option></select></span></div>
<div class="pv-intro">Превью урока: так шаги выглядят в панели задания IntelliJ. Кнопки Check у вопросов работают,
интерактивные схемы — тоже. Код в редакторе — под каждым шагом («Редактор»).</div>
{steps}
<script>{kit}</script>
<script>
(function(){{
var root=document.documentElement;
function theme(t){{root.className='pv-'+t;root.setAttribute('data-k-theme',t);
document.querySelectorAll('img[data-pv-dark]').forEach(function(i){{i.src=i.getAttribute(t=='dark'?'data-pv-dark':'data-pv-light');}});}}
document.getElementById('pv-theme').onclick=function(){{theme(root.className=='pv-dark'?'light':'dark');}};
document.getElementById('pv-w').onchange=function(){{root.style.setProperty('--pv-w',this.value+'px');}};
document.querySelectorAll('.pv-choice').forEach(function(c){{var msg=JSON.parse(c.getAttribute('data-msg'));
c.querySelector('.pv-check').onclick=function(){{var ok=true;c.querySelectorAll('input').forEach(function(i){{if((i.checked?1:0)!=+i.getAttribute('data-ok'))ok=false;}});
var r=c.querySelector('.pv-result');r.textContent=ok?msg.ok:msg.no;r.className='pv-result '+(ok?'pv-ok':'pv-no');}};}});
if(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)theme('dark');
}})();
</script></body></html>"""


def bundle(lesson_rel):
    """Один самодостаточный HTML со всеми шагами урока: картинки и kit.js внутри."""
    course, tree = course_tree()
    target = (ROOT / lesson_rel).resolve()
    for sec in tree:
        for les in sec["lessons"]:
            if les["dir"].resolve() != target:
                continue
            page_of = {t["dir"].resolve(): OUT / "x" for t in les["tasks"]}
            parts = []
            for n, t in enumerate(les["tasks"], 1):
                h = render_step(t, OUT, page_of, inline=True)
                choice = choice_block(t["info"]).replace('name="o"', f'name="o{n}"')
                files = student_files(t)
                editor = ""
                if files:
                    editor = '<details class="pv-ed"><summary>Редактор (глазами ученика)</summary>' + "".join(
                        f'<div class="pv-file"><div class="pv-file-h">{html.escape(fn)}</div><pre>{c}</pre></div>'
                        for fn, c in files) + "</details>"
                parts.append(f'<section class="pv-step"><div class="pv-stepno">Шаг {n} из {len(les["tasks"])} · '
                             f'{TYPE_NAME.get(t["type"], t["type"])}</div>'
                             f'<h1 class="pv-title">{TYPE_ICON.get(t["type"], "")} {html.escape(t["name"])}</h1>'
                             f'<div class="pv-content">{h}</div>{choice}{editor}</section>')
            OUT.mkdir(parents=True, exist_ok=True)
            out = ROOT / "build" / f"lesson-{target.name}.html"
            out.write_text(BUNDLE.format(title=html.escape(les["name"]), css=CSS, steps="".join(parts),
                                         kit=(ROOT / "lesson-kit" / "kit.js").read_text(encoding="utf-8")
                                         .replace("</script", "<\\/script")),
                           encoding="utf-8")
            print(f"Готово: {out.relative_to(ROOT)}")
            return 0
    print(f"Урок {lesson_rel} не найден в course-info.yaml")
    return 1


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--bundle":
        return bundle(sys.argv[2])
    course, tree = course_tree()
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(ROOT / "lesson-kit", OUT / "lesson-kit")

    flat, page_of = [], {}
    for sec in tree:
        for les in sec["lessons"]:
            for t in les["tasks"]:
                page = OUT / t["dir"].relative_to(ROOT) / "index.html"
                page_of[t["dir"].resolve()] = page
                flat.append((sec, les, t, page))

    widths = "".join(f'<option value="{w}">{lab}</option>' for w, lab in
                     (("400", "панель 400 px"), ("480", "панель 480 px"), ("600", "панель 600 px"), ("800", "панель 800 px")))
    problems = []
    for i, (sec, les, t, page) in enumerate(flat):
        out_dir = page.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        h = render_step(t, out_dir, page_of)
        if "data-pv-missing" in h:
            problems.append(f"{t['dir'].relative_to(ROOT)}: картинка не найдена")
        steps = "".join(
            f'<a class="{"pv-cur" if tt is t else ""}" href="{os.path.relpath(page_of[tt["dir"].resolve()], out_dir)}" title="{html.escape(tt["name"])}"></a>'
            for tt in les["tasks"])
        prev_link = f'<a href="{os.path.relpath(flat[i-1][3], out_dir)}">← Назад</a>' if i > 0 else ""
        next_link = f'<a href="{os.path.relpath(flat[i+1][3], out_dir)}">Next →</a>' if i + 1 < len(flat) else ""
        editor = ""
        files = student_files(t)
        if files:
            editor = '<div class="pv-editor"><div class="pv-file-h">Редактор (глазами ученика)</div>' + "".join(
                f'<div class="pv-file"><div class="pv-file-h">{html.escape(n)}</div><pre>{c}</pre></div>' for n, c in files) + "</div>"
        check = ""
        if t["type"] in ("edu", "output"):
            check = '<div class="pv-checkinfo">В IDE здесь кнопка <b>Check</b>: она запустит тесты задачи.</div>'
        elif t["type"] == "ide":
            check = '<div class="pv-checkinfo">В IDE здесь кнопка <b>Check</b>: шаг засчитается после нажатия.</div>'
        page.write_text(PAGE.format(
            title=html.escape(t["name"]), css=CSS, index=os.path.relpath(OUT / "index.html", out_dir),
            crumbs=html.escape(f'{sec["name"]} › {les["name"]}'), prev=prev_link, next=next_link, widths=widths,
            steps=steps, icon=TYPE_ICON.get(t["type"], ""), name=html.escape(t["name"]), content=h,
            choice=choice_block(t["info"]), check=check, editor=editor), encoding="utf-8")

    # оглавление
    body = [f'<div class="pv-index"><h1>{html.escape(course.get("title", "Курс"))}</h1>'
            '<p>Превью шагов курса. Тема и ширина панели переключаются сверху на странице шага.</p>']
    for sec in tree:
        body.append(f"<h2>{html.escape(sec['name'])}</h2>")
        for les in sec["lessons"]:
            body.append(f"<h3>{html.escape(les['name'])}</h3><ol>")
            for t in les["tasks"]:
                rel = os.path.relpath(page_of[t["dir"].resolve()], OUT)
                body.append(f'<li>{TYPE_ICON.get(t["type"], "")} <a href="{rel}">{html.escape(t["name"])}</a> '
                            f'<span style="color:var(--muted)">· {TYPE_NAME.get(t["type"], t["type"])}</span></li>')
            body.append("</ol>")
    body.append("</div>")
    (OUT / "index.html").write_text(
        "<!doctype html><html lang='ru' class='pv-light'><head><meta charset='utf-8'><title>Превью курса</title>"
        f"<style>{CSS}</style></head><body>{''.join(body)}</body></html>", encoding="utf-8")

    print(f"Готово: {len(flat)} шагов → {OUT.relative_to(ROOT)}/index.html")
    for p in problems:
        print("  ⚠", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
