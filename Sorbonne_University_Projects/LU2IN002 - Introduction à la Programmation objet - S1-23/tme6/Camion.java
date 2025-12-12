public class Camion extends AMoteur {
    private double volumeTransporte;

    public Camion(String marque,double reservoir,double volumeTransporte) {
        super(marque,reservoir);
        this.volumeTransporte = volumeTransporte;
    }

    public void transporter(String materiau, int km) {
        double ess = super.getEssence();
		double dis = super.getDistance();

		if(super.enPanne()) {
			System.out.println("Le camion " + id + " n’a plus plus d’essence!");
		} else if(ess- km < 0) {
			dis += ess;
        	ess = 0;
			System.out.println("Le camion " + id + " n'a pas assez d'essence pour rouler " + km + " km." + " Il s'arrete à " + dis + " km");
		} else {
			ess -= km;
			dis += km;
			System.out.println("Le camion " + id + " a transporté des " + materiau + " sur " + km + " km");
		}
    }

    public String toString() {
        return "Camion " + super.toString() + " " + volumeTransporte + " m^3 transportés";
    }
}
