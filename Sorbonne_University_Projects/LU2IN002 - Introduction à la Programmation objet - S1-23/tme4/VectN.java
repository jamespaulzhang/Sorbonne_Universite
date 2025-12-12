public class VectN{
	private int[] tab;

	private VectN(int n){
		tab = new int[n];
	}

	public VectN(int n, int valMax){
		this(n);
		for(int i = 0; i < tab.length; i++){
			tab[i] = (int)(Math.random()*(valMax+1)+0);
		}
	}

	public VectN(){
		this(5,9);
	}

	public VectN(int a,int b,int c){
		this(3);
		tab[0] = a;
		tab[1] = b;
		tab[2] = c;
	}

	public int somme(){
		int som = 0;
		for(int x : tab){
			som += x;
		}
		return som;
	}

	public String toString(){
		String s = "";
		int i = 0;
		for (int x : tab){
			s += x ;
			if(i < tab.length-1){
				s += ", ";
				i+=1;
			}
		}
		return "[" + s + "]";
	}

	public int[] getTab(){
		int[] tab2 = new int[tab.length];
		for (int i = 0; i < tab.length; i++){
			tab2[i] = tab[i];
		}
		return tab2;
	}
}