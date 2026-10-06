public class Main {
    public static void main(String[] args) {
        int iron = 20;
        int sand = 48;
        int beef = 5;

        int ironCoal = (iron + 7) / 8;
        int sandCoal = (sand + 7) / 8;
        int beefCoal = (beef + 7) / 8;
        System.out.println("Уголь для железа: " + ironCoal);
        System.out.println("Уголь для песка: " + sandCoal);
        System.out.println("Уголь для говядины: " + beefCoal);
    }
}
