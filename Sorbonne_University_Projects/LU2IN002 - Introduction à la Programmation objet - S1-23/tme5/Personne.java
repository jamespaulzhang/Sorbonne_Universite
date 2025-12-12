public class Personne{
	private String nom;
	private static char lettre = 'A';
	private static int nbPersonnes = 0;

	public Personne(){
		nbPersonnes += 1;
		nom = "Individu" + lettre;
		lettre += 1;
	}

	public static int getNbPersonnes(){
		return nbPersonnes;
	}

	public String toString(){
		return nom;
	}
}