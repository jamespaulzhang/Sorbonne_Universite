public class TestVectN{
	public static void main(String[] args) {
    // Testons les constructeurs et les méthodes
    // VectN vect1 = new VectN(5); ca c'est pas possible car constructeur VectN(int n) est prive
    VectN vect2 = new VectN(3, 10);
    VectN vect3 = new VectN();
    VectN vect4 = new VectN(4, 5, 6);

    //System.out.println("Vecteur 1: " + vect1);
    System.out.println("Vecteur 2: " + vect2);
    System.out.println("Vecteur 3: " + vect3);
    System.out.println("Vecteur 4: " + vect4);

    System.out.println("Somme de vecteur 2: " + vect2.somme());

    int[] tab = vect4.getTab();
    tab[0] = 100;
    System.out.println("Vecteur 4 après modification: " + vect4);
    }
}