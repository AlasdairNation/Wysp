import os, platform, sys
from pathlib import Path


class JVMHandler:
    def __init__(self, jpypeDir: str = None):
        self.jpypeDir = jpypeDir
        self.path = ''
    
            
    def start(self):
        if self.jpypeDir and self.jpypeDir not in sys.path:
            sys.path.append(self.jpypeDir) 
        print(f"RUN! {self.jpypeDir}")
        try:
            import jpype
        except ImportError:
            pass
        
        if self.jpypeDir:
            self.path = self.jpypeDir
        else:
            self.path = jpype.getDefaultJVMPath()

        # look for files named "capstone.jar"
        jar_files = list(Path(__file__).parent.glob("capstone.jar"))
        if not jar_files:
            raise FileNotFoundError("capstone.jar file not found")
        
        # start JVM
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Dynamically construct the path to the libjvm.so file relative to the current directory 
        if os.path.exists(os.path.join(current_dir, 'JVM', 'jdk')):
            self.path = os.path.join(current_dir, "JVM", 'jdk', 'lib', 'server', "libjvm.so")
            
        else: 
            self.path = jpype.getDefaultJVMPath()
        
        jpype.startJVM(
            self.path,
            classpath=jar_files,
            convertStrings=False
        )

    def stop(self):
        if self.jpypeDir and self.jpypeDir not in sys.path:
            sys.path.append(self.jpypeDir) 
        try:
            import jpype
        except ImportError:
            pass
        jpype.shutdownJVM()


if __name__ == "__main__":
    # example usage
    p = input("JVM path (leave empty for default): ")
    if not p:
        handler = JVMHandler()
    else:
        handler = JVMHandler(p)

    try:
        # start
        handler.start()
        print("JVM started successfully")

        # stop
        handler.stop()
        print("JVM stopped successfully")

    except OSError as e:
        # error when starting JVM
        print("Error starting JVM:", e)

    except RuntimeError as e:
        # error when stopping JVM
        print("Error stopping JVM:", e)

    except Exception as e:
        # any other unexpected error
        import traceback

        print("Unexpected error:", e)
        traceback.print_exc()
