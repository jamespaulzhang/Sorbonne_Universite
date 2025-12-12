public class Groupe{
	private EtreVivant[] tab;
	private int nb_vivants;

	public Groupe(int taille){
		tab = new EtreVivant[taille];
	}

	public void ajouter(EtreVivant e){
		if (nb_vivants < tab.length){
			tab[nb_vivants++] = e;
		}else{
			System.out.println("Le tableau est pleine,pas possible d'ajouer un vivant");
		}
	}

	public int nombrePasKo(){
		int compteur = 0;
		for (int i = 0;i < tab.length;i++){
			if (tab[i] != null && tab[i].estPasKO()){
				compteur++;
			}
		}
		return compteur;
	}

	public void subirDegatsGroupe(int degats){
		for (int i = 0;i < tab.length;i++){
			if (tab[i] != null){
				tab[i].subirDegats(degats);
			}	
		}
	}

	public void attaqueGroupe(Groupe g) {
        int somme = 0;
        for (EtreVivant membre : tab) {
            if (membre != null && membre.estPasKO()) {
                somme += membre.getDegats();
            }
        }

        int membresPasKo = g.nombrePasKo();
        if (membresPasKo > 0) {
            int degatsParMembre = (int)somme / membresPasKo;
            g.subirDegatsGroupe(degatsParMembre);
        }
    }


}