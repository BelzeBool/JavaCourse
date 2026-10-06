# Задача: ID предмета

В моде постоянно приходится разбирать ID: из какого мода предмет и как он называется.
Напиши такой разбор.

## Условие

ID уже лежит в переменной `id`. Разрежи его по двоеточию и напечатай обе части:

<pre class="k-console">Пространство имён: minecraft
Путь: diamond_sword</pre>

Проверка смотрит и на код:

- номер двоеточия найди методом `indexOf` — чисел 9 и 10 в коде быть не должно;
- части вырежи из `id` методом `substring` — тексты `minecraft` и `diamond_sword` встречаются
  в коде только один раз, в самом `id`.

<div class="hint" title="С чего начать">

Сначала найди двоеточие и положи его номер в переменную: `int colon = id.indexOf(":");`
Потом вырежи части — как в примере на прошлом шаге.
</div>

<div class="hint" title="В ответ попало двоеточие">

`minecraft:` — значит, вырезано на клетку больше. Второй номер в `substring(от, до)` в кусок
не входит, поэтому пиши `substring(0, colon)`.

`:diamond_sword` — путь начался с самого двоеточия. Начни на клетку позже: `substring(colon + 1)`.
</div>

<div class="hint" title="Решение целиком">

```java
int colon = id.indexOf(":");
String namespace = id.substring(0, colon);
String path = id.substring(colon + 1);
System.out.println("Пространство имён: " + namespace);
System.out.println("Путь: " + path);
```
</div>

## Попробуй после Check

Поменяй ID на `ruby_mod:ruby` и запусти. Должно напечататься `ruby_mod` и `ruby` — без других правок.

<script src="../../../lesson-kit/kit.js"></script>
