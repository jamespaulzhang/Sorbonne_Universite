public class Villageois{
	private String nom;
	private double poids;
	private boolean malade;
	private String ouiounon;

	public Villageois(String nom,double poids,boolean malade){
		this.nom = nom;
		this.poids = poids;
		this.malade = malade;
	}

	public Villageois(String nomVillageois){
		this.nom = nomVillageois;
		this.poids = Math.random()*(150 - 50)+50;
		this.malade = Math.random() < 0.2;
		if (malade == true){
			ouiounon = "Oui";
		}else{
			ouiounon = "Non";
		}
	}

	public double poidsSouleve(){
		if (malade == true){
			return this.poids/4;
		}else{
			return this.poids/3;
		}
	}

	public String getNom(){
		return nom;
	}

	public double getPoids(){
		return poids;
	}

	public boolean getMalade(){
		return malade;
	}

	public String toString(){
		String poid = String.format("%.2f",poids);
		double ps = poidsSouleve();
		String poidsou = String.format("%.1f",ps);
		return "Villageois : " + nom + " , Poids: " + poid + " kg, Malade: " + ouiounon + " ,peut soulever " + poidsou + " kg";
	}
}