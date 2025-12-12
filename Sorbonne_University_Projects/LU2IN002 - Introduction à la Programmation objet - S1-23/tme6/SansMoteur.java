public class SansMoteur extends Vehicule{
	public SansMoteur(String marque){
		super(marque);
	}

	public String toString(){
		return super.toString() + " sans moteur";
	}
}