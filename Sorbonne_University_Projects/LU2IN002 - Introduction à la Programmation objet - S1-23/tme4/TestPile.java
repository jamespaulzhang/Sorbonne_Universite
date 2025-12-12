public class TestPile {
    public static void main(String[] args) {
        Pile pile = new Pile(3);

        pile.empiler(new Assiette(1));
        pile.empiler(new Assiette(2));
        pile.empiler(new Assiette(3));

        System.out.println(pile.toString());

        pile.depiler();

        System.out.println(pile.toString());

        pile.empiler(new Assiette(4));
        pile.empiler(new Assiette(5));

        System.out.println(pile.toString());

        pile.depiler();
        pile.depiler();
        pile.depiler();
        pile.depiler(); // Dépiler une quatrième fois (la pile sera vide)

        System.out.println(pile.toString());
    }
}