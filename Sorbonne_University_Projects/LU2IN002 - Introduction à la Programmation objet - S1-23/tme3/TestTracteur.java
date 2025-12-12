public class TestTracteur{
	public static void main(String[] args){
		Roue r1 = new Roue(120);
		Roue r2 = new Roue(120);
		Roue r3 = new Roue();
		Roue r4 = new Roue();

		System.out.println(r1);
		System.out.println(r2);
		System.out.println(r3);
		System.out.println(r4);

		Cabine c = new Cabine(3,"Bleue");
		System.out.println(c);

		Tracteur t1 = new Tracteur(c,r1,r2,r3,r4);
		System.out.println(t1);

		Tracteur t2 = new Tracteur(t1);
		t2.peindre("Rouge");
		System.out.println(t2);
		System.out.println(t1);
	}
}