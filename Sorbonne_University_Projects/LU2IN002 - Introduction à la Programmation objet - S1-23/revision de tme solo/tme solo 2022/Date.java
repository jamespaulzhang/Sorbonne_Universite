public class Date{
	private String jour;
	private String mois;
	private String annee;

	public Date(String jour,String mois,String annee){
		this.jour = jour;
		this.mois = mois;
		this.annee = annee;
	}

	public String toString(){
		return jour + "-" + mois + "-" + annee;
	}
}