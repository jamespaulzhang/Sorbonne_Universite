public class Velo extends SansMoteur{
	private int nb_vitesses;
	public Velo(String marque,int nb_vitesses){
		super(marque);
		this.nb_vitesses = nb_vitesses;
	}

	public String toString(){
		return "Vélo " + super.toString() + " " + nb_vitesses + " vitesses";
	}

	public void transporter(String depart,String arrivee){
		System.out.println("Le velo " + id + " se déplace de " + depart + " à " + arrivee);
	}
}