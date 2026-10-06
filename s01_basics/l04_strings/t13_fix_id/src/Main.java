public class Main {
    public static void main(String[] args) {
        String modId = "ruby_mod";
        String title = " Ruby Sword ";
        title = title.strip();
        String path = title.toLowerCase();
        path = path.replace(" ", "_");
        String id = modId + ":" + path;
        System.out.println("ID: " + id);
        System.out.println("Ключ перевода: item." + modId + "." + path);
        System.out.println("Проверка: " + id.equals("ruby_mod:ruby_sword"));
    }
}
