## **Running the executable on the Curtin Lab Machines (Recommended)** 
1. Make sure the executable is on the desktop.
2. Set the permissions of the file to allow execution: Right click -> properties -> permissions -> "Allow executing file as program". (Sometimes needs you to turn off and on again)
3. Run as a program: Right click -> "Run as program"

Note: 
Booting and creating new projects can sometimes take a while, we promise it's not frozen. We just didn't have enough to to implement loading bars.

## **Running the executable on the other Machines**
1. Ensure you have the latest versions of java, and python installed.
2. Install the latest version of TKinter: Typically achieved with running "pip install tk" inside your terminal/powershell. Any issues with running the game are likely because tkinter hasn't been installed correctly.
3. Run the program

## **Windows Specific Troubleshooting**
If you recieve the error "FileNotFoundError: capstone.jar file not found" when you attempt to run the java python game, your java path environment may not be properly configured.

1. In windows search bar search: Edit the system environmental variables
2. Click Environmental Variables
3. Under System Variables Find Path
4. Click Path then click edit
5. Click New
6. Then put the location of you JDK bin file usally C:\Program Files\Java\jdk-xx\bin Replace jdk-xx with actual version, I.E jdk-21
