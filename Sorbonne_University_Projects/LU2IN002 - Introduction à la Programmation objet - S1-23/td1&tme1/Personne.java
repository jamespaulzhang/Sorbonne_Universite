public class Personne{
	private String nom;
	private int age;

	public Personne(String nom,int age){
		this.nom = nom;
		this.age = age;
	}

	public String toString(){
		return "Je m’appelle " + this.nom + ", j’ai " + this.age + " ans";
	}

	public void sePresenter(){
		System.out.println(this.toString());
	}

	public int getAge(){
		return age;
	}

	public void vieillir(){
		this.age = age + 1;
	}
}