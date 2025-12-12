public class RandomGeneration {
    public static void main(String[] args) {
        // Générer un réel dans [10, 30[
        double realValue = Math.random() * (30 - 10) + 10;
        System.out.println("Réel généré : " + realValue);

        // Générer un entier dans [50, 150]
        int intValue = (int) (Math.random() * (150 - 50 + 1) + 50);
        System.out.println("Entier généré : " + intValue);

        // Générer un booléen vrai dans 25% des cas
        boolean boolValue = Math.random() < 0.25;
        System.out.println("Booléen généré : " + boolValue);

        // Générer une lettre de l'alphabet entre 'a' et 'z'
        char letter = (char) (Math.random() * ('z' - 'a' + 1) + 'a');
        System.out.println("Lettre générée : " + letter);
    }
}
