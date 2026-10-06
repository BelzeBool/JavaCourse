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

    /** Исходник без комментариев — чтобы закомментированный код не засчитывался. */
    public static String sourceWithoutComments(String path) {
        return source(path)
                .replaceAll("(?s)/\\*.*?\\*/", "")
                .replaceAll("//[^\\n]*", "");
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
