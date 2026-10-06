import course.Check;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Tests {
    @Test
    public void declaresTicks() {
        Check.assertDeclared("int", "ticks", "200_?000", "int ticks = 200000;");
    }

    @Test
    public void computesFromTicks() {
        if (Check.count("\\bticks\\b") < 2) {
            Assertions.fail("Время считай из переменной ticks: например, int totalSeconds = ticks / 20;");
        }
    }

    @Test
    public void computesItself() {
        Check.assertNoNumbers("Пусть программа посчитает сама — из ticks, делением и остатком.", 2, 46, 40, 10000);
    }

    @Test
    public void numbersNotInText() {
        assertNotInText("Пусть число печатает программа: \"Время: \" + hours + \" ч \" + …", "2", "46", "40");
    }

    @Test
    public void output() {
        String out = Check.runMain(() -> Main.main(new String[]{}));
        Check.assertOutput("Время: 2 ч 46 мин 40 с", out);
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
