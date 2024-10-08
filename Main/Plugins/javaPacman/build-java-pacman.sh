#!/bin/bash

JAVA_DIR="java"
SOURCE_DIR="capstone"
BIN_DIR="bin"
JAR_FILE="capstone.jar"
MANIFEST_FILE="manifest.txt"
MAIN_CLASS="capstone.prototype.Search"
ORIGINAL_DIR="$(pwd)"

# switch to java directory
echo "Changing working directory to ./java/"
cd "$JAVA_DIR"
echo "Working directory: $(pwd)"

# clean bin dir if exist
if [ -d "$BIN_DIR" ]; then
    echo "Cleaning the bin directory..."
    rm -rf "$BIN_DIR"
fi

mkdir -p "$BIN_DIR"

# compile
echo "Compiling Java files..."
javac -d "$BIN_DIR" "$SOURCE_DIR"/**/*.java

# check if compilation was successful
if [ $? -ne 0 ]; then
    echo "Compilation failed. Exiting."
    exit 1
fi

# manifest
echo "Creating manifest file..."
echo "Main-Class: $MAIN_CLASS" > "$MANIFEST_FILE"

# jar file
echo "Creating JAR file..."
jar cfm "$JAR_FILE" "$MANIFEST_FILE" -C "$BIN_DIR" .
echo "Build complete: $JAR_FILE"

# cleanup
echo "Cleanup..."
rm "$MANIFEST_FILE"
rm -rf "$BIN_DIR"

# move jar back to original working dir
echo "Moving jar file back..."
cd "$ORIGINAL_DIR"
mv "$JAVA_DIR/$JAR_FILE" "$ORIGINAL_DIR"

echo "Success!"
