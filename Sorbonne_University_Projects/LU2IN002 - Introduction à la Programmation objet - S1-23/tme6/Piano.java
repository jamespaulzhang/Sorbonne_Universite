public class Piano extends Instrument{
	private int nb_touches;

	public Piano(int poids,int prix,int nb_touches){
		super(poids,prix);
		this.nb_touches = nb_touches;
	}

	public String toString(){
		return "Piano " + nb_touches + " touches " + super.toString();
	}

	public void jouer(){
		System.out.println("Piano : 'La Piano " + nb_touches + " touches joue'");
	}
}