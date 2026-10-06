import course.Check;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Tests {
    @Test
    public void keepsCoordinates() {
        Check.assertDeclared("int", "spawnX", "10", "int spawnX = 10;");
        Check.assertDeclared("int", "spawnZ", "30", "int spawnZ = 30;");
        Check.assertDeclared("int", "playerX", "-\\s*150", "int playerX = -150;");
        Check.assertDeclared("int", "playerZ", "210", "int playerZ = 210;");
    }

    @Test
    public void computesItself() {
        Check.assertNoNumbers("Пусть программа посчитает сама — из координат.", 160, 180, 241, 25600, 32400, 58000);
    }

    @Test
    public void numbersNotInText() {
        assertNotInText("Пусть число печатает программа: приклей к тексту переменную, например \"По X: \" + dx", "160", "180", "241");
    }

    @Test
    public void output() {
        String out = Check.runMain(() -> Main.main(new String[]{}));
        Check.assertOutput("""
                По X: 160
                По Z: 180
                По прямой: 241
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
