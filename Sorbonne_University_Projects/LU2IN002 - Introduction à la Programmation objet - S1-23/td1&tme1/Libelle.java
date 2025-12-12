public class Libelle {
    private final String[] unites = {"zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf"};
    private final String[] onze_a_seize = {"onze", "douze", "treize", "quatorze", "quinze", "seize"};
    private final String[] dizaines = {"dix", "vingt", "trente", "quarante", "cinquante", "soixante"};
    private final String cent = "cent";

    public String traduireNombre(int nombre) {
        if (nombre < 0 || nombre >= 1000) {
            return "Nombre non pris en charge";
        }

        if (nombre >= 0 && nombre < 10) {
            return unites[nombre];
        }

        if (nombre > 10 && nombre < 17) {
            return onze_a_seize[nombre - 11];
        }

        if (nombre < 70) {
            int dizaine = nombre / 10;
            int unite = nombre % 10;
            if (unite == 1) {
                return dizaines[dizaine - 1] + " et un";
            } else if (unite == 0) {
                return dizaines[dizaine - 1];
            } else {
                return dizaines[dizaine - 1] + "-" + unites[unite];
            }
        }

        if (nombre >= 70 && nombre < 80) {
            return dizaines[5] + "-" + traduireNombre(nombre - 60);
        }

        if (nombre == 80){
            return "quatre-vingt";
        }

        if (nombre > 80 && nombre < 100){
            return "quatre-vingt" + "-" + traduireNombre(nombre - 80);
        }

        if (nombre == 100){
            return cent;
        }

        if (nombre > 100 && nombre < 200) {
            return cent + " " + traduireNombre(nombre - 100);
        }

        if (nombre < 1000) {
            int centaine = nombre / 100;
            int reste = nombre % 100;
            if (reste == 0) {
                return unites[centaine] + " " + cent;
            } else {
                return unites[centaine] + " " + cent + " " + traduireNombre(reste);
            }
        }

        return "Nombre non pris en charge";
    }

    public String traduire(int nombre) {
        return traduireNombre(nombre);
    }

    public static void main(String[] args) {
        Libelle libelle = new Libelle();
        System.out.println(libelle.traduire(0)); 
        System.out.println(libelle.traduire(9)); 
        System.out.println(libelle.traduire(10)); 
        System.out.println(libelle.traduire(11));  // "onze"
        System.out.println(libelle.traduire(16)); 
        System.out.println(libelle.traduire(17));
        System.out.println(libelle.traduire(19));
        System.out.println(libelle.traduire(20));
        System.out.println(libelle.traduire(44));
        System.out.println(libelle.traduire(69));
        System.out.println(libelle.traduire(70));
        System.out.println(libelle.traduire(79));
        System.out.println(libelle.traduire(80));
        System.out.println(libelle.traduire(88));
        System.out.println(libelle.traduire(90));
        System.out.println(libelle.traduire(99));
        System.out.println(libelle.traduire(100));
        System.out.println(libelle.traduire(101));
        System.out.println(libelle.traduire(110));
        System.out.println(libelle.traduire(111));
        System.out.println(libelle.traduire(123));  // "cent vingt-trois"
        System.out.println(libelle.traduire(199));
        System.out.println(libelle.traduire(200));
        System.out.println(libelle.traduire(231));
        System.out.println(libelle.traduire(303));
        System.out.println(libelle.traduire(321));
        System.out.println(libelle.traduire(999));
    }
}
