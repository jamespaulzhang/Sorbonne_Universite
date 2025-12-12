public class Joueur {
    private String nom;
    private Ballon bal;

    public Joueur(String nom, Ballon bal) {
        this.nom = nom;
        this.bal = bal;
    }

    public Joueur(String nom) {
        this.nom = nom;
        this.bal = null;
    }

    public String getNom(){
    	return nom;
    }

    public Ballon getBal(){
    	return bal;
    }

	public boolean avoirBallon() {
        return bal != null;
    }

	public String passerBallon(Joueur j2) {
    	if (bal != null && j2.getBal() != null && this.nom != j2.getNom()) {
        	return nom + " passe le ballon à " + j2.getNom();
    	} else if (bal == null || j2.getBal() == null) {
        	return nom + " ne peut pas passer le ballon, car il ne l'a pas";
    	} else {
        	return nom + " ne peut pas se passer le ballon à lui-même";
    	}
	}

    public Ballon tirer() {
    	if (bal != null) {
        	Ballon tempBallon = bal;
        	bal = null;
        	System.out.println(nom + " tire !");
        	return tempBallon;
    	} else {
        System.out.println(nom + " n'a pas le ballon, il ne peut pas tirer");
        return null;
    	}
    }

    public String toString() {
        if (bal != null) {
            return nom + " a le ballon de couleur " + bal.getCouleur() + " et de diamètre " + bal.getDiametre() + " cm";
        } else {
            return nom + " n'a pas le ballon";
        }
    }

    public static void main(String[] args) {
    	Ballon bal = new Ballon(21, "bleu");
    	Joueur olive = new Joueur("Olive", bal);
    	Joueur paul = new Joueur("Paul");
    	Joueur tom = new Joueur("Tom");

    	//System.out.println(olive.toString());
    	//System.out.println(paul.toString());
    	//System.out.println(olive.avoirBallon());
    	//System.out.println(olive.passerBallon(tom));
    	//System.out.println(olive.passerBallon(paul));
    	//System.out.println(olive.passerBallon(olive));

		for (int i = 0; i <= 3; i++) {
	        if (olive.avoirBallon()) {
	            tom.bal = olive.tirer();
	            System.out.println(olive);
	            System.out.println(tom);
                System.out.println("\n");
	        } else if (tom.avoirBallon()) {
	        	olive.bal = tom.tirer();
	            System.out.println(olive);
	            System.out.println(tom);
                System.out.println("\n");
	        }
	    }

	    Ballon ballForShot = olive.tirer();
	    if (ballForShot != null) {
	        System.out.println(olive.getNom() + " tire au but !");
	    }
	}
}