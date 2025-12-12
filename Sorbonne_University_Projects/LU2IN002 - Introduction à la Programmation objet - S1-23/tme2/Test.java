public class Test{
	public static void main(String[] args){
		Ballon bal = new Ballon(21,"bleu");
    	Joueur olive = new Joueur("Olive",bal);
    	Joueur tom = new Joueur("Tom");
		System.out.println(olive.toString());
		System.out.println(tom.toString());
	}
}