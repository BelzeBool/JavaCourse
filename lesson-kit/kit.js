/*
 * Набор компонентов для уроков курса (lesson kit).
 *
 * Подключается последней строкой task.md:
 *     <script src="../../../lesson-kit/kit.js"></script>
 *
 * Что делает:
 *  1. Определяет тему IDE (светлая/тёмная) по цвету фона панели и ставит <html data-k-theme="...">.
 *  2. Добавляет стили для компонентов k-* (см. docs/lesson-design.md, раздел «Компоненты»).
 *  3. «Оживляет» интерактивные компоненты: пошаговую трассировку (k-trace), разбор строки (k-anatomy),
 *     сундуки-переменные (k-vars), подсветку кода (k-code).
 *
 * Главное правило: без этого скрипта (старый Swing-рендер, ошибка загрузки) любой компонент
 * остаётся обычным читаемым HTML — кодом, таблицей, абзацем. Скрипт только улучшает вид.
 */
(function () {
  "use strict";
  if (window.__kitLoaded) return;
  window.__kitLoaded = true;

  // ---------- 1. Тема ----------
  function parseRgb(s) {
    var m = /rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)/.exec(s || "");
    if (!m) return null;
    if (m[4] !== undefined && +m[4] === 0) return null; // прозрачный — не считается
    return [+m[1], +m[2], +m[3]];
  }
  function detectTheme() {
    var els = [document.body, document.documentElement];
    for (var i = 0; i < els.length; i++) {
      if (!els[i]) continue;
      var rgb = parseRgb(getComputedStyle(els[i]).backgroundColor);
      if (rgb) {
        var lum = (0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]) / 255;
        return lum < 0.5 ? "dark" : "light";
      }
    }
    // фон не задан — смотрим на цвет текста: светлый текст значит тёмную тему
    var fg = parseRgb(getComputedStyle(document.body).color);
    if (fg && (fg[0] + fg[1] + fg[2]) / 3 > 140) return "dark";
    return "light";
  }

  // ---------- 2. Стили ----------
  var CSS = [
    ":root[data-k-theme=light]{--k-type:#2F62C8;--k-name:#B5530F;--k-value:#2E7A1F;--k-err:#C2303F;--k-mod:#7A45B5;",
    "--k-line:rgba(0,0,0,.13);--k-soft:rgba(0,0,0,.035);--k-softer:rgba(0,0,0,.06);--k-muted:#646B7A;",
    "--k-key-bg:#E8F0FD;--k-key-line:#9DB8EE;--k-trap-bg:#FDF1E3;--k-trap-line:#E7B57D;--k-mod-bg:#F2EAFB;--k-mod-line:#C3A5E6;",
    "--k-err-bg:#FCEBED;--k-ok:#2E7A1F;--k-ok-bg:#E7F3E1;--k-hl:#FFF3C4;--k-hl-line:#E8B93A;",
    "--k-con-bg:#1E1F22;--k-con-fg:#DFE1E5;--k-con-dim:#7A7E85;",
    "--k-code-bg:#FFFFFF;--k-c-kw:#0033B3;--k-c-str:#067D17;--k-c-num:#1750EB;--k-c-com:#8C8C8C;--k-c-fn:#00627A;--k-c-txt:#080808;}",

    ":root[data-k-theme=dark]{--k-type:#7AA2F7;--k-name:#F0A35E;--k-value:#8BCB6A;--k-err:#F2737F;--k-mod:#C29BF0;",
    "--k-line:rgba(255,255,255,.15);--k-soft:rgba(255,255,255,.035);--k-softer:rgba(255,255,255,.07);--k-muted:#9DA0A8;",
    "--k-key-bg:#1D2A44;--k-key-line:#35528A;--k-trap-bg:#3A2A17;--k-trap-line:#7A5427;--k-mod-bg:#2E2340;--k-mod-line:#5E447F;",
    "--k-err-bg:#3B1C20;--k-ok:#8BCB6A;--k-ok-bg:#1F3319;--k-hl:#3D3520;--k-hl-line:#B8912D;",
    "--k-con-bg:#141517;--k-con-fg:#DFE1E5;--k-con-dim:#6F737A;",
    "--k-code-bg:#1E1F22;--k-c-kw:#CF8E6D;--k-c-str:#6AAB73;--k-c-num:#2AACB8;--k-c-com:#7A7E85;--k-c-fn:#56A8F5;--k-c-txt:#BCBEC4;}",

    // общие
    ".k-label{font-size:.72em;letter-spacing:.08em;text-transform:uppercase;font-weight:700;color:var(--k-muted)}",
    ".k-mono,.k-code,.k-console,.k-anatomy,.k-var-value,.k-trace pre{font-family:'JetBrains Mono',Menlo,Consolas,monospace}",

    // плашки
    ".k-key,.k-trap,.k-mod,.k-ru,.k-recap{border-radius:8px;padding:.6em .9em;margin:1em 0;border:1px solid var(--k-line)}",
    ".k-key{background:var(--k-key-bg);border-color:var(--k-key-line)}",
    ".k-trap{background:var(--k-trap-bg);border-color:var(--k-trap-line)}",
    ".k-mod{background:var(--k-mod-bg);border-color:var(--k-mod-line)}",
    ".k-key>p:first-child,.k-trap>p:first-child,.k-mod>p:first-child,.k-ru>p:first-child{margin-top:0}",
    ".k-key>p:last-child,.k-trap>p:last-child,.k-mod>p:last-child,.k-ru>p:last-child{margin-bottom:0}",
    ".k-ru{border-style:dashed;background:transparent}",
    ".k-ru::before{content:'По-русски';display:block;margin-bottom:.3em;font-size:.72em;letter-spacing:.08em;text-transform:uppercase;font-weight:700;color:var(--k-name)}",

    // консоль
    ".k-console{background:var(--k-con-bg);color:var(--k-con-fg);border-radius:8px;padding:.7em .9em;margin:.8em 0;white-space:pre-wrap;line-height:1.45;font-size:.93em}",
    ".k-console:empty::before{content:'(пока пусто)';color:var(--k-con-dim)}",

    // подсвеченный код внутри компонентов
    ".k-code{background:var(--k-code-bg);color:var(--k-c-txt);border:1px solid var(--k-line);border-radius:8px;padding:.6em .8em;margin:.6em 0;white-space:pre;overflow-x:auto;line-height:1.5;font-size:.93em}",
    ".k-c-kw{color:var(--k-c-kw);font-weight:600}.k-c-str{color:var(--k-c-str)}.k-c-num{color:var(--k-c-num)}.k-c-com{color:var(--k-c-com);font-style:italic}.k-c-fn{color:var(--k-c-fn)}",

    // разбор строки
    ".k-anatomy{display:flex;flex-wrap:wrap;align-items:flex-start;gap:.15em .1em;font-size:1.15em;margin:1em 0;padding:.9em 1em .6em;border:1px solid var(--k-line);border-radius:8px;background:var(--k-soft)}",
    ".k-anatomy>span{display:inline-flex;flex-direction:column;align-items:center;padding:.1em .25em;border-radius:5px;white-space:pre}",
    ".k-anatomy>span[data-label]::after{content:attr(data-label);font-family:-apple-system,'Segoe UI',sans-serif;font-size:.58em;margin-top:.35em;padding-top:.2em;border-top:2px solid currentColor;color:var(--k-muted);white-space:nowrap}",
    ".k-anatomy>span.t-type{color:var(--k-type)}.k-anatomy>span.t-name{color:var(--k-name)}.k-anatomy>span.t-value{color:var(--k-value)}.k-anatomy>span.t-err{color:var(--k-err)}",
    ".k-anatomy>span[data-explain]{cursor:pointer}.k-anatomy>span[data-explain]:hover,.k-anatomy>span.k-on{background:var(--k-softer)}",
    ".k-anatomy-explain{flex-basis:100%;font-family:-apple-system,'Segoe UI',sans-serif;font-size:.8em;margin-top:.5em;min-height:1.4em;color:inherit}",
    ".k-anatomy-explain:empty::before{content:'Нажми на любую часть строки — появится пояснение.';color:var(--k-muted)}",

    // сундуки-переменные
    ".k-vars{display:flex;flex-wrap:wrap;gap:.8em;margin:1em 0}",
    ".k-var{position:relative;min-width:7.5em;border:2px solid var(--k-line);border-radius:8px;background:var(--k-soft);padding:1.35em .7em .55em;text-align:center}",
    ".k-var-type{position:absolute;top:-.75em;left:.6em;font:700 .75em 'JetBrains Mono',Menlo,Consolas,monospace;color:var(--k-type);background:var(--k-key-bg);border:1px solid var(--k-key-line);border-radius:5px;padding:.05em .4em}",
    ".k-var-name{display:block;font:600 .85em 'JetBrains Mono',Menlo,Consolas,monospace;color:var(--k-name);margin-bottom:.25em}",
    ".k-var-value{display:block;font-size:1.15em;font-weight:700;color:var(--k-value);min-height:1.3em}",
    ".k-var.k-new{border-style:dashed}",
    ".k-var.k-changed{border-color:var(--k-hl-line);background:var(--k-hl)}",
    ".k-var.k-empty .k-var-value{color:var(--k-muted);font-weight:400}",

    // трассировка
    ".k-trace{border:1px solid var(--k-line);border-radius:10px;margin:1.2em 0;padding:.8em .9em;background:var(--k-soft)}",
    ".k-trace-title{font-weight:700;margin-bottom:.5em}",
    ".k-trace-title .k-label{margin-right:.6em;color:var(--k-name)}",
    ".k-trace-code{background:var(--k-code-bg);border:1px solid var(--k-line);border-radius:8px;padding:.5em 0;margin:0 0 .7em;overflow-x:auto;font-family:'JetBrains Mono',Menlo,Consolas,monospace;font-size:.93em;line-height:1.55}",
    ".k-trace-line{display:block;white-space:pre;padding:0 .8em 0 .4em;color:var(--k-c-txt);border-left:3px solid transparent}",
    ".k-trace-line .k-ln{display:inline-block;width:2em;text-align:right;margin-right:.9em;color:var(--k-muted);user-select:none}",
    ".k-trace-line.k-cur{background:var(--k-hl);border-left-color:var(--k-hl-line)}",
    ".k-trace-line.k-done{opacity:.75}",
    ".k-trace-bar{display:flex;flex-wrap:wrap;align-items:center;gap:.5em;margin:.4em 0 .7em}",
    ".k-btn{font:inherit;font-size:.9em;padding:.35em .9em;border-radius:6px;border:1px solid var(--k-line);background:var(--k-code-bg);color:inherit;cursor:pointer}",
    ".k-btn:hover{background:var(--k-softer)}.k-btn:disabled{opacity:.45;cursor:default}",
    ".k-btn.k-primary{background:var(--k-type);border-color:var(--k-type);color:#fff}",
    ".k-trace-step{font-size:.85em;color:var(--k-muted);margin-left:auto}",
    ".k-trace-explain{margin:.2em 0 .7em;padding:.5em .7em;border-left:3px solid var(--k-name);background:var(--k-code-bg);border-radius:0 6px 6px 0;min-height:1.5em}",
    ".k-trace-cols{display:flex;flex-wrap:wrap;gap:.8em;align-items:flex-start}",
    ".k-trace-cols>div{flex:1 1 14em}",
    ".k-trace .k-vars{margin:.5em 0}",
    ".k-trace .k-console{margin:.5em 0;min-height:2.6em}",

    // ошибка компилятора
    ".k-error{border:1px solid var(--k-line);border-left:4px solid var(--k-err);border-radius:8px;padding:.6em .9em;margin:1em 0;background:var(--k-soft)}",
    ".k-error>pre{margin:.3em 0;white-space:pre-wrap}",
    ".k-error>pre.k-msg{color:var(--k-err);font-family:'JetBrains Mono',Menlo,Consolas,monospace;font-size:.9em;background:var(--k-err-bg);border-radius:6px;padding:.4em .6em}",
    ".k-error>p{margin:.4em 0}",

    // сравнение
    ".k-compare{display:flex;flex-wrap:wrap;gap:.8em;margin:1em 0}",
    ".k-compare>div{flex:1 1 13em;border:1px solid var(--k-line);border-radius:8px;padding:.5em .8em;background:var(--k-soft)}",
    ".k-compare>.k-good{border-top:4px solid var(--k-ok)}.k-compare>.k-bad{border-top:4px solid var(--k-err)}",
    ".k-compare>.k-good::before{content:'✓ Так';display:block;font-weight:700;color:var(--k-ok);margin-bottom:.2em}",
    ".k-compare>.k-bad::before{content:'✗ Не так';display:block;font-weight:700;color:var(--k-err);margin-bottom:.2em}",
    ".k-compare>div>p:first-of-type{margin-top:.2em}",

    // итог урока
    ".k-recap{background:var(--k-ok-bg);border-color:var(--k-ok)}",
    ".k-recap::before{content:'Итог';display:block;font-size:.72em;letter-spacing:.08em;text-transform:uppercase;font-weight:700;color:var(--k-ok);margin-bottom:.3em}",
    ".k-recap ul{margin:.2em 0;padding-left:1.3em}.k-recap li{margin:.25em 0}",

    // «проверь себя»: вопрос с ответом под катом (<details class="k-self">)
    "details.k-self{border:1px solid var(--k-line);border-radius:8px;margin:.6em 0;padding:.45em .8em;background:var(--k-soft)}",
    "details.k-self>summary{cursor:pointer;font-weight:600}",
    "details.k-self[open]>summary{margin-bottom:.4em}",
    "details.k-self>p:last-child{margin-bottom:.2em}",

    // термин
    ".k-term{border-bottom:1px dashed currentColor;cursor:help}",

    // «ты здесь»: путь по уроку
    ".k-path{display:flex;flex-wrap:wrap;gap:.3em;margin:0 0 1em;font-size:.8em}",
    ".k-path>span{padding:.15em .55em;border-radius:999px;border:1px solid var(--k-line);color:var(--k-muted)}",
    ".k-path>span.k-here{border-color:var(--k-name);color:var(--k-name);font-weight:700}",
    ".k-path>span.k-was{color:inherit}"
  ].join("\n");

  function injectCss() {
    if (document.getElementById("k-style")) return;
    var st = document.createElement("style");
    st.id = "k-style";
    st.textContent = CSS;
    (document.head || document.documentElement).appendChild(st);
  }

  // ---------- 3. Подсветка Java ----------
  var KW = /^(abstract|boolean|break|byte|case|catch|char|class|continue|default|do|double|else|enum|extends|final|finally|float|for|if|implements|import|instanceof|int|interface|long|new|package|private|protected|public|record|return|short|static|super|switch|this|throw|throws|try|var|void|while|true|false|null)$/;
  function esc(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function highlight(line) {
    var re = /(\/\/.*$)|("(?:\\.|[^"\\])*"?)|('(?:\\.|[^'\\])*'?)|(\b\d+(?:\.\d+)?[LlFfDd]?\b)|([A-Za-z_]\w*)(?=\s*\()|([A-Za-z_]\w*)|([\s\S])/g;
    var out = "", m;
    while ((m = re.exec(line)) !== null) {
      if (m[1]) out += '<span class="k-c-com">' + esc(m[1]) + "</span>";
      else if (m[2] || m[3]) out += '<span class="k-c-str">' + esc(m[2] || m[3]) + "</span>";
      else if (m[4]) out += '<span class="k-c-num">' + esc(m[4]) + "</span>";
      else if (m[5]) out += KW.test(m[5]) ? '<span class="k-c-kw">' + esc(m[5]) + "</span>" : '<span class="k-c-fn">' + esc(m[5]) + "</span>";
      else if (m[6]) out += KW.test(m[6]) ? '<span class="k-c-kw">' + esc(m[6]) + "</span>" : esc(m[6]);
      else out += esc(m[7]);
    }
    return out;
  }
  function codeLines(pre) {
    var text = pre.textContent.replace(/\r/g, "").replace(/^\n/, "").replace(/\n\s*$/, "");
    return text.split("\n");
  }
  function upgradeCode(pre) {
    if (pre.__k) return;
    pre.__k = true;
    pre.innerHTML = codeLines(pre).map(highlight).join("\n");
  }

  // ---------- 4. Сундуки-переменные ----------
  // <div class="k-vars">int diamonds = 5; boolean isNight = false; double health</div>
  function parseVars(text) {
    return text.split(";").map(function (part) {
      part = part.trim();
      if (!part) return null;
      var m = /^(\S+)\s+([A-Za-z_]\w*)\s*(?:=\s*([\s\S]*))?$/.exec(part);
      if (!m) return null;
      return { type: m[1], name: m[2], value: m[3] === undefined ? null : m[3].trim() };
    }).filter(Boolean);
  }
  function varBox(v, cls) {
    var d = document.createElement("div");
    d.className = "k-var" + (v.value === null ? " k-empty" : "") + (cls ? " " + cls : "");
    d.innerHTML = (v.type ? '<span class="k-var-type">' + esc(v.type) + "</span>" : "") +
      '<span class="k-var-name">' + esc(v.name) + "</span>" +
      '<span class="k-var-value">' + (v.value === null ? "пусто" : esc(v.value)) + "</span>";
    return d;
  }
  function upgradeVars(el) {
    if (el.__k) return;
    el.__k = true;
    var vars = parseVars(el.textContent);
    if (!vars.length) return;
    el.textContent = "";
    vars.forEach(function (v) { el.appendChild(varBox(v)); });
  }

  // ---------- 5. Разбор строки ----------
  function upgradeAnatomy(el) {
    if (el.__k) return;
    el.__k = true;
    var parts = el.querySelectorAll("span[data-explain]");
    if (!parts.length) return;
    var box = document.createElement("div");
    box.className = "k-anatomy-explain";
    el.appendChild(box);
    Array.prototype.forEach.call(parts, function (p) {
      p.addEventListener("click", function () {
        Array.prototype.forEach.call(parts, function (q) { q.classList.remove("k-on"); });
        p.classList.add("k-on");
        box.innerHTML = p.getAttribute("data-explain");
      });
    });
  }

  // ---------- 6. Пошаговая трассировка ----------
  // Разметка: <div class="k-trace" data-title="..."><pre>код</pre><table>…</table></div>
  // Первая колонка таблицы — номер строки кода. Предпоследняя — «Экран» (что напечатано на этом шаге),
  // последняя — пояснение. Колонки между ними — переменные; в заголовке можно указать тип: «int diamonds».
  // Пустая ячейка переменной — «такой переменной ещё нет».
  function cellText(td) { return td ? td.textContent.trim() : ""; }
  function upgradeTrace(el) {
    if (el.__k) return;
    var pre = el.querySelector("pre"), table = el.querySelector("table");
    if (!pre || !table) return;
    var rows = Array.prototype.slice.call(table.querySelectorAll("tr"));
    if (rows.length < 2) return;
    var head = Array.prototype.slice.call(rows[0].children).map(cellText);
    if (head.length < 3) return;
    var varCols = head.slice(1, head.length - 2).map(function (h) {
      var m = /^(\S+)\s+(\S+)$/.exec(h);
      return m ? { type: m[1], name: m[2] } : { type: "", name: h };
    });
    var steps = rows.slice(1).map(function (tr) {
      var tds = Array.prototype.slice.call(tr.children);
      return {
        line: parseInt(cellText(tds[0]), 10),
        vars: varCols.map(function (_, i) { var t = cellText(tds[1 + i]); return t === "" ? null : t; }),
        out: tds[head.length - 2] ? tds[head.length - 2].textContent.replace(/^\n+|\s+$/g, "") : "",
        // <td data-print> — шаг печатает через print: перевода строки после текста нет
        newline: !(tds[head.length - 2] && tds[head.length - 2].hasAttribute("data-print")),
        explain: tds[head.length - 1] ? tds[head.length - 1].innerHTML : ""
      };
    });
    el.__k = true;
    var lines = codeLines(pre);
    var title = el.getAttribute("data-title") || "Выполняем по шагам";

    el.innerHTML = "";
    var t = document.createElement("div");
    t.className = "k-trace-title";
    t.innerHTML = '<span class="k-label">Интерактив</span>' + esc(title);
    var code = document.createElement("div");
    code.className = "k-trace-code";
    code.innerHTML = lines.map(function (l, i) {
      return '<span class="k-trace-line" data-n="' + (i + 1) + '"><span class="k-ln">' + (i + 1) + "</span>" + highlight(l) + "</span>";
    }).join("");
    var bar = document.createElement("div");
    bar.className = "k-trace-bar";
    bar.innerHTML = '<button class="k-btn" data-a="prev">← Назад</button>' +
      '<button class="k-btn k-primary" data-a="next">Дальше →</button>' +
      '<button class="k-btn" data-a="reset">Сначала</button><span class="k-trace-step"></span>';
    var explain = document.createElement("div");
    explain.className = "k-trace-explain";
    var cols = document.createElement("div");
    cols.className = "k-trace-cols";
    cols.innerHTML = '<div><div class="k-label">Сундуки (переменные)</div><div class="k-vars"></div></div>' +
      '<div><div class="k-label">Экран программы</div><pre class="k-console"></pre></div>';
    [t, code, bar, explain, cols].forEach(function (n) { el.appendChild(n); });

    var varsEl = cols.querySelector(".k-vars"), conEl = cols.querySelector(".k-console");
    var stepEl = bar.querySelector(".k-trace-step");
    var cur = -1; // -1 — до запуска

    function render() {
      Array.prototype.forEach.call(code.children, function (ln) {
        var n = +ln.getAttribute("data-n");
        ln.classList.toggle("k-cur", cur >= 0 && steps[cur].line === n);
      });
      varsEl.innerHTML = "";
      var prev = cur > 0 ? steps[cur - 1].vars : varCols.map(function () { return null; });
      var shown = 0;
      varCols.forEach(function (vc, i) {
        var val = cur >= 0 ? steps[cur].vars[i] : null;
        if (val === null) return;
        shown++;
        var cls = prev[i] === null ? "k-new k-changed" : (prev[i] !== val ? "k-changed" : "");
        varsEl.appendChild(varBox({ type: vc.type, name: vc.name, value: val }, cls));
      });
      if (!shown) varsEl.innerHTML = '<span class="k-label" style="text-transform:none;letter-spacing:0;font-weight:400">пока ни одной</span>';
      var out = "";
      for (var k = 0; k <= cur; k++) {
        if (steps[k].out || !steps[k].newline) out += steps[k].out + (steps[k].newline ? "\n" : "");
      }
      conEl.textContent = out.replace(/\n$/, "");
      explain.innerHTML = cur < 0 ? "Нажми «Дальше», чтобы выполнить первую строку." : steps[cur].explain;
      stepEl.textContent = cur < 0 ? "Шагов: " + steps.length : "Шаг " + (cur + 1) + " из " + steps.length;
      bar.querySelector('[data-a="prev"]').disabled = cur < 0;
      bar.querySelector('[data-a="next"]').disabled = cur >= steps.length - 1;
    }
    bar.addEventListener("click", function (e) {
      var a = e.target && e.target.getAttribute && e.target.getAttribute("data-a");
      if (a === "next" && cur < steps.length - 1) cur++;
      if (a === "prev" && cur >= 0) cur--;
      if (a === "reset") cur = -1;
      render();
    });
    render();
  }

  // ---------- 7. Запуск ----------
  function each(sel, fn) { Array.prototype.forEach.call(document.querySelectorAll(sel), fn); }
  function init() {
    document.documentElement.setAttribute("data-k-theme", detectTheme());
    injectCss();
    each("pre.k-code", upgradeCode);
    each(".k-error > pre:not(.k-msg)", function (p) { p.classList.add("k-code"); upgradeCode(p); });
    each(".k-vars", upgradeVars);
    each(".k-anatomy", upgradeAnatomy);
    each(".k-trace", upgradeTrace);
  }
  window.lessonKit = { init: init, highlight: highlight };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
