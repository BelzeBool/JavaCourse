public class Main {
    public static void main(String[] args) {
        String id = "minecraft:stone";
        int colon = id.indexOf(":");
        String namespace = id.substring(0, colon);
        String path = id.substring(colon + 1);
        System.out.println(colon);
        System.out.println(namespace);
        System.out.println(path);
    }
}
