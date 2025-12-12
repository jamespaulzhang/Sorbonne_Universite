public class Navire{
	private static int count = 0;
	private int id;
	private String pays_origin;
	private double capacite;
	private double charge;
	private Marchandise[] tab;
	private int nb_marchandise;


	public Navire(String pays_origin,double capacite){
		this.pays_origin = pays_origin;
		this.capacite = capacite;
		id = count++;
		tab = new Marchandise[10];
		nb_marchandise = 0;
	}

	public Navire(double capacite){
		this("None",capacite);
	}

	public double CalculerPoidsCharge() {
    	double poids_total = 0;

    	for (int i = 0; i < tab.length; i++) {
        	if (tab[i] != null) {
            	poids_total += tab[i].getPoids();
        	}
   	 	}

    	return poids_total;
	}

	public void ajouterMarchandise(Marchandise m) {
        if (nb_marchandise < 10 && charge + m.getPoids() <= capacite) {
            tab[nb_marchandise++] = m;
            charge += m.getPoids();
        } else if (nb_marchandise >= 10) {
            System.out.println("Il n'y a plus d'espace pour la marchandise.");
        } else {
            System.out.println("Le navire est saturé.");
        }
    }
}