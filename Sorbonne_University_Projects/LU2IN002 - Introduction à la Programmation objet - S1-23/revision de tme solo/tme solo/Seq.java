public abstract class Seq{
	private String[] sq;
	public String[] acidesAmines = {"A","C","D","E","F","G","H","I","K","L","M","N","P","O","R","S","T","V","W","Y"};

	public Seq(int len){
		sq = new String[len];
        for (int i = 0; i < len; i++){
            sq[i] = acidesAmines[(int)(Math.random() * acidesAmines.length)];
        }
    }

	public String[] getSq() {
        return sq;
    }
}