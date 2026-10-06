import course.Check;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class Tests {
    @Test
    public void startsAtFive() {
        Check.assertDeclared("int", "level", "5", "int level = 5;");
    }

    @Test
    public void computesItself() {
        Check.assertNoNumbers("Пусть программа посчитает сама: прибавь к level 7, потом отними 3.", 12, 9);
    }

    @Test
    public void printsVariable() {
        int prints = Check.count("println\\s*\\([^;]*\\blevel\\b");
        Assertions.assertTrue(prints >= 3,
                "Все три строки печатай из переменной: System.out.println(\"Уровень: \" + level);"
                        + "\nСейчас команд println с level: " + prints + ".");
    }

    @Test
    public void output() {
        String out = Check.runMain(() -> Main.main(new String[]{}));
        Check.assertOutput("""
                Уровень: 5
                После боя: 12
                После зачарования: 9
                """, out);
    }
}
