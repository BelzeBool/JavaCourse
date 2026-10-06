# Вопросы к строке: equals и другие

Игрок пишет в чат название предмета. Программе надо узнать: это алмазный меч? А вообще меч?
Ответ — «да» или «нет», то есть `boolean`: `true` или `false`. Для таких вопросов у строки тоже
есть методы.

## Совпадает целиком: equals

```java
String item = "diamond_sword";
System.out.println(item.equals("diamond_sword"));
System.out.println(item.equals("Diamond_Sword"));
System.out.println(item.equalsIgnoreCase("Diamond_Sword"));
```

<pre class="k-console">true
false
true</pre>

- `equals(текст)` — `true`, если строки совпадают **символ в символ**: каждая буква, регистр, пробелы.
- `equalsIgnoreCase(текст)` — то же, но заглавные и строчные буквы считаются одинаковыми.

## Совпадает часть

```java
boolean isSword = item.endsWith("_sword");
System.out.println("Меч: " + isSword);
System.out.println("Алмазный: " + item.startsWith("diamond"));
System.out.println("Железный: " + item.contains("iron"));
```

<pre class="k-console">Меч: true
Алмазный: true
Железный: false</pre>

- `startsWith(текст)` — начинается ли строка с этого текста;
- `endsWith(текст)` — заканчивается ли им;
- `contains(текст)` — есть ли такой кусок где-нибудь внутри.

Ответ можно сразу напечатать или положить в переменную типа `boolean` — как `isSword`.

<div class="k-trap">

**Ловушка: пробел и регистр.** Для `equals` строки `"diamond_sword"` и `" Diamond_Sword"` — разные:
лишний пробел, заглавные буквы. Сначала приведи строку в порядок, потом сравнивай:
`input.strip().toLowerCase().equals("diamond_sword")`.
</div>

<div class="k-key">

**Запомни.** Строки сравнивают методом `equals`. В уроке 1.5 появятся знаки сравнения для чисел —
для строк они работают не так, как кажется. Там и разберём почему. А ещё в 1.5 программа научится
по ответу `true` или `false` выбирать, что делать дальше.
</div>

## Попробуй

В редакторе оба примера. Поменяй `"diamond_sword"` в первой строке на `"iron_sword"`. Сначала
предскажи, какие ответы поменяются, потом запусти и проверь.

<script src="../../../lesson-kit/kit.js"></script>
