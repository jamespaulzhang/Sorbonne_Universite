public class Orchestre {
	private Instrument[] tab;
	private static int num = 0;

	public Orchestre(int max) {
		tab = new Instrument[max];
	}

	public void ajouterInstrument(Instrument x) {
		if(num < tab.length) {
			tab[num++] = x;
		} else {
			System.out.println("C'est déjà plein. Impossible d'ajouter l'instrument");
		}
	}

	public void jouer() {
		for(int i = 0; i < num; i++) {
			tab[i].jouer();
		}
	}
}