public abstract class AnimalSansPatte extends Animal{
	public AnimalSansPatte(String nom,int age){
		super(nom,age);
	}

	public AnimalSansPatte(String nom){
		super(nom,1);
	}

	public String toString(){
		return super.toString() + " c'est un animal sans patte";
	}
}