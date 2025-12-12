public class Boa extends AnimalSansPatte{
	public Boa(String nom,int age){
		super(nom,age);
	}

	public Boa(String nom){
		super(nom);
	}

	public String toString(){
		return "Boa " + super.toString() + " sana pattes";
	}

	public void vieillir(){
		super.vieillir();
	}

	public String crier(){
		return toString() + "Siffle";
	}
}