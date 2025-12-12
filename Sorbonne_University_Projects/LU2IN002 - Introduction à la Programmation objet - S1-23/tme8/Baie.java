public class Baie implements Toxique,Ramassable{
	public String nom;
	public double poids;
	public Baie(String nom){
		this.nom = nom;
		this.poids = Math.random()*3;
	}
	public double getPoids(){
		return this.poids;
	}
	public String toString(){
		String s = this.nom + " " + this.poids + "kg";
		return s;
	}
	public double ramassable(){
		return this.getPoids();
	}
}