public class NonPerissable{
	private double poids;
	private String type;

	public NonPerissable(double poids,String type){
		this.poids = poids;
		this.type = type;
	}

	public String toString() {
        return " de poids " + poids + "kilos est non-périssable de type " + type;
    }
}