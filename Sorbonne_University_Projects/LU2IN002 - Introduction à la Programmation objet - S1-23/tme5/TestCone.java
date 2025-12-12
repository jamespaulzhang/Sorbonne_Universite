public class TestCone{
	public static void main(String[] args){
		System.out.println(Cone.getnbCones()); //Il s'affiche 0
		Cone c1 = new Cone(5.4,7.2);
		System.out.println(c1);
		Cone c2 = new Cone();
		System.out.println(c2);
		System.out.println(Cone.getnbCones()); //Il s'affiche 2
	}
}