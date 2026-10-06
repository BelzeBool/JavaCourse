public class Main {
    public static void main(String[] args) {
        String nick = "Steve_Miner";

        System.out.println("Ник: " + nick);
        System.out.println("Символов: " + nick.length());
        System.out.println("Первая буква: " + nick.charAt(0));
        System.out.println("Последняя буква: " + nick.charAt(nick.length() - 1));
        System.out.println("Капсом: " + nick.toUpperCase());
    }
}
