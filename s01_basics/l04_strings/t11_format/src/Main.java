public class Main {
    public static void main(String[] args) {
        String name = "Steve";
        int level = 30;
        double health = 17.5;
        String line = String.format("Игрок %s, уровень %d, здоровье %.1f", name, level, health);
        System.out.println(line);

        System.out.println(String.format("%-8s%5d", "Steve", 30));
        System.out.println(String.format("%-8s%5d", "Alex", 7));

        String card = """
                Игрок: %s
                Уровень: %d
                """.formatted(name, level);
        System.out.print(card);
    }
}
