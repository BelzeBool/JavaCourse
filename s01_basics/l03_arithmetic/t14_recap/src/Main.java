public class Main {
    public static void main(String[] args) {
        int blocks = 200;
        System.out.println("Стаков: " + blocks / 64 + ", сверху: " + blocks % 64);

        int fuse = 30;
        System.out.println("Крипер взорвётся через " + fuse / 20.0 + " с");

        int items = 20;
        System.out.println("Угля нужно: " + (items + 7) / 8);
    }
}
