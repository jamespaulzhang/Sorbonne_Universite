public class Pile{
	private Assiette[] tab;
	private int nbA;

	public Pile(int taille_max){
		tab = new Assiette[taille_max];
		nbA = 0;
	}

	public boolean estVide(){
		return nbA == 0;
	}

	public boolean estPleine(){
		return nbA == tab.length;
	}

	public void empiler(Assiette a) {
        if (!estPleine()) {
            tab[nbA] = a;
            nbA++;
        }
    }
	
	public Assiette depiler() {
        if (!estVide()) {
            nbA--;
            Assiette a = tab[nbA];
            tab[nbA] = null; // Retirer l'assiette du sommet de la pile
            return a;
        }
        return null;
    }

 	public String toString() {
        StringBuilder result = new StringBuilder();
        for (int i = nbA - 1; i >= 0; i--) {
            result.append(tab[i]).append("\n");
        }
        return result.toString();
    }
}