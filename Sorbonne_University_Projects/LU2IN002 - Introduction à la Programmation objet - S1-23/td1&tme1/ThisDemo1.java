public class ThisDemo1{
	int number;
	public ThisDemo1 increment(){
		number++;
		return this; //返回类自身的引用，通过this这个关键字返回自身这个对象
	}
	private void print(){
		System.out.println("number = " + number);
	}
	public static void main(String[] args){
		ThisDemo1 tt = new ThisDemo1();
		tt.increment().increment().increment().print(); //然后在一条语句里面实现多次的操作，还是贴出来
	}
}