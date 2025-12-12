public class Vache extends AnimalAPatte{ 
	private final double quantite_lait;

	public Vache(String nom,int age){
		super(nom,age,4);
		quantite_lait = Math.random()*25 + 5;
	}

	public Vache(String nom){
		super(nom,4);
		quantite_lait = Math.random()*25 + 5;
	}

	public String toString(){
		return "Vache " + super.toString() + " avec " + super.getPatte() + " pattes et produit le quantite du lait: " + quantite_lait;
	}

	public void vieillir(){
		super.vieillir();
	}

	public String crier(){
		return toString() + "Beuglement";
	}
}