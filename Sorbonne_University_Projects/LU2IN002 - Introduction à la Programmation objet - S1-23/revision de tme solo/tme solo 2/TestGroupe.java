public class TestGroupe{
	public static void main(String[] args){
		Groupe groupeSorcier = new Groupe(10);
		Sorcier s1 = new Sorcier(20,4);
		Sorcier s2 = new Sorcier(20,6);
		Sorcier s3 = new Sorcier(20,8);
		groupeSorcier.ajouter(s1);
		groupeSorcier.ajouter(s2);
		groupeSorcier.ajouter(s3);

		Groupe groupeDragon = new Groupe(3);
		Dragon d = new Dragon(false);
		groupeDragon.ajouter(d);

		System.out.println("Le groupe est compose de: ");
		System.out.println(s1);
		System.out.println(s2);
		System.out.println(s3);
		System.out.println("Le groupe est compose de: ");
		System.out.println(d);

		groupeSorcier.attaqueGroupe(groupeDragon);
		groupeDragon.attaqueGroupe(groupeSorcier);
		System.out.println(s1);
		System.out.println(s2);
		System.out.println(s3);
		System.out.println(d);
	}
}