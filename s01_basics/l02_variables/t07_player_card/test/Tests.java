import course.Check;
import org.junit.jupiter.api.Test;

public class Tests {
    @Test
    public void name() {
        Check.assertDeclared("String", "name", "\"Алекс\"", "String name = \"Алекс\";");
    }

    @Test
    public void level() {
        Check.assertDeclared("int", "level", "30", "int level = 30;");
    }

    @Test
    public void health() {
        Check.assertDeclared("double", "health", "17\\.5", "double health = 17.5;");
    }

    @Test
    public void inNether() {
        Check.assertDeclared("boolean", "inNether", "true", "boolean inNether = true;");
    }

    @Test
    public void inventoryKey() {
        Check.assertDeclared("char", "inventoryKey", "'E'", "char inventoryKey = 'E';");
    }

    @Test
    public void output() {
        String out = Check.runMain(() -> Main.main(new String[]{}));
        Check.assertOutput("""
                Игрок: Алекс
                Уровень: 30
                Здоровье: 17.5
                В Незере: true
                Клавиша инвентаря: E
                """, out);
    }
}
