public class Rubis extends Joyau {
    private String couleur;

    public Rubis(String nom, int prix, String couleur) {
        super(nom,prix);
        this.couleur = couleur;
    }

    public String getCouleur() {
        return couleur;
    }
}