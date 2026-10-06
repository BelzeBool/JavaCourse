import course.Check;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class Tests {
    /** Сколько раз число встречается в коде — и в кавычках тоже: "Символов: 11" — тоже готовое число. */
    private static int numberInCode(int n) {
        return Check.count("(?<![\\w.])" + n + "(?![\\w.])");
    }

    @Test
    public void nickUnchanged() {
        Check.assertDeclared("String", "nick", "\"Steve_Miner\"", "String nick = \"Steve_Miner\";");
    }

    @Test
    public void nickFromVariable() {
        int times = Check.count("Steve_Miner");
        if (times > 1) {
            Assertions.fail("Ник печатай из переменной: \"Ник: \" + nick."
                    + "\nТекст Steve_Miner должен быть в коде один раз — в объявлении nick. Сейчас — " + times + ".");
        }
    }

    @Test
    public void lengthComputed() {
        if (numberInCode(11) > 0) {
            Assertions.fail("В коде готовое число 11. Длину пусть посчитает программа: nick.length()");
        }
        Check.assertCode("\\.length\\s*\\(\\s*\\)", "Длину узнай методом: nick.length()");
    }

    @Test
    public void lastIndexComputed() {
        if (numberInCode(10) > 0) {
            Assertions.fail("В коде готовое число 10. Номер последней клетки найди через длину: nick.length() - 1");
        }
    }

    @Test
    public void lettersFromNick() {
        if (Check.count("буква:\\s*[^\"\\s]") > 0) {
            Assertions.fail("Буквы не вписывай в текст готовыми — достань их из nick методом charAt."
                    + "\nНапример: \"Первая буква: \" + nick.charAt(0)");
        }
        if (Check.count("\\.charAt\\s*\\(") < 2) {
            Assertions.fail("Первую и последнюю букву достань методом charAt: nick.charAt(0) и ещё один charAt — для последней.");
        }
    }

    @Test
    public void upperCaseComputed() {
        if (Check.count("STEVE") > 0) {
            Assertions.fail("Готового текста STEVE_MINER в коде быть не должно. Ник капсом сделай методом: nick.toUpperCase()");
        }
        Check.assertCode("\\.toUpperCase\\s*\\(\\s*\\)", "Ник капсом сделай методом: nick.toUpperCase()");
    }

    @Test
    public void output() {
        String out = Check.runMain(() -> Main.main(new String[]{}));
        Check.assertOutput("""
                Ник: Steve_Miner
                Символов: 11
                Первая буква: S
                Последняя буква: r
                Капсом: STEVE_MINER
                """, out);
    }
}
