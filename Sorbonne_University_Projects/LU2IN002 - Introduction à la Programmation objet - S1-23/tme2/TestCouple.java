public class TestCouple{
	public static void main(String[] args){
		Couple cA = new Couple(1,5);
		Couple cB = new Couple(3,7);
		cA.addition(cB);
		Couple cAPlusCB = cA;
		System.out.println(cAPlusCB.toString());
	}
}