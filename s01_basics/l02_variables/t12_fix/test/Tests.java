import course.Check;
import org.junit.jupiter.api.Test;

public class Tests {
    @Test
    public void printsFromVariables() {
        Check.assertCode("\\+\\s*torches\\b", "Количество факелов печатай из переменной: \"Факелов: \" + torches");
        Check.assertCode("\\+\\s*isNight\\b", "Ночь печатай из переменной: \"Ночь: \" + isNight");
    }

    @Test
    public void output() {
        String out = Check.runMain(() -> Main.main(new String[]{}));
        Check.assertOutput("""
                Факелов: 32
                Ночь: true
                """, out);
    }
}
