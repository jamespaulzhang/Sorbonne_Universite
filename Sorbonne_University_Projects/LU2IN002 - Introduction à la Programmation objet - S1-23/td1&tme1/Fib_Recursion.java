public class Fib_Recursion{
	public static void main(String[] args){
		System.out.println("斐波那契数列：\t");
		for(int i = 1; i <= 10; i++){
			int number = getNumber(i);
			System.out.print(number + "\t");
		}
	}

	public static int getNumber(int m){
		if (m == 1 || m == 2){
			return 1;
		}
		return getNumber(m - 1) + getNumber(m - 2);
	}
}