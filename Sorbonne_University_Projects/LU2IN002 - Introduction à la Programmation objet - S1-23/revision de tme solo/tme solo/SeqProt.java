import java.util.ArrayList;
public class SeqProt extends Seq{
	private ArrayList<AA> pprot;

	public SeqProt(int len){
		super(len);
		pprot = new ArrayList<AA>();

		String[] sq = super.getSq();
		for (int i = 0; i < sq.length; i++) {
            char nomAA = sq[i].charAt(0);
            int idxAA = i + 1;
            AA aa = new AA(nomAA, idxAA);
            pprot.add(aa);
        }
	}

	public void displayProt(){
		for(AA o : pprot){
			System.out.println("Nom " + o.getNom() + " ID :" + o.getIdx() + " avec poids " + o.getPoids() + "kg");
		}
	}

	public int compteAA(char Z){
		int compteur = 0;
		for(AA o : pprot){
			if (o.getNom() == Z){
				compteur++;
			}
		}
		return compteur;
	}

	public double compareSequences(SeqProt other) {
    	int identicalCount = 0;
    	for (int i = 0; i < this.getSq().length; i++) {
        	if (this.getSq()[i].charAt(0) == other.getSq()[i].charAt(0)) {
            	identicalCount++;
        	}
    	}
    	return (double) identicalCount / this.getSq().length * 100;
	}

	public String getSqAsString() {
        StringBuilder sb = new StringBuilder();
        for (AA aa : pprot) {
            sb.append(aa.getNom());
        }
        return sb.toString();
    }

    public void changerAcideAmine(int position, char nouveauNom) {
        System.out.println("Avant modification: " + getSqAsString());

        // Modify the existing AA instance directly
        pprot.get(position - 1).setNom(nouveauNom);

        System.out.println("Après modification: " + getSqAsString());
    }
}
