public class Vehicule{
	private static int compteur = 0;
	protected final int id;
	private String marque;
	private double distance;

	public Vehicule(String marque){
		compteur += 1;
		id = compteur;
		this.marque = marque;
	}

	public double getDistance(){
		return distance;
	}

	public String toString(){
		return id + " de marque " + marque;
	}

	public String rouler(double dis_roule){
		distance += dis_roule;
		return toString() + " a roulé " + dis_roule + " km";
	}
}