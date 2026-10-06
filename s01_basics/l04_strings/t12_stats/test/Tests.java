import course.Check;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.util.Locale;

public class Tests {
    @BeforeAll
    public static void dotAsDecimalSeparator() {
        // %.1f берёт разделитель из настроек языка: на русской системе это запятая.
        // Проверяем с точкой, как в условии задачи.
        Locale.setDefault(Locale.ROOT);
    }

    @Test
    public void usesTemplate() {
        if (Check.count("String\\s*\\.\\s*format\\s*\\(|\\.formatted\\s*\\(|\\.printf\\s*\\(") == 0) {
            Assertions.fail("Строки таблицы печатай по шаблону: String.format(\"%-10s%-9d%.1f\", name1, level1, health1)");
        }
        Check.assertCode("%-10s", "Колонка с именем — шириной 10, прижата влево: в шаблоне нужен пропуск %-10s.");
    }

    @Test
    public void noManualSpaces() {
        if (Check.count("\"[ ]{2,}\"") > 0) {
            Assertions.fail("Пробелы вручную не добавляй — ширину колонок задаёт шаблон: %-10s и %-9d.");
        }
    }

    @Test
    public void namesFromVariables() {
        for (String name : new String[]{"Steve", "Alex", "Kai"}) {
            int times = Check.count("\\b" + name + "\\b");
            if (times > 1) {
                Assertions.fail("Имена бери из переменных name1, name2, name3."
                        + "\nИмя " + name + " должно быть в коде один раз — в объявлении. Сейчас — " + times + ".");
            }
        }
    }

    @Test
    public void numbersFromVariables() {
        for (String var : new String[]{"level1", "level2", "level3", "health1", "health2", "health3"}) {
            if (Check.count("\\b" + var + "\\b") < 2) {
                Assertions.fail("Уровень и здоровье бери из переменных. Переменная " + var
                        + " объявлена, но в таблице не используется.");
            }
        }
    }

    @Test
    public void output() {
        String out = Check.runMain(() -> Main.main(new String[]{}));
        Check.assertOutput("""
                Игрок     Уровень  Здоровье
                Steve     30       17.5
                Alex      7        9.0
                Kai       12       20.0
                """, out);
    }
}
