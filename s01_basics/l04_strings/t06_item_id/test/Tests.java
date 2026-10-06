import course.Check;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class Tests {
    @Test
    public void idUnchanged() {
        Check.assertDeclared("String", "id", "\"minecraft:diamond_sword\"", "String id = \"minecraft:diamond_sword\";");
    }

    @Test
    public void colonFound() {
        Check.assertNoNumbers("Номер двоеточия найди методом: int colon = id.indexOf(\":\");", 9, 10);
    }

    @Test
    public void partsCutFromId() {
        int namespace = Check.count("minecraft");
        int path = Check.count("diamond_sword");
        if (namespace > 1 || path > 1) {
            Assertions.fail("Части вырежи из id методом substring, а не пиши готовым текстом."
                    + "\nТексты minecraft и diamond_sword должны быть в коде один раз — в самом id."
                    + "\nСейчас в коде minecraft: " + namespace + ", diamond_sword: " + path + ".");
        }
    }

    @Test
    public void output() {
        String out = Check.runMain(() -> Main.main(new String[]{}));
        Check.assertOutput("""
                Пространство имён: minecraft
                Путь: diamond_sword
                """, out);
    }
}
