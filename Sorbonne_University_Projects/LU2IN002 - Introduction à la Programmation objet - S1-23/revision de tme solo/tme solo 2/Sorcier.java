public class Sorcier extends EtreVivant{
	private int intelligence;

	public Sorcier(int pointVie, int intelligence) {
        super(pointVie);
        this.intelligence = intelligence;
    }

	public int getDegats(){
		int degats = intelligence + (int)(Math.random() * 3 + 2);
		return degats; 
	}

	public String toString(){
		return "Sorcier d'intelligence " + intelligence + " - pointVie : " + getPointVie() + ", id : " + id;
	}
}