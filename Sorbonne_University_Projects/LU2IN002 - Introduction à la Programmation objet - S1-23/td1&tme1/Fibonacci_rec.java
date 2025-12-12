public class Fibonacci_rec{
	public static int Fibonacci(int n){
		if (n == 0)
			return 1;
		else if (n == 1)
			return 2;
		else
			return Fibonacci(n - 1) + Fibonacci(n - 2);
	}

	public static void main(String[] args){
		int n = 0;
		while (n <= 8){
			System.out.print(Fibonacci(n) + " ");
			n += 1;	
		}
	}
}