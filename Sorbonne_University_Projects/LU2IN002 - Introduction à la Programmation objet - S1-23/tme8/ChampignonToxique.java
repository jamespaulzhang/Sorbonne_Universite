public class ChampignonToxique extends Champignon implements Toxique{
	public ChampignonToxique(String nom){
		super(nom);
	}
	public double getPoids(){
		return this.poids;
	}
	public String toString(){
		String s = this.nom + " " + this.poids + "kg";
		return s;
	}
}