public class Perissable{
	private double poids;
	private Date datePeremption;
	public Perissable(double poids,Date datePeremption){
		this.poids = poids;
		this.datePeremption = datePeremption;
	}

	public String toString() {
        return " de poids " + poids + " kilos est périssable le " + datePeremption.toString();
    }
}