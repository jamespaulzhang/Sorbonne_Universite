public class TrianglePascal{
	private int[][] tab_deux_dim;

	public TrianglePascal(int n){
		tab_deux_dim = new int[n][];
		for(int i = 0; i < tab_deux_dim.length; i++){
			tab_deux_dim[i] = new int[i+1];
		}
	}

	public void remplirTriangle(){
		for(int i = 0; i < tab_deux_dim.length; i++){
			for(int j = 0; j < tab_deux_dim[i].length; j++){
				if(j == 0 || j == i){
					tab_deux_dim[i][j] = 1;
				}else{
					tab_deux_dim[i][j] = tab_deux_dim[i - 1][j - 1] + tab_deux_dim[i - 1][j];
				}
			}
		}
	}

	public String toString(){
		StringBuilder s = new StringBuilder();
		for(int i = 0; i < tab_deux_dim.length; i++){
			for(int j = 0; j < tab_deux_dim[i].length; j++){
				s.append(tab_deux_dim[i][j] + " ");
			}
			s.append("\n");
		}
		return s.toString();
	}
}