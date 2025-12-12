public class Rectangle extends Figure2D {
    // Variables d'instance spécifiques à Rectangle (longueur et largeur)
    private double longueur;
    private double largeur;

    // Constructeur
    public Rectangle(double longueur, double largeur) {
        super(longueur); // On utilise la longueur comme taille de la figure
        this.longueur = longueur;
        this.largeur = largeur;
    }

    // Implémentation de la méthode surface() pour Rectangle
    public double surface() {
        return longueur * largeur;
    }

    // Implémentation de la méthode perimetre() pour Rectangle
    public double perimetre() {
        return 2 * (longueur + largeur);
    }
}