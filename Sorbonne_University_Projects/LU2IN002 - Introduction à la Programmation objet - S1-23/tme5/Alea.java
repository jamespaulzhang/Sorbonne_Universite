public class Alea{
	//mettre un constructeur private pour empecher creer d'instance dans l'autre classe
	private Alea(){
	}

	public static char lettre(){
		return (char)(Math.random()*('z' - 'a' + 1) + 'a');
	}

	public static String chaine(){
		String s = "";
		for(int i = 0; i < 10; i++){
			s += lettre();
		}
		return s;
	}

	public static void main(String[] args){
		System.out.println(Alea.lettre());
		System.out.println(Alea.chaine());
	}
}