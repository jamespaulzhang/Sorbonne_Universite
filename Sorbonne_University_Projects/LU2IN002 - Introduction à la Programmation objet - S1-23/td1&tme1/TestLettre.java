public class TestLettre {
    public static void main(String[] args) {
        for (char c = 'a'; c <= 'z'; c++) {
        	Lettre carac1 = new Lettre(c);
            System.out.print(carac1.getCodeAscii() + " ");
        }

        System.out.println();
        for (char c = 'a'; c <= 'z'; c++) {
        	Lettre carac2 = new Lettre(c);
        	System.out.print(carac2.getCarac() + " ");
        	if ((carac2.getCarac() - 'a' + 1) % 5 == 0) 
            	System.out.println(); // Pass to the next line after every 5 characters
        }
    }
}
