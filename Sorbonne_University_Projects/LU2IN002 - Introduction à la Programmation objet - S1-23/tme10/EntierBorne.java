public class EntierBorne {
    private int valeur;
    public static final int MAX = 100;
    public static final int MIN = -100;

    public EntierBorne(int valeur) throws HorsBornesException{
        if (valeur > MAX)
            throw new HorsBornesException("Entier trop grand : " + valeur);
        if (valeur < MIN)
            throw new HorsBornesException("Entier trop petit : " + valeur);
        this.valeur = valeur;
    }

    public EntierBorne somme(EntierBorne eb) throws HorsBornesException{
        return new EntierBorne(valeur + eb.valeur);
    }

    public EntierBorne divPar(EntierBorne eb) throws DivisionParZeroException,HorsBornesException{
        if(eb.valeur == 0){
            throw new DivisionParZeroException("Division par zero");
        }else{
            return new EntierBorne((int)valeur/eb.valeur);
        }   
    }

    public String toString(){
        return "" + valeur;
    }
}