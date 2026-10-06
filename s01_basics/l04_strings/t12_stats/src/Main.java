public class Main {
    public static void main(String[] args) {
        String name1 = "Steve";
        int level1 = 30;
        double health1 = 17.5;

        String name2 = "Alex";
        int level2 = 7;
        double health2 = 9.0;

        String name3 = "Kai";
        int level3 = 12;
        double health3 = 20.0;

        System.out.println("Игрок     Уровень  Здоровье");
        System.out.println(String.format("%-10s%-9d%.1f", name1, level1, health1));
        System.out.println(String.format("%-10s%-9d%.1f", name2, level2, health2));
        System.out.println(String.format("%-10s%-9d%.1f", name3, level3, health3));
    }
}
