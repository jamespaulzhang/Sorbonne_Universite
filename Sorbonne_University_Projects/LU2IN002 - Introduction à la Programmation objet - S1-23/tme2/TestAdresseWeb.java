public class TestAdresseWeb{
	public static void main(String[] args){
		AdresseWeb web1 = new AdresseWeb("ftp","site.fr","/dir");
		AdresseWeb web2 = new AdresseWeb("site.fr","/dir/page1.html");
		AdresseWeb web3 = new AdresseWeb("site.fr");
		
		System.out.println(web1);
		System.out.println(web2);
		System.out.println(web3);
	}
}