public class Point{
	private int posx;
	private int posy;

	public Point(int posx,int posy){
		this.posx = posx;
		this.posy = posy;
	}

	public Point(){
		this((int)(Math.random()*10),(int)(Math.random()*10));
	}

	public void setPosx(int posx){
		this.posx = posx;
	}

	public void setPosy(int posy){
		this.posy = posy;
	}

	public int getPosx(){
		return posx;
	}

	public int getPosy(){
		return posy;
	}

	public String toString(){
		return "(" + posx + ", " + posy + ")";
	}

	public double distance(Point p) {
    	int dx = p.getPosx() - this.getPosx();
    	int dy = p.getPosy() - this.getPosy();
    	return Math.sqrt(dx * dx + dy * dy);
    }

    public void deplaceToi(int newx, int newy){
    	this.posx = newx;
    	this.posy = newy;
    }

    public Point(Point acopier){
    	this(acopier.posx,acopier.posy);
    }
}