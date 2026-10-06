public class Main {
    public static void main(String[] args) {
        String input = " Diamond Pickaxe ";
        String path = input.strip().toLowerCase().replace(" ", "_");
        String id = "minecraft:" + path;
        System.out.println("ID: " + id);
        System.out.println("Путь: " + id.substring(id.indexOf(":") + 1));
        System.out.println("Кирка: " + id.endsWith("_pickaxe"));
        System.out.println(String.format("В пути %d символов, первый — %s", path.length(), path.charAt(0)));
    }
}
