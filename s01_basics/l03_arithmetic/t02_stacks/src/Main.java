public class Main {
    public static void main(String[] args) {
        int blocks = 200;
        int stacks = blocks / 64;
        int rest = blocks % 64;
        System.out.println("Полных стаков: " + stacks);
        System.out.println("Остаток: " + rest);
    }
}
