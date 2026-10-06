# Задача: почини генератор ID

Алекс делает мод. Программа берёт название предмета, которое видит игрок, и собирает из него
ID и ключ перевода. В ID Minecraft разрешены только строчные латинские буквы, цифры и знаки
`_ - . /` — пробел или заглавная буква сломают мод.

В программе **три ошибки** — из разных шагов этого урока. Почини их так, чтобы программа
напечатала:

<pre class="k-console">ID: ruby_mod:ruby_sword
Ключ перевода: item.ruby_mod.ruby_sword
Проверка: true</pre>

Название `" Ruby Sword "` не меняй — пробелы по краям и заглавные буквы должна убрать программа.
Последнюю строку тоже не трогай: она сама сверяет ID с образцом и напечатает `true`, когда всё
починено.

Порядок работы как в уроке 1.1: нажми **Check**, прочитай первую ошибку, почини, повтори.

<div class="hint" title="Ошибка cannot find symbol">

`symbol: variable toLowerCase` — Java ищет переменную, а это метод. Чего не хватает у метода?
</div>

<div class="hint" title="Вместо подчёркиваний — пробелы">

`replace` сначала принимает то, **что искать**, потом — **на что менять**. Сейчас наоборот.
</div>

<div class="hint" title="Подчёркивания по краям: _ruby_sword_">

Пробелы по краям никуда не делись. `strip()` вызван, но его результат пропал — строка
не меняется, метод делает новую. Куда её положить?
</div>

<div class="hint" title="Решение целиком">

```java
String modId = "ruby_mod";
String title = " Ruby Sword ";
title = title.strip();
String path = title.toLowerCase();
path = path.replace(" ", "_");
String id = modId + ":" + path;
System.out.println("ID: " + id);
System.out.println("Ключ перевода: item." + modId + "." + path);
System.out.println("Проверка: " + id.equals("ruby_mod:ruby_sword"));
```
</div>

<div class="k-mod">

**В моде пригодится.** Ключ перевода `item.ruby_mod.ruby_sword` — настоящий: по нему Minecraft
ищет название предмета в файлах перевода `en_us.json` и `ru_ru.json`. Их ты заполнишь в главе 4.
</div>

<script src="../../../lesson-kit/kit.js"></script>
