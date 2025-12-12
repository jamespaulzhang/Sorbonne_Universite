public class AA{
	private char nom;
	private int idx;
	private double poids;

	public AA(char nom,int idx){
		this.nom = nom;
		this.idx = idx;
		poids = Math.random() * 10;
	}

	public char getNom(){
		return nom;
	}

	public double getPoids(){
		return poids;
	}

	public int getIdx(){
		return idx;
	}

	public void setNom(char nouveauNom) {
    	System.out.println("Changing nom to: " + nouveauNom);
    	this.nom = nouveauNom;
	}

}