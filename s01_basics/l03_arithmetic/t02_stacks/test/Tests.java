import course.Check;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Tests {
    @Test
    public void declaresBlocks() {
        Check.assertDeclared("int", "blocks", "200", "int blocks = 200;");
    }

    @Test
    public void usesDivision() {
        if (!Pattern.compile("\\bblocks\\s*/").matcher(Check.sourceWithoutStrings("src/Main.java")).find()) {
            Assertions.fail("Полные стаки посчитай делением переменной blocks: blocks / 64");
        }
    }

    @Test
    public void usesRemainder() {
        if (!Pattern.compile("\\bblocks\\s*%").matcher(Check.sourceWithoutStrings("src/Main.java")).find()) {
            Assertions.fail("Остаток посчитай знаком % от переменной blocks: blocks % 64");
        }
    }

    @Test
    public void computesItself() {
        Check.assertNoNumbers("Пусть программа посчитает сама: blocks / 64 и blocks % 64.", 3, 8);
    }

    @Test
    public void numbersNotInText() {
        assertNotInText("Пусть число печатает программа: \"Полных стаков: \" + stacks", "3", "8");
    }

    @Test
    public void output() {
        String out = Check.runMain(() -> Main.main(new String[]{}));
        Check.assertOutput("""
                Полных стаков: 3
                Остаток: 8
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
