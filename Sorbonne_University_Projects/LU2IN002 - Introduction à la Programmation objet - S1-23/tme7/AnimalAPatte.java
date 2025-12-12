public abstract class AnimalAPatte extends Animal{
	private final int patte;

	public AnimalAPatte(String nom,int age,int patte){
		super(nom,age);
		this.patte = patte;
	}

	public AnimalAPatte(String nom,int patte){
		this(nom,1,patte);
	}

	public String toString(){
		return super.toString() + " c'est un animal a patte";
	}

	public int getPatte(){
		return patte;
	}
}