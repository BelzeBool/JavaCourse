public class Main {
    public static void main(String[] args) {
        final int MAX_HEALTH = 20;
        final int MAX_STACK_SIZE = 64;
        int health = 17;
        int missingHealth = MAX_HEALTH - health;
        System.out.println("До полного здоровья: " + missingHealth);
        System.out.println("В стак помещается: " + MAX_STACK_SIZE);
        // MAX_STACK_SIZE = 16;
    }
}
