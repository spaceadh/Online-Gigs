public class Main {
    public static void main(String[] args) {
        // Define your polynomial coefficients
        Complex[] coefficients = new Complex[] {
            new Complex(-1.0, 0.0), new Complex(), new Complex(), new Complex(1.0, 0.0)
        };
        
        // Create polynomial object
        polynomial polynomial = new polynomial(coefficients);
        
        // Define origin and width for the fractal
        Complex origin = new Complex(-1.0, 1.0);
        double width = 2.0;
        
        // Create Project2 object
        Project2 fractalGenerator = new Project2(polynomial, origin, width);
        
        // Create and save the light fractal image
        fractalGenerator.createFractal(false);
        fractalGenerator.saveFractal("fractal-light.png");
        System.out.println("Light fractal image created and saved.");
        
        // Create and save the dark fractal image
        fractalGenerator.createFractal(true);
        fractalGenerator.saveFractal("fractal-dark.png");
        System.out.println("Dark fractal image created and saved.");
    }
}