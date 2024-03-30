#!/bin/bash

# Compile the Java files
javac -d out/production/RootFinding src/Complex.java src/polynomial.java src/Secant.java src/Project2.java src/Main.java

# Check if compilation was successful
if [ $? -eq 0 ]; then
    echo "Compilation successful."

    # Run the Main class
    java -cp out/production/RootFinding Main
else
    echo "Compilation failed."
fi