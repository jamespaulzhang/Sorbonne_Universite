public class Projet{
	private String projet;
	private Trio t;
	private static int nbprojet = 0;

	public Projet(String projet){
		t = new Trio();
		this.projet = projet;
		nbprojet += 1;
	}

	public Projet(){
		this(Alea.chaine());
	}

	public String toString(){
		return "Projet " + projet + " " + t;
	}

	public static int getNbprojet(){
		return nbprojet;
	}

}