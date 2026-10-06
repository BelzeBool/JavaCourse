package course;

import org.junit.jupiter.api.Assertions;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Помощники для тестов курса. Ученику этот файл не показывается.
 * Все сообщения об ошибках — на русском и с подсказкой, где именно расхождение.
 */
public final class Check {
    private Check() {
    }

    /** Запускает main ученика и возвращает всё, что он напечатал. */
    public static String runMain(ThrowingRunnable main) {
        PrintStream original = System.out;
        ByteArrayOutputStream buffer = new ByteArrayOutputStream();
        System.setOut(new PrintStream(buffer, true, StandardCharsets.UTF_8));
        try {
            main.run();
        } catch (Throwable e) {
            System.setOut(original);
            Assertions.fail("Программа упала с ошибкой: " + e
                    + "\nЗапусти программу (зелёный треугольник рядом с main) и посмотри, что случилось.");
        } finally {
            System.setOut(original);
        }
        return buffer.toString(StandardCharsets.UTF_8);
    }

    /**
     * Сравнивает вывод построчно. Пробелы в конце строк и пустые строки в самом конце не считаются.
     * При ошибке показывает номер первой отличающейся строки и оба варианта целиком.
     */
    public static void assertOutput(String expected, String actual) {
        List<String> exp = lines(expected);
        List<String> act = lines(actual);
        if (exp.equals(act)) {
            return;
        }
        StringBuilder msg = new StringBuilder();
        if (act.isEmpty()) {
            msg.append("Программа ничего не напечатала.");
        } else {
            int n = Math.max(exp.size(), act.size());
            for (int i = 0; i < n; i++) {
                String e = i < exp.size() ? exp.get(i) : null;
                String a = i < act.size() ? act.get(i) : null;
                if (e == null) {
                    msg.append("Лишняя строка ").append(i + 1).append(": «").append(a).append("»");
                    break;
                }
                if (a == null) {
                    msg.append("Не хватает строки ").append(i + 1).append(": «").append(e).append("»");
                    break;
                }
                if (!e.equals(a)) {
                    msg.append("Строка ").append(i + 1).append(" отличается.")
                            .append("\n  ждём:     «").append(e).append("»")
                            .append("\n  получили: «").append(a).append("»")
                            .append("\n  ").append(whereDiffers(e, a));
                    break;
                }
            }
        }
        msg.append("\n\nОжидаемый вывод:\n").append(String.join("\n", exp))
                .append("\n\nТвой вывод:\n").append(act.isEmpty() ? "(пусто)" : String.join("\n", act));
        Assertions.fail(msg.toString());
    }

    /** Читает исходник ученика, например "src/Main.java". */
    public static String source(String path) {
        try {
            return Files.readString(Path.of(path), StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new IllegalStateException("Не нашёл файл " + path, e);
        }
    }

    /**
     * Исходник без комментариев — чтобы закомментированный код не засчитывался.
     * Комментарии заменяются пробелами, переводы строк сохраняются: номера строк остаются верными.
     * Содержимое строк в кавычках не трогается.
     */
    public static String sourceWithoutComments(String path) {
        return blank(source(path), false);
    }

    /** Исходник без комментариев и без содержимого строк: "Алмазов: 5" → "          ". Номера строк сохраняются. */
    public static String sourceWithoutStrings(String path) {
        return blank(source(path), true);
    }

    /** Код ученика по умолчанию — src/Main.java без комментариев. */
    public static String code() {
        return sourceWithoutComments("src/Main.java");
    }

    /** Номер строки (с 1) для позиции в тексте. */
    public static int lineOf(String text, int index) {
        int line = 1;
        for (int i = 0; i < index && i < text.length(); i++) {
            if (text.charAt(i) == '\n') {
                line++;
            }
        }
        return line;
    }

    /**
     * Проверяет, что в коде объявлена переменная: тип, имя и значение.
     * valueRegex — регулярное выражение для значения, например "5" или "\"Стив\"".
     * Если нашлась похожая строка с другим типом или значением — сообщение укажет на неё.
     */
    public static void assertDeclared(String type, String name, String valueRegex, String shown) {
        String code = code();
        if (Pattern.compile("\\b" + Pattern.quote(type) + "\\s+" + Pattern.quote(name) + "\\s*=\\s*" + valueRegex + "\\s*;")
                .matcher(code).find()) {
            return;
        }
        Matcher any = Pattern.compile("(\\b[\\w\\[\\]]+)\\s+" + Pattern.quote(name) + "\\s*(=[^;\\n]*)?;?").matcher(code);
        while (any.find()) {
            String foundType = any.group(1);
            if (foundType.equals("println") || foundType.equals("print") || foundType.equals("return")) {
                continue;
            }
            int line = lineOf(code, any.start());
            if (!foundType.equals(type) && isTypeName(foundType)) {
                Assertions.fail("Строка " + line + ": у переменной " + name + " тип " + foundType + ", а нужен " + type + "."
                        + "\nЖдём объявление: " + shown);
            }
            if (foundType.equals(type)) {
                Assertions.fail("Строка " + line + ": переменная " + name + " объявлена, но значение не то."
                        + "\n  у тебя: " + any.group().trim()
                        + "\n  ждём:   " + shown);
            }
        }
        Assertions.fail("Не нашёл объявление переменной " + name + ".\nЖдём строку: " + shown
                + "\nПроверь имя: регистр букв важен, " + name + " и " + capitalize(name) + " — разные имена.");
    }

    /** Проверяет, что код совпадает с регулярным выражением; иначе — понятное сообщение. */
    public static void assertCode(String regex, String message) {
        if (!Pattern.compile(regex).matcher(code()).find()) {
            Assertions.fail(message);
        }
    }

    /** Сколько раз регулярное выражение встречается в коде (без комментариев). */
    public static int count(String regex) {
        Matcher m = Pattern.compile(regex).matcher(code());
        int n = 0;
        while (m.find()) {
            n++;
        }
        return n;
    }

    /**
     * Проверяет, что числа не вписаны в код «готовыми» (вне строк в кавычках).
     * Нужна там, где число должна посчитать программа, а не ученик в уме.
     */
    public static void assertNoNumbers(String why, int... numbers) {
        String code = sourceWithoutStrings("src/Main.java");
        for (int n : numbers) {
            Matcher m = Pattern.compile("(?<![\\w.])" + n + "(?![\\w.])").matcher(code);
            if (m.find()) {
                Assertions.fail("Строка " + lineOf(code, m.start()) + ": в коде готовое число " + n + ". " + why);
            }
        }
    }

    private static boolean isTypeName(String word) {
        return word.matches("int|long|double|float|boolean|char|byte|short|String|var");
    }

    private static String capitalize(String s) {
        return s.isEmpty() ? s : Character.toUpperCase(s.charAt(0)) + s.substring(1);
    }

    private static String blank(String src, boolean strings) {
        StringBuilder out = new StringBuilder(src.length());
        int i = 0;
        while (i < src.length()) {
            char c = src.charAt(i);
            char next = i + 1 < src.length() ? src.charAt(i + 1) : '\0';
            if (c == '/' && next == '/') {
                while (i < src.length() && src.charAt(i) != '\n') {
                    out.append(' ');
                    i++;
                }
            } else if (c == '/' && next == '*') {
                int end = src.indexOf("*/", i + 2);
                end = end < 0 ? src.length() : end + 2;
                for (; i < end; i++) {
                    out.append(src.charAt(i) == '\n' ? '\n' : ' ');
                }
            } else if (c == '"' || c == '\'') {
                char quote = c;
                out.append(c);
                i++;
                while (i < src.length() && src.charAt(i) != quote && src.charAt(i) != '\n') {
                    if (src.charAt(i) == '\\' && i + 1 < src.length()) {
                        out.append(strings ? "  " : src.substring(i, i + 2));
                        i += 2;
                        continue;
                    }
                    out.append(strings ? ' ' : src.charAt(i));
                    i++;
                }
                if (i < src.length() && src.charAt(i) == quote) {
                    out.append(quote);
                    i++;
                }
            } else {
                out.append(c);
                i++;
            }
        }
        return out.toString();
    }

    private static List<String> lines(String text) {
        List<String> result = new ArrayList<>();
        for (String line : Arrays.asList(text.replace("\r\n", "\n").replace('\r', '\n').split("\n", -1))) {
            result.add(line.stripTrailing());
        }
        while (!result.isEmpty() && result.get(result.size() - 1).isEmpty()) {
            result.remove(result.size() - 1);
        }
        return result;
    }

    private static String whereDiffers(String e, String a) {
        int i = 0;
        while (i < e.length() && i < a.length() && e.charAt(i) == a.charAt(i)) {
            i++;
        }
        if (i == a.length()) {
            return "Твоя строка обрывается на символе " + (i + 1) + " — дальше должно быть «" + e.substring(i) + "».";
        }
        if (i == e.length()) {
            return "После символа " + i + " у тебя лишнее: «" + a.substring(i) + "».";
        }
        return "Первое отличие в символе " + (i + 1) + ": ждём «" + e.charAt(i) + "», а у тебя «" + a.charAt(i) + "».";
    }

    @FunctionalInterface
    public interface ThrowingRunnable {
        void run() throws Exception;
    }
}
