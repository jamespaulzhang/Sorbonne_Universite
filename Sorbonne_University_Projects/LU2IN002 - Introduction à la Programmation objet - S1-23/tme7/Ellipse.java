public class Ellipse extends Figure2D {
    // Variables d'instance spécifiques à Ellipse (demi-grand axe et demi-petit axe)
    private double demiGrandAxe;
    private double demiPetitAxe;

    // Constructeur
    public Ellipse(double demiGrandAxe, double demiPetitAxe) {
        super(demiGrandAxe); // On utilise le demi-grand axe comme taille de la figure
        this.demiGrandAxe = demiGrandAxe;
        this.demiPetitAxe = demiPetitAxe;
    }

    // Implémentation de la méthode surface() pour Ellipse
    public double surface() {
        return Math.PI * demiGrandAxe * demiPetitAxe;
    }

    // Implémentation de la méthode perimetre() pour Ellipse
    public double perimetre() {
        return 2 * Math.PI * Math.sqrt((Math.pow(demiGrandAxe, 2) + Math.pow(demiPetitAxe, 2)) / 2);
    }
}
