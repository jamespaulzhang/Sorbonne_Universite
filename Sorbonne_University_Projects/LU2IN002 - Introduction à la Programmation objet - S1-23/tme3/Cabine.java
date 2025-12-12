public class Cabine{
	private int volume;
	private String couleur;

	public Cabine(int volume,String couleur){
		this.volume = volume;
		this.couleur = couleur;
	}

	public String toString(){
		return volume + "cm^3, " + couleur; 
	}

	public void setCouleur(String couleur){
		this.couleur = couleur;
	}

	public Cabine(Cabine acopier){
		this.volume = acopier.volume;
		this.couleur = acopier.couleur;
	}
}