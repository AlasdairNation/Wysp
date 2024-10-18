#!/bin/bash

JAVA_DIR="java"
SOURCE_DIR="capstone"
BIN_DIR="bin"
JAR_FILE="capstone.jar"
MANIFEST_FILE="manifest.txt"
MAIN_CLASS="capstone.prototype.Search"
ORIGINAL_DIR="$(pwd)"

# Switch to java directory
echo "Changing working directory to ./$JAVA_DIR/"
cd "$JAVA_DIR" || { echo "Failed to change directory to $JAVA_DIR"; exit 1; }
echo "Working directory: $(pwd)"

# Clean bin dir if exists
if [ -d "$BIN_DIR" ]; then
    echo "Cleaning the bin directory..."
    rm -rf "$BIN_DIR"
fi

mkdir -p "$BIN_DIR"

# Compile Java files
echo "Compiling Java files..."
find "$SOURCE_DIR" -name "*.java" > sources.txt
javac -d "$BIN_DIR" @sources.txt

# Check if compilation was successful
if [ $? -ne 0 ]; then
    echo "Compilation failed. Exiting."
    exit 1
fi

# Create manifest file
echo "Creating manifest file..."
echo "Main-Class: $MAIN_CLASS" > "$MANIFEST_FILE"

# Create JAR file
echo "Creating JAR file..."
jar cfm "$JAR_FILE" "$MANIFEST_FILE" -C "$BIN_DIR" .
echo "Build complete: $JAR_FILE"

# Cleanup
echo "Cleanup..."
rm "$MANIFEST_FILE"
rm -rf "$BIN_DIR"
rm sources.txt

# Move JAR file back to original working directory
echo "Moving jar file back..."
cd "$ORIGINAL_DIR" || exit
mv "$JAVA_DIR/$JAR_FILE" "$ORIGINAL_DIR"

echo "Success!"
