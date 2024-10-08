@echo off

set JAVA_DIR=java
set SOURCE_DIR=capstone
set BIN_DIR=bin
set JAR_FILE=capstone.jar
set MANIFEST_FILE=manifest.txt
set MAIN_CLASS=capstone.prototype.Search
set ORIGINAL_DIR=%cd%

rem Change directory to java directory
echo Changing working directory to .\java\
cd %JAVA_DIR%
echo Working directory: %cd%

rem Clean bin dir if it exists
if exist %BIN_DIR% (
    echo Cleaning the bin directory...
    rmdir /s /q %BIN_DIR%
)

mkdir %BIN_DIR%

rem Compile
echo Compiling Java files...
javac -d %BIN_DIR% %SOURCE_DIR%\**\*.java

rem Check if compilation was successful
if %ERRORLEVEL% neq 0 (
    echo Compilation failed. Exiting.
    exit /b 1
)

rem Create manifest file
echo Creating manifest file...
echo Main-Class: %MAIN_CLASS% > %MANIFEST_FILE%

rem Create JAR file
echo Creating JAR file...
jar cfm %JAR_FILE% %MANIFEST_FILE% -C %BIN_DIR% .
echo Build complete: %JAR_FILE%

rem Cleanup
echo Cleanup...
del %MANIFEST_FILE%
rmdir /s /q %BIN_DIR%

rem Move JAR file back to original working directory
echo Moving jar file back...
cd %ORIGINAL_DIR%
move %JAVA_DIR%\%JAR_FILE% %ORIGINAL_DIR%

echo Success!