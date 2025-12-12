public class TestEntierBorne {
    public static void main(String[] args){
        try{
            EntierBorne ebX = new EntierBorne((int)(Math.random()*301 - 150));
            System.out.println("ebX : " + ebX);
            EntierBorne ebY = new EntierBorne((int)(Math.random()*3));
            System.out.println("ebY : " + ebY);
            EntierBorne ebSomme = ebX.somme(ebY);
			System.out.println("La somme = " + ebSomme.toString());
            EntierBorne ebDiv = ebX.divPar(ebY);
			System.out.println("La division = " + ebDiv.toString());
        }catch(HorsBornesException e){
            System.out.println(e.getMessage());
        }catch(DivisionParZeroException e){
            System.out.println(e.getMessage());
        }
    }
}
