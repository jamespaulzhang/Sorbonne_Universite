package org.o7planning.tutorial.am.privatedemo;

public class Person{
	public String name;
	private String secret;

	public Person(String name){
		this.name = name;
	}

	public void showSecret(){
		System.out.println("Secret: " + this.secret);
	}

	class Diary{
		public void Logging(){
			System.out.println("Secret: " + secret);
		}
	}
}