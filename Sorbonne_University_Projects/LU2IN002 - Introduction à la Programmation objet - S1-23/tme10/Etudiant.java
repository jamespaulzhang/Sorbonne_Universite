import java.util.ArrayList;

public class Etudiant {
    private String nom;
    private ArrayList<Integer> notes;

    public Etudiant(String nom) {
        this.nom = nom;
        this.notes = new ArrayList<>();
    }
    
    public String toString() {
        return nom + " " + notes;
    }

    public void entrerNote(int note) throws TabNotesPleinException {
        if (notes.size() >= 5) {
            throw new TabNotesPleinException("Le tableau de notes de l'étudiant " + nom + " est plein");
        }
        notes.add(note);
    }
}
