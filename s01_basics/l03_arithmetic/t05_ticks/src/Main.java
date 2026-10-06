public class Main {
    public static void main(String[] args) {
        int ticks = 200000;
        int totalSeconds = ticks / 20;
        int hours = totalSeconds / 3600;
        int minutes = totalSeconds % 3600 / 60;
        int seconds = totalSeconds % 60;
        System.out.println("Время: " + hours + " ч " + minutes + " мин " + seconds + " с");
    }
}
