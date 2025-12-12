public class Voiture extends AMoteur{
	private int places;
	public Voiture(String marque,double reservoir,int places) {
        super(marque,reservoir);
        this.places = places;
    }

	public String toString() {
        return "Voiture " + super.toString() + " " + places + " places";
    }

	public void transporter(int nbPers,int km){
		double ess = super.getEssence();
		double dis = super.getDistance();
		if (ess - km >= 0 && places - nbPers >= 0){
			System.out.println("La voiture " + id + " transporte " + nbPers + " personne sur " + km + " km");
			ess -= km;
			dis += km;
			places -= nbPers;
		} else if(ess - km < 0 && places - nbPers >= 0) {
        	dis += ess;
        	ess = 0;
			System.out.println("La voiture " + id + " n'a pas assez d'essence pour rouler " + km + " km." + " Il s'arrete à " + dis + " km");
		} else if(super.enPanne()){
			System.out.println("La voiture " + id + " n’a plus d’essence !");
		} else if(places - nbPers < 0){
			System.out.println("Il y a pas assez de places");
		}
	}
}