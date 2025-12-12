public class Carre extends Figure2D {
    // Variable d'instance spécifique à Carre (côté)
    private double cote;

    // Constructeur
    public Carre(double cote) {
        super(cote); // On utilise le côté comme taille de la figure
        this.cote = cote;
    }

    // Implémentation de la méthode surface() pour Carre
    public double surface() {
        return cote * cote;
    }

    // Implémentation de la méthode perimetre() pour Carre
    public double perimetre() {
        return 4 * cote;
    }
}
