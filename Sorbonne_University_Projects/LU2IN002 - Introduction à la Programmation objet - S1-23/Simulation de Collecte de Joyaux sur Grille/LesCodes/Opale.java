public class Opale extends Joyau {
    private boolean iridescent;

    public Opale(String nom,int prix, boolean iridescent) {
        super(nom,prix);
        this.iridescent = iridescent;
    }

    public boolean isIridescent() {
        return iridescent;
    }
}