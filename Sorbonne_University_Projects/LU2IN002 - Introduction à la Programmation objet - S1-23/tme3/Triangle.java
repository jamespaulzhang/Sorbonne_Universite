public class Triangle{
	private Point p1;
	private Point p2;
	private Point p3;

	public Triangle(Point p1,Point p2,Point p3){
		this.p1 = p1;
		this.p2 = p2;
		this.p3 = p3;
	}

	public Triangle(){
		this(new Point(),new Point(),new Point());
	}

	public String toString(){
		return "{(" + p1.getPosx() + "," + p1.getPosy() + ") ; (" + p2.getPosx() + "," + p2.getPosy() + ") ; (" + p3.getPosx() + "," + p3.getPosy() + ")}";
	}

	public double getPerimetre(){
		return p1.distance(p2) + p2.distance(p3) + p1.distance(p3);
	}

	public Triangle(Triangle acopier){
		this(new Point(acopier.p1),new Point(acopier.p2),new Point(acopier.p3));
	}

	public boolean equals(Triangle t) {
    	return this.p1.equals(t.p1) && this.p2.equals(t.p2) && this.p3.equals(t.p3);
	}
}