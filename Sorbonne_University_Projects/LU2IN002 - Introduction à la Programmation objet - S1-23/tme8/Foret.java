import java.util.ArrayList;
public class Foret{
	private Object[][] terrain;

	public Foret(int taille){ //terrain est carre
		terrain = new Object[taille][taille];
	} 

	public boolean placer(Object obj){
		int x = (int)(Math.random()*terrain.length);
		int y = (int)(Math.random()*terrain[0].length);
		if (terrain[x][y] == null){
			terrain[x][y] = obj;
			return true;
		}else{
			return false;
		}
	}

	public String toString(){
		String s = "";
		for (int i = 0;i < terrain.length;i++){
			s += "| ";
			for (int j = 0;j < terrain[i].length;j++){
				if (terrain[i][j] != null){
					s += terrain[i][j].toString().charAt(0);
				}else{
					s += " ";
				}
			}
			s += " |\n";
		}
		return s;
	}

	public ArrayList<Champignon> ramasserChampignons(){
		ArrayList<Champignon> ary_lst = new ArrayList<Champignon>();
		for(int i = 0; i < terrain.length; i++){
			for(int j = 0; j < terrain[i].length; j++){
				if(terrain[i][j] instanceof Champignon){
					ary_lst.add((Champignon)terrain[i][j]);
					terrain[i][j] = null;
				}
			}
		}
		return ary_lst;
	}

	public ArrayList<Ramassable> ramasserTout(){
		ArrayList<Ramassable> ary_lst = new ArrayList<Ramassable>();
		for(int i = 0; i < terrain.length; i++){
			for(int j = 0; j < terrain[i].length; j++){
				if(terrain[i][j] instanceof Ramassable){
					ary_lst.add((Ramassable)terrain[i][j]);
					terrain[i][j] = null;
				}
			}
		}
		return ary_lst;
	}

	public void ramasser(Panier p){
		ArrayList<Ramassable> ary_lst = ramasserTout();
		for(Ramassable o : ary_lst){
			p.add(o);
		}
	}

}