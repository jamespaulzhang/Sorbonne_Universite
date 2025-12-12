public class Tracteur{
	private Cabine c;
	private Roue r1,r2,r3,r4;

	public Tracteur(Cabine c,Roue r1,Roue r2,Roue r3,Roue r4){
		this.c = c;
		this.r1 = r1;
		this.r2 = r2;
		this.r3 = r3;
		this.r4 = r4;
	}

	public String toString(){
		return "les diametres des r1-4 sont: " + r1 + " " + r2 + " " + r3 + " " + r4 + " ,et le volume et la couleur de la cabine c est: " + c;
	}

	public void peindre(String couleur){
		c.setCouleur(couleur);
	}

	public Tracteur(Tracteur acopier){
		this.c = new Cabine(acopier.c);
		this.r1 = new Roue(acopier.r1);
		this.r2 = new Roue(acopier.r2);
		this.r3 = new Roue(acopier.r3);
		this.r4 = new Roue(acopier.r4);
	}
}