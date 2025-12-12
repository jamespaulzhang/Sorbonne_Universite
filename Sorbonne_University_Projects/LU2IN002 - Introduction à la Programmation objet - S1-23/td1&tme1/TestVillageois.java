public class TestVillageois {
    public static void main(String[] args) {
        Villageois villageois1 = new Villageois("Alice");
        Villageois villageois2 = new Villageois("Bob");
        Villageois villageois3 = new Villageois("Charlie");
        Villageois villageois4 = new Villageois("David");

        System.out.println(villageois1);
        System.out.println(villageois2);
        System.out.println(villageois3);
        System.out.println(villageois4);
            
        double poidstotale = villageois1.poidsSouleve() + villageois2.poidsSouleve() + villageois3.poidsSouleve() + villageois4.poidsSouleve();
        System.out.printf("Le poids totale est : %.2f kg\n",poidstotale);
        if (poidstotale >= 100){
            System.out.println("Ils peut déplacer le rocher qui pèse 100kg.");
        }else{
            System.out.println("Ils ne peut pas déplacer le rocher qui pèse 100kg.");
        }
    }
}
