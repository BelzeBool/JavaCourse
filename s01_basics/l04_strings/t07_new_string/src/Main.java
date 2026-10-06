public class Main {
    public static void main(String[] args) {
        String name = " Ruby ";
        name.strip();
        System.out.println("«" + name + "»");
        name = name.strip();
        System.out.println("«" + name + "»");

        String title = " Ruby Sword ";
        String id = title.strip().toLowerCase().replace(" ", "_");
        System.out.println(id);
    }
}
