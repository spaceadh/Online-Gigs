public class Complex {
    private double real;
    private double imag;

    // Constructors
    public Complex() {
        this.real = 0.0;
        this.imag = 0.0;
    }

    public Complex(double real, double imag) {
        this.real = real;
        this.imag = imag;
    }

    // Getters and Setters
    public double getReal() {
        return real;
    }

    public void setReal(double real) {
        this.real = real;
    }

    public double getImag() {
        return imag;
    }

    public void setImag(double imag) {
        this.imag = imag;
    }

    // Method to get modulus
    public double modulus() {
        return Math.sqrt(real * real + imag * imag);
    }

    // Method to add two complex numbers
    public Complex add(Complex other) {
        return new Complex(this.real + other.real, this.imag + other.imag);
    }

    // Method to subtract two complex numbers
    public Complex subtract(Complex other) {
        return new Complex(this.real - other.real, this.imag - other.imag);
    }

    // Method to multiply two complex numbers
    public Complex multiply(Complex other) {
        double realPart = this.real * other.real - this.imag * other.imag;
        double imagPart = this.real * other.imag + this.imag * other.real;
        return new Complex(realPart, imagPart);
    }

    // Method to divide two complex numbers
    public Complex divide(Complex other) {
        double denominator = other.real * other.real + other.imag * other.imag;
        double realPart = (this.real * other.real + this.imag * other.imag) / denominator;
        double imagPart = (this.imag * other.real - this.real * other.imag) / denominator;
        return new Complex(realPart, imagPart);
    }

    // Method to check equality
    public boolean equals(Complex other) {
        return this.real == other.real && this.imag == other.imag;
    }

    // Method to convert complex number to string
    @Override
    public String toString() {
        return "(" + real + " + " + imag + "i)";
    }
}