public class AMoteur extends Vehicule{
	private double reservoir;
	private double essence;
	
	public AMoteur(String marque,double reservoir){
		super(marque);
		this.reservoir = reservoir;
	}

	public String toString(){
		return super.toString() + " avec moteur"; 
	}

	public void approvisionner(double nbLitres) {
		if(reservoir >= (essence + nbLitres)) {
			essence += nbLitres;
		} else {
			System.out.println("Vous avez approvisionner trop. Essayez une autre fois.");
		}
	}

    public boolean enPanne() {
        return essence <= 0;
    }

    public double getEssence(){
    	return essence;
    }
}