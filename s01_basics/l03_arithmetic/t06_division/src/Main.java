public class Main {
    public static void main(String[] args) {
        int fuse = 30;
        double seconds = fuse / 20;
        System.out.println(seconds);
        seconds = fuse / 20.0;
        System.out.println(seconds);

        System.out.println((double) fuse / 20);
        System.out.println((int) 1.99);
    }
}
