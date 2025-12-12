public class SystemeSolaire{
	public static void main(String[] args){
		Planete mercure = new Planete ("Mercure",2439.7);
//Planete mercure : declaration d'une variable , new Planete... : creation d'un objet
		Planete terre = new Planete ("Terre",6378.1);
		Planete mars = new Planete ("Mars");

		double rayonmercure = mercure.getRayon();
		double rayonterre = terre.getRayon();

		System.out.println(mercure.toString());//planete Mercure de rayon 2439.7
		System.out.println(terre);
		System.out.println("Rayon de Mercure: " + rayonmercure + "km");
		System.out.println("Rayon de Terre: " + rayonterre + "km");
		System.out.println(mars);

        // Utilisation du premier constructeur avec nom et rayon spécifiés
        Planete planete1 = new Planete("Terre", 6371);

        // Utilisation du deuxième constructeur avec seulement le nom spécifié
        Planete planete2 = new Planete("Mars");

        // Affichage des informations des planètes créées
        System.out.println("Planète 1 : " + planete1.getNom() + ", Rayon : " + planete1.getRayon() + " km");
        System.out.println("Planète 2 : " + planete2.getNom() + ", Rayon : " + planete2.getRayon() + " km");
    }
} 