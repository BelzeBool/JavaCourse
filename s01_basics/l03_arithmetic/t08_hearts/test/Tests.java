import course.Check;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Tests {
    @Test
    public void keepsHealth() {
        Check.assertDeclared("int", "health", "17", "int health = 17;");
    }

    @Test
    public void heartsFromHealth() {
        Check.assertCode("\\bhearts\\s*=[^;]*\\bhealth\\b",
                "Сердечки считай из переменной health, а не готовым числом: double hearts = health ...;");
    }

    @Test
    public void computesItself() {
        Matcher m = Pattern.compile("(?<![\\w.])8\\.5(?![\\w.])").matcher(Check.sourceWithoutStrings("src/Main.java"));
        if (m.find()) {
            Assertions.fail("Строка " + Check.lineOf(Check.code(), m.start())
                    + ": в коде готовое число 8.5. Пусть программа посчитает сама — из health.");
        }
        Check.assertNoNumbers("Пусть программа посчитает сама — из health.", 8);
    }

    @Test
    public void numbersNotInText() {
        assertNotInText("Пусть число печатает программа: \"Сердечек: \" + hearts", "8.5", "8");
    }

    @Test
    public void output() {
        String out = Check.runMain(() -> Main.main(new String[]{}));
        Check.assertOutput("""
                Сердечек: 8.5
                Полных сердечек: 8
                """, out);
    }

    /** Ответ не вписан готовым числом в текст в кавычках. */
    private static void assertNotInText(String why, String... numbers) {
        String code = Check.code();
        Matcher s = Pattern.compile("\"(?:\\\\.|[^\"\\\\\\n])*\"").matcher(code);
        while (s.find()) {
            for (String n : numbers) {
                if (Pattern.compile("(?<!\\d)(?<!\\d\\.)" + Pattern.quote(n) + "(?!\\d)(?!\\.\\d)").matcher(s.group()).find()) {
                    Assertions.fail("Строка " + Check.lineOf(code, s.start()) + ": число " + n
                            + " вписано прямо в текст " + s.group() + ". " + why);
                }
            }
        }
    }
}
