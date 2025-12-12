public class Planete{
	private String nom;
 	private double rayon; //en kilometre

 	public Planete(String nom,double rayon){
 		this.nom = nom;
 		this.rayon = rayon;
 	}

 	public Planete(String nom){
 		this.nom = nom;
 		this.rayon = 1000;
 	}

 	public String toString(){
 		String s = "Planete " + nom + ",de rayon " + rayon;
 		return s;
 	}

 	public String getNom(){
 		return nom;
 	}

 	public double getRayon(){
 		return rayon;
 	}
}