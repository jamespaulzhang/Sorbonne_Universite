public class Coureur{
	private int numDossard;
	private double tempsAu100;
	private boolean possedeTemoin;

	public Coureur(int numDossard){
		this.numDossard = numDossard;
		this.tempsAu100 = Math.random()*(4) + 12;
		this.possedeTemoin = false;
	}	

	public Coureur(){
		this((int)(Math.random()*(1000 - 1 + 1) + 1));
	}

	public int getNumDossard(){
		return numDossard;
	}

	public double getTempsAu100(){
		return tempsAu100;
	}

	public boolean getPossedeTemoin(){
		return possedeTemoin;
	}

	void setPossedeTemoin(boolean possedeTemoin){
		this.possedeTemoin = possedeTemoin;
	}

	public String toString(){
		String s = "Coureur " + numDossard + " tempsAu100: " + String.format("%.2f",tempsAu100) + "s au 100m possedeTemoin: ";
		if (possedeTemoin)
			return "Coureur " + numDossard + " possedeTemoin: Oui";
		return s + "Non";
	}

	void passeTemoin(Coureur c){
		System.out.println("moi,  coureur " + this.numDossard + ", je passe le temoin au coureur " + c.numDossard);
		setPossedeTemoin(this.possedeTemoin);
		setPossedeTemoin(c.possedeTemoin);		
	}

	void courir(){
		System.out.println("je suis le coureur " + this.numDossard + " et je cours");
	}
}