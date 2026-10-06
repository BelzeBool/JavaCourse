import course.Check;
import org.junit.jupiter.api.Test;

public class Tests {
    @Test
    public void fixedProgramRuns() {
        String out = Check.runMain(() -> Main.main(new String[]{}));
        Check.assertOutput("""
                Ищу алмазы...
                Нашёл 3 алмаза!
                Иду домой
                """, out);
    }
}
