public class Diamant extends Joyau {
    private int carats;
    public Diamant(String nom,int prix,int carats) {
        super(nom,prix);
        this.carats = carats;
    }

    public int getCarats(){
        return carats;
    }
}