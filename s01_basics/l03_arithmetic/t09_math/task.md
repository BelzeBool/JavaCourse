# Готовые формулы: Math

Корень, степень, «большее из двух» — считать такое знаками `+ - * /` долго и неудобно. В Java для
этого есть готовый набор формул — [Math](psi_element://java.lang.Math). Подключать его не нужно:
он всегда под рукой.

Формулу зовут как `println`: имя, а в скобках — числа для неё. Если чисел два — через запятую.

```java
System.out.println(Math.max(17, 20));
System.out.println(Math.min(80, 64));
System.out.println(Math.abs(-160));
System.out.println(Math.round(8.5));
System.out.println(Math.sqrt(16));
System.out.println(Math.pow(2, 10));
```

<pre class="k-console">20
64
160
9
4.0
1024.0</pre>

- `Math.max(a, b)` — большее из двух чисел.
- `Math.min(a, b)` — меньшее. `Math.min(80, 64)` — сколько из 80 блоков влезет в один слот.
- `Math.abs(x)` — число без минуса. Расстояние не бывает отрицательным: `Math.abs(-160)` — это 160 блоков.
- `Math.round(x)` — округлить до целого, от .5 — вверх.
- `Math.sqrt(x)` — квадратный корень: какое число, умноженное само на себя, даёт x.
- `Math.pow(a, b)` — a в степени b: `Math.pow(2, 10)` — это 2 * 2 * … * 2, десять двоек.

Как такие формулы устроены внутри и как написать свою — в уроке 1.7.

<div class="k-trap">

**Ловушка: тип результата.** `sqrt` и `pow` всегда дают `double` — поэтому `4.0`, а не `4`.
А `round` даёт `long`, и в сундук `int` его просто так не положить.
</div>

<div class="k-error">
<pre>int distance = Math.round(240.8);</pre>
<pre class="k-msg">error: incompatible types: possible lossy conversion from long to int</pre>
<p><b>Перевод:</b> «при переводе из long в int часть числа может потеряться». <code>round</code> вернул <code>long</code>, а сундук — <code>int</code>.</p>
<p><b>Как чинить:</b> взять сундук <code>long</code> — <code>long distance = Math.round(240.8);</code> — или привести тип: <code>(int) Math.round(240.8)</code>.</p>
</div>

## Попробуй

В редакторе все примеры. Допиши строку: сколько блоков в кубе 5 × 5 × 5? Посчитай через
`Math.pow(5, 3)` и запусти. Почему вышло `125.0`, а не `125`?

<script src="../../../lesson-kit/kit.js"></script>
