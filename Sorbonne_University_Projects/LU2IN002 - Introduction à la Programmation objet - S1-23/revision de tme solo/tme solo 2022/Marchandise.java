public class Marchandise{
	public final int id;
	private double poids;
	private Date datePeremption;
	private Perissable perissable;
    private NonPerissable nonPerissable;

	public Marchandise(double poids,Date datePeremption){
		id = (int)(Math.random()*1000+1);
		this.poids = poids;
		this.datePeremption = datePeremption;
        this.perissable = new Perissable(poids,datePeremption);
	}

	public Marchandise(int poids, String type) {
        id = (int)(Math.random()*1000+1);
        this.poids = poids;
        this.nonPerissable = new NonPerissable(poids,type);
    }

	public String toString() {
        if (perissable != null) {
            return "La marchandise " + id + perissable.toString();
        } else {
            return "La marchandise " + id + nonPerissable.toString();
        }
    }

    public void setPerissable(Date datePeremption) {
        this.perissable = new Perissable(poids, datePeremption);
    }

    public void setNonPerissable(String type) {
        this.nonPerissable = new NonPerissable(poids, type);
    }

    public double getPoids() {
        return poids;
    }
}