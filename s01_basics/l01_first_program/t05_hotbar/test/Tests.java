import course.Check;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class Tests {
    @Test
    public void printsHotbar() {
        String out = Check.runMain(() -> Main.main(new String[]{}));
        Check.assertOutput("""
                [Меч] [Кирка] [Факел] [Хлеб]
                Выбран слот 1: Меч
                """, out);
    }

    @Test
    public void usesFourPrints() {
        String code = Check.sourceWithoutComments("src/Main.java");
        int prints = code.split("System\\.out\\.print\\(", -1).length - 1;
        Assertions.assertTrue(prints >= 4,
                "Первую строку нужно собрать из четырёх команд print"
                        + " (по одной на предмет). Сейчас print в коде: " + prints + ".");
    }
}
