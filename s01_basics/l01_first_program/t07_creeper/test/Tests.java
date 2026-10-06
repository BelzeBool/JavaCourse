import course.Check;
import org.junit.jupiter.api.Test;

public class Tests {
    @Test
    public void drawsCreeper() {
        String out = Check.runMain(() -> Main.main(new String[]{}));
        Check.assertOutput("""
                ........
                .##..##.
                .##..##.
                ...##...
                ..####..
                ..####..
                ..#..#..
                ........
                """, out);
    }
}
