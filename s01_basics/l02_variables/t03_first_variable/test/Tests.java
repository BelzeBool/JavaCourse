import course.Check;
import org.junit.jupiter.api.Test;

public class Tests {
    @Test
    public void declaresVariable() {
        Check.assertDeclared("int", "diamonds", "12", "int diamonds = 12;");
    }

    @Test
    public void printsVariable() {
        Check.assertCode("println\\s*\\(\\s*diamonds\\s*\\)",
                "Число 12 нужно напечатать из переменной: System.out.println(diamonds);"
                        + "\nИмя переменной пишется без кавычек.");
    }

    @Test
    public void output() {
        String out = Check.runMain(() -> Main.main(new String[]{}));
        Check.assertOutput("Алмазов: 12", out);
    }
}
