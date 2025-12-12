public class Presentation {
    public static void main(String[] args) {
        Personne paul = new Personne("Paul", 25);
        Personne pierre = new Personne("Pierre", 37);

		System.out.println(paul.toString());
		System.out.println(pierre.toString());

		System.out.println("L'age de Paul est " + paul.getAge() + " ans");
		System.out.println("L'age de Pierre est " + pierre.getAge() + " ans");

        pierre.sePresenter();
        paul.sePresenter();

        for(int i = 0; i <= 19; i++){
            paul.vieillir();
        }
        System.out.println(paul.toString());
        
        int j = 0;
        while(j <= 9){
            pierre.vieillir();
            j++;
        }
        System.out.println(pierre.toString());
    }
}