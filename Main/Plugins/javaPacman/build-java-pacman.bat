@echo off
setlocal enabledelayedexpansion

set JAVA_DIR=java
set SOURCE_DIR=capstone
set BIN_DIR=bin
set JAR_FILE=capstone.jar
set MANIFEST_FILE=manifest.txt
set MAIN_CLASS=capstone.prototype.Search
set ORIGINAL_DIR=%cd%

rem Switch to java directory
echo Changing working directory to .\java\
cd %JAVA_DIR%
echo Working directory: %cd%

rem Clean bin directory if it exists
if exist %BIN_DIR% (
    echo Cleaning the bin directory...
    rmdir /s /q %BIN_DIR%
)
mkdir %BIN_DIR%

rem Gather all Java files
set JAVA_FILES=
for /r %SOURCE_DIR% %%f in (*.java) do (
    set JAVA_FILES=!JAVA_FILES! "%%f"
)

rem Compile Java files
echo Compiling Java files...
javac -d %BIN_DIR% !JAVA_FILES! 2> compile_errors.txt

rem Check if compilation was successful
if %ERRORLEVEL% neq 0 (
    echo Compilation failed. Exiting.
    echo ==== Compilation Errors ====
    type compile_errors.txt
    del compile_errors.txt
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

rem Move JAR file back to original working dir
echo Moving JAR file back...
cd %ORIGINAL_DIR%
move %JAVA_DIR%\%JAR_FILE% %ORIGINAL_DIR%

echo Success!
endlocal
