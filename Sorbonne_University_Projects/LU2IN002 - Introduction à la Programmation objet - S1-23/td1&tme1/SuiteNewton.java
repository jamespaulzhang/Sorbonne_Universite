public class SuiteNewton {
    private double x;
    private double epsilon;

    public SuiteNewton(double x, double epsilon) {
        this.x = x;
        this.epsilon = epsilon;
    }

    public double calculateSqrt() {
        double uPrev = x / 2; // Initial guess for the square root
        double uNext;

        while (true) {
            uNext = 0.5 * (uPrev + x / uPrev); // Compute the next iteration value
            if (Math.abs(uNext - uPrev) < epsilon) { // Check for convergence
                break;
            }
            uPrev = uNext;
        }

        return uNext;
    }

    public static void main(String[] args) {
        double x = 25; // Replace with the desired value
        double epsilon = 1e-6; // Replace with the desired precision (e.g., 1e-6 for 10^-6)

        SuiteNewton sqrtCalculator = new SuiteNewton(x, epsilon);
        double result = sqrtCalculator.calculateSqrt();
        System.out.println("The square root of " + x + " is approximately: " + result);
    }
}
