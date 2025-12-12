public class Roue{
	private int diametre;
	public Roue(int diametre){
		this.diametre = diametre;
	}
	public Roue(){
		this(60);
	}

	public Roue(Roue acopier){
		this.diametre = acopier.diametre;
	}
	public String toString(){
		return diametre + "cm";
	}
}