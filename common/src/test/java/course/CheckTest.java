package course;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.opentest4j.AssertionFailedError;

import java.util.Scanner;

/** Проверяем сами помощники: что они ловят ошибки и пишут понятные сообщения. */
public class CheckTest {

    /** Как будто это Main ученика. */
    static class Sample {
        static int stacks(int count) {
            return count / 64;
        }

        static double half(double x) {
            return x / 2;
        }

        static int[] twice(int[] a) {
            int[] r = new int[a.length];
            for (int i = 0; i < a.length; i++) {
                r[i] = a[i] * 2;
            }
            return r;
        }

        static int broken(int x) {
            return 10 / x;
        }

        static void forever() {
            while (true) {
                Thread.onSpinWait();
            }
        }

        int notStatic() {
            return 1;
        }

        static void echo() {
            Scanner in = new Scanner(System.in);
            String name = in.nextLine();
            int n = in.nextInt();
            System.out.println(name + ":" + (n + 1));
        }
    }

    private static String failure(Runnable r) {
        try {
            r.run();
        } catch (AssertionFailedError e) {
            return e.getMessage();
        }
        throw new AssertionError("ожидали провал проверки, а её прошло");
    }

    @Test
    void callAndAssertCall() {
        Assertions.assertEquals(3, Check.call(Sample.class, "stacks", 200));
        Check.assertCall(3, Sample.class, "stacks", 200);
        Check.assertCall(2.5, Sample.class, "half", 5);
        Check.assertCall(new int[]{2, 4}, Sample.class, "twice", (Object) new int[]{1, 2});
        String msg = failure(() -> Check.assertCall(4, Sample.class, "stacks", 200));
        Assertions.assertTrue(msg.contains("stacks(200) должен вернуть 4, а вернул 3"), msg);
    }

    @Test
    void missingOrWrongMethod() {
        String none = failure(() -> Check.call(Sample.class, "stack", 200));
        Assertions.assertTrue(none.contains("нет метода stack") && none.contains("stack(int)"), none);
        String params = failure(() -> Check.call(Sample.class, "stacks", "200"));
        Assertions.assertTrue(params.contains("параметры не те") && params.contains("stacks(int)"), params);
        String inst = failure(() -> Check.call(Sample.class, "notStatic"));
        Assertions.assertTrue(inst.contains("должен быть static"), inst);
    }

    @Test
    void crashAndTimeout() {
        String crash = failure(() -> Check.call(Sample.class, "broken", 0));
        Assertions.assertTrue(crash.contains("ArithmeticException") && crash.contains("деление на ноль")
                && crash.contains("строка"), crash);
        String slow = failure(() -> Check.call(Sample.class, "forever"));
        Assertions.assertTrue(slow.contains("бесконечный цикл"), slow);
    }

    @Test
    void input() {
        String out = Check.runMainWithInput("Стив\n41\n", Sample::echo);
        Check.assertOutput("Стив:42", out);
        String ended = failure(() -> Check.runMainWithInput("Стив\n", Sample::echo));
        Assertions.assertTrue(ended.contains("ввод закончился"), ended);
    }

    @Test
    void outputDiff() {
        String msg = failure(() -> Check.assertOutput("Алмазов: 12", "Алмазов: 13"));
        Assertions.assertTrue(msg.contains("Строка 1 отличается") && msg.contains("символе 11"), msg);
    }
}
