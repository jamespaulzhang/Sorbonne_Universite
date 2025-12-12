public class Guitare extends Instrument{
	private String type;

	public Guitare(int poids,int prix,String type){
		super(poids,prix);
		this.type = type;
	}

	public String toString(){
		return "Guitare " + type + " " + super.toString();
	}

	public void jouer(){
		System.out.println("Guitare : 'La guitare " + type + " joue'");
	}
}