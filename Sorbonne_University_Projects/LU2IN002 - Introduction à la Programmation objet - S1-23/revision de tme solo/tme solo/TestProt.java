import java.util.Arrays;
import java.util.ArrayList;

public class TestProt {
    public static void main(String[] args) {
        // 4. Exemple d'utilisation de compteAA
        SeqProt seqProt = new SeqProt(10);
        seqProt.displayProt();
        System.out.println("Nombre d'acide aminé 'A' dans la séquence: " + seqProt.compteAA('A'));

        // 5. Créer un ArrayList de type SeqProt et stocker 30 séquences de protéines de longueur 25 acides aminés
        ArrayList<SeqProt> listProt = new ArrayList<>();
        for (int i = 0; i < 30; i++) {
            listProt.add(new SeqProt(25));
        }

        // 6. Comparer chaque séquence avec toutes les autres séquences dans l'ArrayList
        for (int i = 0; i < listProt.size(); i++) {
            for (int j = i + 1; j < listProt.size(); j++) {
                double pourcentageIdentite = listProt.get(i).compareSequences(listProt.get(j));
                System.out.println("Pourcentage d'identité entre séquence " + i + " et séquence " + j + ": " + pourcentageIdentite);
            }
        }

        // 7. Introduire un changement d'acide aminé à la position 5
        for (SeqProt seqProtInstance : listProt) {
            seqProtInstance.changerAcideAmine(5, 'X');
        }
    }
}
