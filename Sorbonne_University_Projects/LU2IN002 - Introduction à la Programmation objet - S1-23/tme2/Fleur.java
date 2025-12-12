public class Fleur{
	private String nom;
	private String couleur;

	public Fleur(String name,String couleur){
		this.nom = name;
		this.couleur = couleur;
	 }

	//public Fleur(String nom){
		//this(nom,"rouge");
	//}

	//public Fleur(String couleur){
		//this("Marguerite",couleur);
	//}

	//public Fleur(){
		//this("Jonquille");
		//couleur = "jaune";
	//}

	public String toString(){
		return nom + " de couleur " + couleur;
	}

	public String getNom(){
		return nom;
	}
}

