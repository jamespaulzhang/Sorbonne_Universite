public class TestSegment{
	public static void main(String[] args){
		Segment seg1 = new Segment(6,8);
		Segment seg2 = new Segment(12,5);
		int longueur1 = seg1.longueur();
		int longueur2 = seg2.longueur();
		if (longueur1 > longueur2){
			System.out.println("le premier segment est plus long: " + seg1);
		}
		System.out.println("le deuxième segment est plus long: " + seg2);
	}
}