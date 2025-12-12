public class TestTableauMain{
	public static void main(String[] args){
		int i = 0;
		System.out.println("Il y a " + args.length + " arguments");
		for(String x : args){
			System.out.println("args[" + i + "] = " + x);
			i += 1;
		}
	}
}