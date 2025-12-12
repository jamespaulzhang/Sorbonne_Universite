public class TestOrchestre{
	public static void main(String[] args){
		Piano p1 = new Piano(300,700,88);
		Guitare g1 = new Guitare(5,200,"classique");

		System.out.println(p1);
		System.out.println(g1);

		//p1.jouer();
		//g1.jouer();

		Orchestre o1 = new Orchestre(10);
		o1.ajouterInstrument(p1);
		o1.ajouterInstrument(g1);
		o1.jouer();
	}
}