public class Menagerie{
	private Animal[] tab;
	private static int num = 0;

	public Menagerie(int max){
		tab = new Animal[max];
	}

	public void ajouter(Animal a){
		if (num < tab.length){
			tab[num] = a;
			num += 1;
		}else{
			System.out.println("C'est déjà plein. Impossible d'ajouter l'animal");
		}
	}

	public String toString(){
		StringBuilder sb = new StringBuilder();
		for (int i = 0;i < num;i++){
			sb.append(tab[i].toString()).append("\n");
        }
        return sb.toString();
	}

	public void midi(){
		for (int i = 0;i < num;i++){
			tab[i].crier();
		}
	}

	public void vieillirTous(){
		for (int i = 0;i < num;i++){
			tab[i].vieillir();
		}
	}

	public static void main(String[] args) {
        Menagerie menagerie = new Menagerie(5);

        Vache vache = new Vache("Bella");
        Boa boa = new Boa("Bob");
        // Ajoutez d'autres animaux si nécessaire

        menagerie.ajouter(vache);
        menagerie.ajouter(boa);

        System.out.println(menagerie);

        menagerie.midi();
        menagerie.vieillirTous();

        System.out.println("Après le midi et le vieillissement :");
        System.out.println(menagerie);
    }
}