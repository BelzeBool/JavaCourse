public class Main {
    public static void main(String[] args) {
        String item = "Diamond_Sword";
        System.out.println(item.equals("diamond_sword"));
        System.out.println(item.equalsIgnoreCase("DIAMOND_SWORD"));
        System.out.println(item.endsWith("Sword"));
        System.out.println(item.contains("sword"));
        System.out.println(item.equals("Diamond_Sword "));
    }
}
