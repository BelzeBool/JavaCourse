public class Main {
    public static void main(String[] args) {
        int days = 100000;

        int ticks = days * 24000;
        System.out.println(ticks);

        long bigTicks = days * 24000L;
        System.out.println(bigTicks);
    }
}
