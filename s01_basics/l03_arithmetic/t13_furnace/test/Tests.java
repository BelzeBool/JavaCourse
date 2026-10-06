import course.Check;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Tests {
    @Test
    public void keepsItems() {
        Check.assertDeclared("int", "iron", "20", "int iron = 20;");
        Check.assertDeclared("int", "sand", "48", "int sand = 48;");
        Check.assertDeclared("int", "beef", "5", "int beef = 5;");
    }

    @Test
    public void computesFromVariables() {
        for (String name : new String[]{"iron", "sand", "beef"}) {
            if (Check.count("\\b" + name + "\\b") < 2) {
                Assertions.fail("Уголь считай из переменной " + name + ": (" + name + " + …) / 8. Готовое число вместо неё не подойдёт.");
            }
        }
    }

    @Test
    public void computesItself() {
        Check.assertNoNumbers("Пусть программа посчитает сама — из iron, sand и beef.", 3, 6);
    }

    @Test
    public void numbersNotInText() {
        assertNotInText("Пусть число печатает программа: \"Уголь для железа: \" + ironCoal", "3", "6", "1");
    }

    @Test
    public void output() {
        String out = Check.runMain(() -> Main.main(new String[]{}));
        Check.assertOutput("""
                Уголь для железа: 3
                Уголь для песка: 6
                Уголь для говядины: 1
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
