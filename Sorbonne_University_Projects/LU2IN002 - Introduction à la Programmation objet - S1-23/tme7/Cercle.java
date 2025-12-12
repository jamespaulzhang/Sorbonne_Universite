public class Cercle extends Figure2D {
    // Variable d'instance spécifique à Cercle (rayon)
    private double rayon;

    // Constructeur
    public Cercle(double rayon) {
        super(rayon); // On utilise le rayon comme taille de la figure
        this.rayon = rayon;
    }

    // Implémentation de la méthode surface() pour Cercle
    public double surface() {
        return Math.PI * Math.pow(rayon, 2);
    }

    // Implémentation de la méthode perimetre() pour Cercle
    public double perimetre() {
        return 2 * Math.PI * rayon;
    }
}
