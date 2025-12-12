public abstract class Animal{
	private String nom;
	private int age;

	public Animal(String nom,int age){
		this.nom = nom;
		this.age = age;
	}

	public Animal(String nom){
		this(nom,1);
	}

	public String toString(){
		return "nom: " + nom + " age: " + age;
	}

	public void vieillir(){
		age += 1;
	}

	public abstract String crier();
}