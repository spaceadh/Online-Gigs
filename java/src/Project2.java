import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import java.io.IOException;
import java.util.ArrayList;

public class Project2 {
    private polynomial polynomial;
    private Complex origin;
    private double width;
    private final int NUMPIXELS = 500;
    private ArrayList<Complex> roots;
    private boolean colourIterations;

    public Project2(polynomial polynomial, Complex origin, double width) {
        this.polynomial = polynomial;
        this.origin = origin;
        this.width = width;
        this.roots = new ArrayList<>();
        this.colourIterations = false;
        setupFractal();
    }

    private void setupFractal() {
        if (polynomial.degree() < 3 || polynomial.degree() > 5) {
            throw new IllegalArgumentException("polynomial degree must be between 3 and 5 inclusive.");
        }
    }

    public void createFractal(boolean colourIterations) {
        this.colourIterations = colourIterations;

        BufferedImage image = new BufferedImage(NUMPIXELS, NUMPIXELS, BufferedImage.TYPE_INT_RGB);
        for (int j = 0; j < NUMPIXELS; j++) {
            for (int k = 0; k < NUMPIXELS; k++) {
                Complex z = pixelToComplex(j, k);
                Secant secant = new Secant(polynomial);
                secant.iterate(new Complex(0, 0), z);
                int rootIndex = getRootIndex(secant.getRoot());

                int color;
                if (colourIterations) {
                    color = getColorFromIterations(secant.getErr());
                } else {
                    color = rootIndex == -1 ? 0xFFFFFF : getColorFromIndex(rootIndex);
                }
                image.setRGB(j, k, color);
            }
        }

        try {
            File output = new File(colourIterations ? "fractal-dark.png" : "fractal-light.png");
            ImageIO.write(image, "png", output);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private Complex pixelToComplex(int j, int k) {
        double deltaZ = width / NUMPIXELS;
        double real = origin.getReal() + deltaZ * j;
        double imag = origin.getImag() - deltaZ * k; // Negative because pixel (0,0) is at the top left
        return new Complex(real, imag);
    }

    private int getRootIndex(Complex root) {
        Secant secant = new Secant(polynomial); // Initialize Secant class
        for (int i = 0; i < roots.size(); i++) {
            if (roots.get(i).subtract(root).modulus() < secant.getTOL()) {
                return i;
            }
        }
        roots.add(root);
        return -1;
    }

    private int getColorFromIndex(int index) {
        switch (index % 3) {
            case 0:
                return Color.RED.getRGB();
            case 1:
                return Color.GREEN.getRGB();
            case 2:
                return Color.BLUE.getRGB();
            default:
                return Color.WHITE.getRGB();
        }
    }

    private int getColorFromIterations(String error) {
        switch (error) {
            case "OK":
                return Color.BLACK.getRGB();
            case "ZERO":
                return Color.GRAY.getRGB();
            case "DNF":
                return Color.WHITE.getRGB();
            default:
                return Color.WHITE.getRGB();
        }
    }

    public void saveFractal(String filename) {
        // Handled in createFractal method
    }
}