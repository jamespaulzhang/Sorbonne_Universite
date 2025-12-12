public class Personne{
	private String nom;
	private Personne conjoint;

	public Personne(String nom){
		this.nom = nom;
		this.conjoint = null;
	}

	public Personne() {
        this("Pers" + (char) ('A' + (int) (Math.random() * ('Z' - 'A' + 1))));
    }

	public String toString() {
        if (conjoint == null) {
            return nom + ", célibataire";
        }
        return nom + ", marié(e)";
    }

    public void epouser(Personne p) {
    	if (this.conjoint != null || p.conjoint != null || this.nom.equals(p.nom) || p == null) {
        	System.out.println("Le mariage de " + this.nom + ", marié(e) avec " + p.nom + ", célibataire est impossible.");
    	} else {
       		this.conjoint = p;
        	p.conjoint = this;
        	System.out.println(this.nom + ", célibataire se marie avec " + p.nom + ", célibataire.");
    	}
	}


    public void divorcer(){
    	if(this.conjoint == null){
        	System.out.println("Ce divorce est impossible, " + this.nom + " n'est pas marié(e).");
    	} else {
        	Personne ancienConjoint = this.conjoint;
        	this.conjoint = null;
        	ancienConjoint.conjoint = null;
        	System.out.println(this.nom + " , marié(e) divorce de " + ancienConjoint.nom + ", marié(e)");
    	}	
	}


    public static void main(String[] args) {
        Personne p1 = new Personne("PersA");
        Personne p2 = new Personne("PersB");
        Personne p3 = new Personne();

        // Marier p1 avec p2
        p1.epouser(p2);

        // Marier p1 avec p3 (impossible)
        p1.epouser(p3);

        // Marier p3 avec p1 (impossible)
        p3.epouser(p1);

        // Marier p3 avec lui-même (impossible)
        p3.epouser(p3);

        // Divorcer p1
        p1.divorcer();

        // Divorcer p3 (impossible, p3 est célibataire)
        p3.divorcer();

        // Afficher l'état des personnes après chaque opération
        System.out.println("État après chaque opération :");
        System.out.println(p1);
        System.out.println(p2);
        System.out.println(p3);
    }
}