public class Main {
    public static void main(String[] args) {
        int spawnX = 10;
        int spawnZ = 30;
        int playerX = -150;
        int playerZ = 210;

        int dx = Math.abs(playerX - spawnX);
        int dz = Math.abs(playerZ - spawnZ);
        long distance = Math.round(Math.sqrt(dx * dx + dz * dz));
        System.out.println("По X: " + dx);
        System.out.println("По Z: " + dz);
        System.out.println("По прямой: " + distance);
    }
}
