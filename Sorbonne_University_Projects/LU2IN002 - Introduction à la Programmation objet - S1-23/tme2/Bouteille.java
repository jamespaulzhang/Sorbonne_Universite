public class Bouteille{
	private double volume; //Volume du liquide dans la bouteille

	public Bouteille(double volume){
		this.volume = volume;
	}

	public Bouteille(){
		this(1.5);
	}

	public void remplir(Bouteille b){
		this.volume = b.volume;
	}

	//public void remplir(double volume){
		//this.volume = volume;
	//}

	public String toString(){
		return("Volume = " + volume);
	}

}