public class TestProjet{
	public static void main(String[] args){
		System.out.println(Personne.getNbPersonnes());

		Personne p1 = new Personne();
		Personne p2 = new Personne();

		System.out.println(p1);
		System.out.println(p2);

		System.out.println(Personne.getNbPersonnes());

		//Trio t1 = new Trio();
		//Trio t2 = new Trio();
		//System.out.println(t1);
		//System.out.println(t2);

		Projet projet1 = new Projet("P3X-774");
		Projet projet2 = new Projet("P3R-233");
		Projet projet3 = new Projet();
		System.out.println(projet1);
		System.out.println(projet2);
		System.out.println(projet3);

		System.out.println(Personne.getNbPersonnes());
		System.out.println(Trio.getcompteur());
		System.out.println(Projet.getNbprojet());
	}
}
