public class TestNavire {
    public static void main(String[] args) {
        Navire monNavire = new Navire("France", 10000);
        Date datePeremption = new Date("08", "02", "2003");
        Marchandise marchandise1 = new Marchandise(50,datePeremption);
        Marchandise marchandise2 = new Marchandise(70,"sucre");
        System.out.println(marchandise1);
        System.out.println(marchandise2);
        monNavire.ajouterMarchandise(marchandise1);
        monNavire.ajouterMarchandise(marchandise2);

        double poidsTotalCharge = monNavire.CalculerPoidsCharge();
        System.out.println("Poids total de la charge dans le navire : " + poidsTotalCharge + " kilos");
    }
}
