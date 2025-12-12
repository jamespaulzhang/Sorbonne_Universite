public class TestVehicule {
    public static void main(String[] args) {
    	Velo velo = new Velo("MyVTT",17);
		System.out.println(velo);
		velo.transporter("Paris", "Lyon");

		Voiture voiture = new Voiture ("MyCar",200,5);
		System.out.println(voiture);
		voiture.approvisionner(200);
		voiture.transporter(5,200);

		Camion camion = new Camion("MyCamion",500,10);
		System.out.println(camion);
		camion.approvisionner(400);
		camion.transporter("tuiles",500);
		
		System.out.println("========================");
        Vehicule[] parc = new Vehicule[3];
        parc[0] = velo;
        parc[1] = voiture;
        parc[2] = camion;

        for (Vehicule vehicule : parc) {
            System.out.println(vehicule.rouler(10));
        }
    }
}
