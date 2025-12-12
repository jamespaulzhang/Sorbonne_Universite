public class TestCoureur{
	public static void main(String[] args){
		Coureur c1 = new Coureur();
		Coureur c2 = new Coureur();
		Coureur c3 = new Coureur();
		Coureur c4 = new Coureur();

		System.out.println("Faire courir en relais 4 fois 100m les quatre coureurs dans l'ordre c1,c2,c3,c4");

		c1.setPossedeTemoin(true);
		System.out.println(c1);
		c1.courir();
		c1.passeTemoin(c2);
		c1.setPossedeTemoin(false);
		System.out.println(c1);

		c2.setPossedeTemoin(true);
		System.out.println(c2);
		c2.courir();
		c2.passeTemoin(c3);
		c2.setPossedeTemoin(false);
		System.out.println(c2);

		c3.setPossedeTemoin(true);
		System.out.println(c3);
		c3.courir();
		c3.passeTemoin(c4);
		c3.setPossedeTemoin(false);
		System.out.println(c3);

		c4.setPossedeTemoin(true);
		System.out.println(c4);
		c4.courir();

		double temps_total = c1.getTempsAu100() + c2.getTempsAu100() + c3.getTempsAu100() + c4.getTempsAu100();
		System.out.println("Temps total pour 400m est: " + String.format("%.2f",temps_total) + "s");
	}
} 