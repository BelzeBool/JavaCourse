public class Main {
    public static void main(String[] args) {
        int side = 50000;
        int a = side * side;
        long b = side * side;
        long c = (long) side * side;
        // long d = 2500000000;
        System.out.println(a);
        System.out.println(b);
        System.out.println(c);
    }
}
