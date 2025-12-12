public class Complexe{
	private double reelle;
	private double imag;

	public Complexe(double reelle,double imag){
		this.reelle = reelle;
		this.imag = imag;
	}

	public Complexe(){
		this(Math.random()*(4) + (-2),Math.random()*(4) + (-2));
	}

	public String toString(){
		if (this.reelle == 0)
			return String.format("%.2f",imag) + "i";
		if (this.reelle == 0 && this.imag == 0)
			return "0";
		if (this.imag == 0)
			return String.format("%.2f",reelle);
		if (this.imag > 0)
			return "(" + String.format("%.2f",reelle) + "+" + String.format("%.2f",imag) + "i)";
		return "(" + String.format("%.2f",reelle) + String.format("%.2f",imag) + "i)";
	}

	public String estReel(){
		if (this.imag == 0)
			return "Il est en fait reelle";
		return "Il est complexe"; 
	}

	public void addition(Complexe c){
		this.reelle += c.reelle;
		this.imag += c.imag;
	}

	public void multiplication(Complexe c){
    	double nouvelleReelle = this.reelle * c.reelle - this.imag * c.imag;
    	double nouvelleImag = this.reelle * c.imag + this.imag * c.reelle;

    	this.reelle = nouvelleReelle;
    	this.imag = nouvelleImag;
	}
}


