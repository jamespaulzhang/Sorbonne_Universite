public class TestForet{
	public static void main(String[] args){
		Foret f = new Foret(10);
		Panier p = new Panier(8.);
		for(int i = 0; i < 10; ){
			double tmp = Math.random()*1;
			if(tmp >= 0.8){
				if(f.placer(new Champignon("Cèpe"))){
					i++;
				}
			}else if(tmp >= 0.5){
				if(f.placer(new Baie("Baie"))){
					i++;
				}
			}else if(tmp >= 0.3){
				if(f.placer(new ChampignonToxique("Amanite"))){
					i++;
				}
			}else {
				if(f.placer(new Arbre("Pin"))){
					i++;
				}
			}
		}
		System.out.println(f.toString() + "\n========================");
		f.ramasser(p);
		System.out.println(p.toString());
		System.out.println(f.toString());
	}
}