public class Couple{
	int x,y;
	public Couple(int x, int y){
		this.x = x;
		this.y = y;
	}

	public void addition(Couple c){
		this.x += c.x;
		this.y += c.y;
	} 


	public String toString(){
		return "(" + x + "," + y + ")";
	}
}