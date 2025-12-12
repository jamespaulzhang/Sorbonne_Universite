public class Segment{
	private int extX;
	private int extY;

	public Segment(int extX,int extY){
		this.extX = extX;
		this.extY = extY;
	}

	public int longueur(){
		if (extX < extY){
			return extY - extX;
		}
		return extX - extY;
	}

	public String toString(){
		return "[" + extX + "," + extY +"]";
	}
}