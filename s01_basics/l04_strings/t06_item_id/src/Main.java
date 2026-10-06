public class Main {
    public static void main(String[] args) {
        String id = "minecraft:diamond_sword";

        int colon = id.indexOf(":");
        String namespace = id.substring(0, colon);
        String path = id.substring(colon + 1);
        System.out.println("Пространство имён: " + namespace);
        System.out.println("Путь: " + path);
    }
}
