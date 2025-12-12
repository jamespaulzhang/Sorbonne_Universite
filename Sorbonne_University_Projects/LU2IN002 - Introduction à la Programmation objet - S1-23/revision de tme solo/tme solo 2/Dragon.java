public class Dragon extends EtreVivant{
	private boolean estGeant;

	public Dragon(boolean estGeant) {
        super(estGeant ? 60 : 40);
        this.estGeant = estGeant;
    }

	public int getDegats(){
		int degats = (int)getPointVie() / 3;
		return degats;
	}

	public String toString(){
		if (estGeant == true){
			return "Dragon geant - pointVie : " + getPointVie() + ",id : " + id;
		}else{
			return "Dragon - pointVie : " + getPointVie() + ",id : " + id;
		}
	}
}