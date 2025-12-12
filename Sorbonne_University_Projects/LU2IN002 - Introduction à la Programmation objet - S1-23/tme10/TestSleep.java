import java.util.InputMismatchException;
import java.util.Scanner;
public class TestSleep{
    public static void main(String[] args){
        Scanner scanner = new Scanner(System.in);
        System.out.print("Entrer un entier : ");
        try{
            int x = scanner.nextInt();
            System.out.println("Attente de " + x + " seconds");
            Thread.sleep(x*1000);
            System.out.println("Fin de l'attente");
        }catch(InputMismatchException e){
            System.out.println("Le nombre est mal forme");
        }catch(InterruptedException e){
            System.out.println(e.getMessage());
        }
        scanner.close();
        
        //System.out.print("Entrer une chaine : ");
        //String chaine = scanner.next();
    }
}
