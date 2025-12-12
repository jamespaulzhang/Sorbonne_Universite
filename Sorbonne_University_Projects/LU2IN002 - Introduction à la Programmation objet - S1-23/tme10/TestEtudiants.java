import java.util.ArrayList;

public class TestEtudiants {
    public static void main(String[] args) {
        ArrayList<Etudiant> listeEtudiants = new ArrayList<>();
        Etudiant dernierEtudiant = null;
        int cpt = 0;

        for (String arg : args) {
            try {
                int note = Integer.parseInt(arg);
                System.out.print(note + " est une note, ");
                dernierEtudiant.entrerNote(note);
            } catch (NumberFormatException e) {
                if (dernierEtudiant != null) {
                    System.out.println();
                }
                System.out.print(arg + " est un nom, ");
                cpt++;
                dernierEtudiant = new Etudiant(arg);
                listeEtudiants.add(dernierEtudiant);
            } catch (TabNotesPleinException e) {
                System.out.println(e.getMessage());
            }
        }

        System.out.println("\nles " + cpt + " étudiants :");
        System.out.println(listeEtudiants);
    }
}