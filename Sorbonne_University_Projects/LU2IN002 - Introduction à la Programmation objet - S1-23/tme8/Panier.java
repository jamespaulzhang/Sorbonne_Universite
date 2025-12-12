import java.util.ArrayList;
public class Panier extends ArrayList<Ramassable>{
	public double poidsMax;
	public Panier(double poidsMax){
		this.poidsMax = poidsMax;
	}

	public double getPoids(){
		double somme = 0.;
		for(Ramassable o : this){
			somme += o.getPoids();
		}
		return somme;
	}

	public boolean add(Ramassable r){
		if(poidsMax < (this.getPoids() + r.getPoids())){
			System.out.println(r.toString() + " n’est pas ajouté au panier.");
		} else {
			super.add(r);
			System.out.println(r.toString() + " est ajouté au panier.");
			return true;
		}
		return false;
	}
	public int compterToxiques(){
		int n = 0;
		for(Ramassable o : this){
			if(o instanceof Toxique){
				n++;
			}
		}
		return n;
	}
	public String toString(){
		return "Pannier contenant " + this.size() + " objets, dont " + this.compterToxiques() + " toxiques (" + this.getPoids() + "kg sur " + this.poidsMax + "kg)";
	}
}