public abstract class EtreVivant{
	private int pointVie;
	private static int compteur = 0;
	public final int id;

	public EtreVivant(int pointVie){
		compteur++;
		id = compteur;
		this.pointVie = pointVie; 
	}

	public void subirDegats(int degate){
		if (pointVie - degate > 0){
			pointVie -= degate;
		}else{
			pointVie = 0;
		}
	}

	public boolean estPasKO(){
		if (pointVie > 0){
			return true;
		}
		return false;
	}

	public abstract int getDegats();

	public int getPointVie(){
		return pointVie;
	}

}