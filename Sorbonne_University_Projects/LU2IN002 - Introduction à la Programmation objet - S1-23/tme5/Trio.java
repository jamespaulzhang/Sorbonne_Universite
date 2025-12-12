public class Trio{
	private int numero;
	private static int compteur = 0;
	private Personne[] trio;

	public Trio(){
		trio = new Personne[3];
		trio[0] = new Personne();
		trio[1] = new Personne();
		trio[2] = new Personne();
		compteur += 1;
		numero = compteur;
	}

	public String toString(){
		return "Trio " + numero + " : " + trio[0] + " " + trio[1] + " " + trio[2];
	}

	public static int getcompteur(){
		return compteur;
	}
}