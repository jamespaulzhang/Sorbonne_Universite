public class Ballon{
	int diametre;
	String couleur;
	public Ballon(int diametre, String couleur){
		this.diametre = diametre;
		this.couleur = couleur;
	}

	public String getCouleur() {
        return couleur;
    }

    public int getDiametre() {
        return diametre;
    }
    
	public String toString(){
		return "ballon " + this.couleur + " " + this.diametre + " cm";
	}

	public static void main(String[] args){
		Ballon ballon = new Ballon(21,"bleu");
		System.out.println(ballon.toString());
	}
}