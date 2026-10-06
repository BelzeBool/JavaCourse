package course;

import org.junit.jupiter.api.Assertions;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.time.Duration;
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

    /** Сколько ждём программу ученика, прежде чем решить, что она зависла. */
    public static final Duration TIMEOUT = Duration.ofSeconds(5);

    /** Запускает main ученика и возвращает всё, что он напечатал. */
    public static String runMain(ThrowingRunnable main) {
        return runMainWithInput("", main);
    }

    /**
     * Запускает main ученика так, будто с клавиатуры ввели input (строки через \n),
     * и возвращает всё, что программа напечатала.
     */
    public static String runMainWithInput(String input, ThrowingRunnable main) {
        PrintStream originalOut = System.out;
        InputStream originalIn = System.in;
        ByteArrayOutputStream buffer = new ByteArrayOutputStream();
        System.setOut(new PrintStream(buffer, true, StandardCharsets.UTF_8));
        System.setIn(new ByteArrayInputStream(input.getBytes(StandardCharsets.UTF_8)));
        try {
            runWithTimeout(main, "Программа", "Программа упала с ошибкой: ");
        } finally {
            System.setOut(originalOut);
            System.setIn(originalIn);
        }
        return buffer.toString(StandardCharsets.UTF_8);
    }

    // ---------- вызов методов ученика ----------

    /**
     * Вызывает static-метод ученика по имени: Check.call(Main.class, "stacks", 200).
     * Если метода нет или параметры не те — понятное сообщение вместо ошибки компиляции тестов.
     */
    public static Object call(Class<?> cls, String name, Object... args) {
        Method m = findMethod(cls, name, args);
        if (!Modifier.isStatic(m.getModifiers())) {
            Assertions.fail("Метод " + name + " должен быть static: в этой главе все методы пишутся со словом static."
                    + "\nЖдём: static ... " + expectedSignature(name, args));
        }
        return invoke(m, null, name, args);
    }

    /** Вызывает метод объекта ученика: Check.callOn(zombie, "takeDamage", 5). */
    public static Object callOn(Object target, String name, Object... args) {
        Method m = findMethod(target.getClass(), name, args);
        return invoke(m, target, name, args);
    }

    /**
     * Проверяет, что метод возвращает нужное значение:
     * Check.assertCall(3, Main.class, "stacks", 200) → «stacks(200) должен вернуть 3, а вернул 4».
     */
    public static void assertCall(Object expected, Class<?> cls, String name, Object... args) {
        Object actual = call(cls, name, args);
        if (!same(expected, actual)) {
            Assertions.fail(expectedSignatureCall(name, args) + " должен вернуть " + describe(expected)
                    + ", а вернул " + describe(actual) + ".");
        }
    }

    /** Создаёт объект класса ученика по имени: Check.newObject("ItemStack", "diamond", 3). */
    public static Object newObject(String className, Object... args) {
        Class<?> cls = classNamed(className);
        List<String> found = new ArrayList<>();
        for (Constructor<?> c : cls.getDeclaredConstructors()) {
            found.add(className + params(c.getParameterTypes()));
            if (fits(c.getParameterTypes(), args)) {
                c.setAccessible(true);
                try {
                    return c.newInstance(convert(c.getParameterTypes(), args));
                } catch (InvocationTargetException e) {
                    rethrowAssertion(e.getCause());
                    Assertions.fail("new " + expectedSignatureCall(className, args) + " упал: " + explain(e.getCause()));
                } catch (ReflectiveOperationException e) {
                    Assertions.fail("Не получилось создать " + className + ": " + e);
                }
            }
        }
        Assertions.fail("У класса " + className + " нет конструктора " + expectedSignature(className, args) + "."
                + (found.isEmpty() ? "" : "\nЕсть такие: " + String.join(", ", found)));
        return null;
    }

    /** Класс ученика по имени (без пакета или с пакетом: "item.ItemStack"). */
    public static Class<?> classNamed(String className) {
        try {
            return Class.forName(className);
        } catch (ClassNotFoundException e) {
            Assertions.fail("Не нашёл класс " + className + ". Проверь имя класса и файла: регистр важен, "
                    + "класс " + className + " должен лежать в файле " + className.replace('.', '/') + ".java.");
            return null;
        }
    }

    /** Значение для сообщений: строки в кавычках, массивы поэлементно. */
    public static String describe(Object v) {
        if (v == null) {
            return "null";
        }
        if (v instanceof String) {
            return "\"" + v + "\"";
        }
        if (v instanceof Character) {
            return "'" + v + "'";
        }
        if (v.getClass().isArray()) {
            return Arrays.deepToString(new Object[]{v}).replaceAll("^\\[|\\]$", "");
        }
        return String.valueOf(v);
    }

    private static Method findMethod(Class<?> cls, String name, Object[] args) {
        List<String> sameName = new ArrayList<>();
        for (Method m : cls.getDeclaredMethods()) {
            if (!m.getName().equals(name)) {
                continue;
            }
            sameName.add(name + params(m.getParameterTypes()));
            if (fits(m.getParameterTypes(), args)) {
                m.setAccessible(true);
                return m;
            }
        }
        if (sameName.isEmpty()) {
            Assertions.fail("В классе " + cls.getSimpleName() + " нет метода " + name + ".\nЖдём: "
                    + expectedSignature(name, args) + "\nПроверь имя: регистр букв важен.");
        }
        Assertions.fail("Метод " + name + " есть, но параметры не те.\n  у тебя: " + String.join(", ", sameName)
                + "\n  ждём:   " + expectedSignature(name, args));
        return null;
    }

    private static Object invoke(Method m, Object target, String name, Object[] args) {
        Object[] converted = convert(m.getParameterTypes(), args);
        Object[] result = new Object[1];
        runWithTimeout(() -> {
            try {
                result[0] = m.invoke(target, converted);
            } catch (InvocationTargetException e) {
                rethrowAssertion(e.getCause());
                Assertions.fail("Вызов " + expectedSignatureCall(name, args) + " упал: " + explain(e.getCause()));
            }
        }, "Вызов " + expectedSignatureCall(name, args), "Вызов " + expectedSignatureCall(name, args) + " упал: ");
        return result[0];
    }

    private static void runWithTimeout(ThrowingRunnable code, String who, String crashed) {
        Assertions.assertTimeoutPreemptively(TIMEOUT, () -> {
            try {
                code.run();
            } catch (Throwable e) {
                rethrowAssertion(e);
                Assertions.fail(crashed + explain(e)
                        + "\nЗапусти программу (зелёный треугольник рядом с main) и посмотри, что случилось.");
            }
        }, () -> who + " работает дольше " + TIMEOUT.toSeconds() + " секунд — похоже на бесконечный цикл."
                + "\nПроверь условие цикла: оно когда-нибудь станет ложным?");
    }

    private static void rethrowAssertion(Throwable e) {
        if (e instanceof AssertionError) {
            throw (AssertionError) e;
        }
    }

    /** Исключение по-русски, со строкой в Main.java, где оно случилось. */
    public static String explain(Throwable e) {
        String type = e.getClass().getSimpleName();
        String ru = switch (type) {
            case "ArithmeticException" -> "арифметическая ошибка (например, деление на ноль)";
            case "ArrayIndexOutOfBoundsException" -> "выход за границы массива";
            case "StringIndexOutOfBoundsException" -> "выход за границы строки";
            case "NullPointerException" -> "обращение к null — там, где ждали объект, ничего нет";
            case "InputMismatchException" -> "введено не то, что ожидал Scanner (например, текст вместо числа)";
            case "NoSuchElementException" -> "ввод закончился, а программа ждёт ещё";
            case "NumberFormatException" -> "текст не получилось превратить в число";
            case "StackOverflowError" -> "переполнение стека — похоже на бесконечную рекурсию";
            case "ClassCastException" -> "неверное приведение типа";
            default -> "";
        };
        StringBuilder out = new StringBuilder(type);
        if (e.getMessage() != null) {
            out.append(": ").append(e.getMessage());
        }
        if (!ru.isEmpty()) {
            out.append(" — ").append(ru);
        }
        for (StackTraceElement el : e.getStackTrace()) {
            String file = el.getFileName();
            if (file != null && !file.equals("Tests.java") && !el.getClassName().startsWith("java.")
                    && !el.getClassName().startsWith("jdk.") && !el.getClassName().equals("course.Check")
                    && !el.getClassName().startsWith("course.Check$")
                    && !el.getClassName().startsWith("org.")) {
                out.append(" (").append(file).append(", строка ").append(el.getLineNumber()).append(")");
                break;
            }
        }
        return out.toString();
    }

    private static boolean fits(Class<?>[] params, Object[] args) {
        if (params.length != args.length) {
            return false;
        }
        for (int i = 0; i < params.length; i++) {
            if (!fits(params[i], args[i])) {
                return false;
            }
        }
        return true;
    }

    private static boolean fits(Class<?> p, Object a) {
        if (a == null) {
            return !p.isPrimitive();
        }
        Class<?> w = wrap(p);
        if (w.isInstance(a)) {
            return true;
        }
        // расширение чисел: int можно передать туда, где ждут long или double
        if (a instanceof Integer && (w == Long.class || w == Double.class)) {
            return true;
        }
        return a instanceof Long && w == Double.class;
    }

    private static Object[] convert(Class<?>[] params, Object[] args) {
        Object[] out = new Object[args.length];
        for (int i = 0; i < args.length; i++) {
            Class<?> w = wrap(params[i]);
            Object a = args[i];
            if (a instanceof Number n && !w.isInstance(a)) {
                a = w == Long.class ? (Object) n.longValue() : w == Double.class ? (Object) n.doubleValue() : a;
            }
            out[i] = a;
        }
        return out;
    }

    private static Class<?> wrap(Class<?> c) {
        if (!c.isPrimitive()) {
            return c;
        }
        return switch (c.getName()) {
            case "int" -> Integer.class;
            case "long" -> Long.class;
            case "double" -> Double.class;
            case "boolean" -> Boolean.class;
            case "char" -> Character.class;
            case "float" -> Float.class;
            case "short" -> Short.class;
            case "byte" -> Byte.class;
            default -> Void.class;
        };
    }

    private static boolean same(Object expected, Object actual) {
        if (expected instanceof Double d && actual instanceof Number n) {
            return Math.abs(d - n.doubleValue()) < 1e-9;
        }
        if (expected != null && actual != null && expected.getClass().isArray()) {
            return Arrays.deepEquals(new Object[]{expected}, new Object[]{actual});
        }
        if (expected instanceof Integer i && actual instanceof Long l) {
            return i.longValue() == l;
        }
        return java.util.Objects.equals(expected, actual);
    }

    private static String params(Class<?>[] types) {
        StringBuilder sb = new StringBuilder("(");
        for (int i = 0; i < types.length; i++) {
            sb.append(i > 0 ? ", " : "").append(types[i].getSimpleName());
        }
        return sb.append(")").toString();
    }

    private static String expectedSignature(String name, Object[] args) {
        StringBuilder sb = new StringBuilder(name).append("(");
        for (int i = 0; i < args.length; i++) {
            Object a = args[i];
            String t = a == null ? "?" : switch (a.getClass().getSimpleName()) {
                case "Integer" -> "int";
                case "Double" -> "double";
                case "Boolean" -> "boolean";
                case "Character" -> "char";
                case "Long" -> "long";
                default -> a.getClass().getSimpleName();
            };
            sb.append(i > 0 ? ", " : "").append(t);
        }
        return sb.append(")").toString();
    }

    private static String expectedSignatureCall(String name, Object[] args) {
        StringBuilder sb = new StringBuilder(name).append("(");
        for (int i = 0; i < args.length; i++) {
            sb.append(i > 0 ? ", " : "").append(describe(args[i]));
        }
        return sb.append(")").toString();
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
