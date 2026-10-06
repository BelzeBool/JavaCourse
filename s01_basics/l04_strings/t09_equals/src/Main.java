public class Main {
    public static void main(String[] args) {
        String item = "diamond_sword";
        System.out.println(item.equals("diamond_sword"));
        System.out.println(item.equals("Diamond_Sword"));
        System.out.println(item.equalsIgnoreCase("Diamond_Sword"));

        boolean isSword = item.endsWith("_sword");
        System.out.println("Меч: " + isSword);
        System.out.println("Алмазный: " + item.startsWith("diamond"));
        System.out.println("Железный: " + item.contains("iron"));
    }
}
