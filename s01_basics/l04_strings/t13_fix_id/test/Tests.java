import course.Check;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class Tests {
    @Test
    public void titleUnchanged() {
        Check.assertDeclared("String", "title", "\" Ruby Sword \"", "String title = \" Ruby Sword \";"
                + "\nНазвание не меняй: пробелы по краям и заглавные буквы должна убрать программа.");
    }

    @Test
    public void checkLineKept() {
        Check.assertCode("id\\s*\\.\\s*equals\\s*\\(\\s*\"ruby_mod:ruby_sword\"\\s*\\)",
                "Строку с проверкой не меняй: System.out.println(\"Проверка: \" + id.equals(\"ruby_mod:ruby_sword\"));");
    }

    @Test
    public void idBuiltByProgram() {
        int times = Check.count("ruby_sword");
        if (times > 1) {
            Assertions.fail("ID собирает программа из title — готовый ruby_sword вписывать не нужно."
                    + "\nТекст ruby_sword должен быть в коде один раз — в строке проверки. Сейчас — " + times + ".");
        }
    }

    @Test
    public void output() {
        String out = Check.runMain(() -> Main.main(new String[]{}));
        Check.assertOutput("""
                ID: ruby_mod:ruby_sword
                Ключ перевода: item.ruby_mod.ruby_sword
                Проверка: true
                """, out);
    }
}
