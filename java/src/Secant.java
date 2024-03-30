public class Secant {
    private polynomial polynomial;
    private final int MAXITER = 1000;
    private final double TOL = 1e-10;
    private Complex root;
    private String err;

    public Secant(polynomial polynomial) {
        this.polynomial = polynomial;
        this.root = new Complex();
        this.err = "";
    }

    public void iterate(Complex z0, Complex z1) {
        Complex f0 = polynomial.evaluate(z0);
        Complex f1 = polynomial.evaluate(z1);

        for (int i = 0; i < MAXITER; i++) {
            if (f1.equals(f0)) {
                this.err = "ZERO";
                return;
            }

            Complex temp = z1.subtract(z0).divide(f1.subtract(f0));
            z0 = z1;
            f0 = f1;
            z1 = z1.subtract(temp.multiply(f1));

            if (z1.subtract(z0).modulus() < TOL && polynomial.evaluate(z1).modulus() < TOL) {
                this.root = z1;
                this.err = "OK";
                return; // Corrected here: added semicolon
            }
        }

        this.err = "DNF";
    }

    public Complex getRoot() {
        return root;
    }

    public String getErr() {
        return err;
    }
    public double getTOL() {
        return TOL;
    }
}