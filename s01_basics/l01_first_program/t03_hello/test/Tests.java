import course.Check;
import org.junit.jupiter.api.Test;

public class Tests {
    @Test
    public void printsThreeLines() {
        String out = Check.runMain(() -> Main.main(new String[]{}));
        Check.assertOutput("""
                Привет, Майнкрафт!
                Меня зовут Стив.
                Сегодня я построю дом.
                """, out);
    }
}
