# Задача: почини сундуки

Стив ставит факелы на ночь. В программе **три ошибки** — по одной из каждого шага этого урока.
Почини их так, чтобы программа напечатала:

<pre class="k-console">Факелов: 32
Ночь: true</pre>

Тексты в кавычках не меняй. Факелов сначала 64, потом их становится 32 — эти две строки
оставь, только почини.

Порядок работы как в уроке 1.1: нажми **Check**, прочитай первую ошибку, почини, повтори.

<div class="hint" title="Подсказка к первой ошибке">

`variable torches is already defined` — переменную объявили дважды. Во второй раз тип не нужен.
</div>

<div class="hint" title="Подсказка ко второй ошибке">

`incompatible types: String cannot be converted to boolean` — в сундук для «да/нет» положили текст.
Какие два значения бывают у `boolean`?
</div>

<div class="hint" title="Подсказка к третьей ошибке">

`cannot find symbol` — такого имени нет. Сравни имя в печати с объявлением буква в букву.
</div>

<div class="hint" title="Решение целиком">

```java
int torches = 64;
torches = 32;
boolean isNight = true;
System.out.println("Факелов: " + torches);
System.out.println("Ночь: " + isNight);
```
</div>

<script src="../../../lesson-kit/kit.js"></script>
