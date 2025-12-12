public abstract class Figure {
    // Variables d'instance (double pour la taille)
    protected double taille;

    // Constructeur
    public Figure(double taille) {
        this.taille = taille;
    }

    // Méthode abstraite surface()
    public abstract double surface();
}