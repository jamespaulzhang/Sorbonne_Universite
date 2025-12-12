public class Alphabet{
	public static void main(String[] args){
		for (char c1 = '0'; c1 <= '9'; c1++){
			System.out.format("Valeur de nombre: %s, son code d'ASCII: %d\n",c1,(int)c1);
		}

		
		for (char c2 = 'A'; c2 <= 'Z'; c2++){
			System.out.format("Lettre de alphabet: %s, son code d'ASCII: %d\n",c2,(int)c2);

		}

		char c3 = '0';
		while (c3 <= '9'){
			System.out.format("Valeur de nombre: %s, son code d'ASCII: %d\n",c3,(int)c3);
			c3 += 1;
		}

		char c4 = 'A';
		while(c4 <= 'Z'){
			System.out.format("Lettre de alphabet: %s, son code d'ASCII: %d\n",c4,(int)c4);
			c4 += 1;
		}
	}
}