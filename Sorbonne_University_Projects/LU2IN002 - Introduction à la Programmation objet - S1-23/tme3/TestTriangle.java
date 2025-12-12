public class TestTriangle{
	public static void main(String[] args){
		Point p1 = new Point();
		Point p2 = new Point();
		Point p3 = new Point();
		Triangle t1 = new Triangle(p1,p2,p3);
		double d = p1.distance(p2);
		System.out.println(p1);
		System.out.println(p2);
		System.out.println(d);
		System.out.println(t1);
		System.out.println("La perimetre de cet triangle est: " + t1.getPerimetre());

		Triangle t2 = new Triangle(t1);
		Triangle t3 = t1;
		System.out.println("t1 et t2 sont-ils structurellement égaux ? " + t1.equals(t2));
		System.out.println("t1 et t3 sont-ils structurellement égaux ? " + t1.equals(t3));
		p1.deplaceToi(2023,2023);
		System.out.println(t1);
		System.out.println(t2);
	}
}