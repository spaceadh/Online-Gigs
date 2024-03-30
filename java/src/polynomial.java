public class polynomial {
    private Complex[] coeff;

    // Constructors
    public polynomial() {
        this.coeff = new Complex[]{new Complex(0.0, 0.0)};
    }

    public polynomial(Complex[] coeff) {
        // Removing leading zero coefficients
        int lastIndex = coeff.length - 1;
        while (lastIndex >= 0 && coeff[lastIndex].equals(new Complex(0.0, 0.0))) {
            lastIndex--;
        }
        this.coeff = new Complex[lastIndex + 1];
        System.arraycopy(coeff, 0, this.coeff, 0, lastIndex + 1);
    }

    // Method to get degree of polynomial
    public int degree() {
        return coeff.length - 1;
    }

    // Method to evaluate polynomial at a given complex number
    public Complex evaluate(Complex z) {
        Complex result = new Complex();
        for (int i = coeff.length - 1; i >= 0; i--) {
            result = result.multiply(z).add(coeff[i]);
        }
        return result;
    }
}