import course.Check;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class Tests {
    @Test
    public void printsSign() {
        String out = Check.runMain(() -> Main.main(new String[]{}));
        Check.assertOutput("""
                Табличка у шахты:
                "Не копай прямо вниз!"
                Мир лежит в C:\\minecraft\\saves
                """, out);
    }

    @Test
    public void usesSinglePrintln() {
        String code = Check.sourceWithoutComments("src/Main.java");
        int println = code.split("System\\.out\\.println\\(", -1).length - 1;
        int print = code.split("System\\.out\\.print\\(", -1).length - 1;
        Assertions.assertTrue(println == 1 && print == 0,
                "Нужна ровно одна команда println и ни одной print — переносы делай через \\n."
                        + " Сейчас в коде println: " + println + ", print: " + print + ".");
    }
}
