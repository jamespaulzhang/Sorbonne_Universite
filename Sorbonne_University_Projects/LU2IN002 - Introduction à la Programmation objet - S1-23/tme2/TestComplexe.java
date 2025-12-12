public class TestComplexe{
	public static void main(String[] args){
		Complexe c = new Complexe();
		Complexe c2 = new Complexe();
		Complexe c3 = new Complexe();
		System.out.println("Le complexe c: " + c.estReel());
		System.out.println("Le complexe c2: " + c2.estReel());
		System.out.println("Le complexe c3: " + c3.estReel());
		System.out.println("Le complexe c: " + c);
		System.out.println("Le complexe c2: " + c2);
		System.out.println("Le complexe c3: " + c3);
		c.addition(c2);
		System.out.println("L'addition de c et c2: " + c);
		c.multiplication(c3);
		System.out.println("Le multiplication de (c+c2) avec c3: " + c);

		//Test i^2 = -1?
		Complexe c4 = new Complexe(0,1);
		Complexe c5 = c4;
		c4.multiplication(c5);
		System.out.println("Le complexe i^2: " + c4.estReel());
		System.out.println("i^2 = " + c4);

		//Test (1 + i) × (2 + 2i) = 4i?
		Complexe c6 = new Complexe(1,1);
		Complexe c7 = new Complexe(2,2);
		c6.multiplication(c7);
		System.out.println("Le complexe (1 + i) × (2 + 2i): " + c6.estReel());
		System.out.println("(1 + i) × (2 + 2i) = " + c6);
	}
}