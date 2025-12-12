public class Fibonacci{

	public static void main(String[] args) {
		int a = 0;
		int b = 1;
		int temp = 0;
		System.out.format("Suite de Fibonacci:      %d\t",0);
		System.out.format("%d\t",1);
		for (int i = 1; i <= 9; i++){
			temp = a + b;
			a = b;
			b = temp;
			System.out.format("%d\t",temp);
		}
	}
}