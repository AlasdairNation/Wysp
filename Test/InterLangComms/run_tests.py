# Run this file instead of running pytest on this directory
import os
from pathlib import Path

# jpype jvm cannot be started twice in the same process, so tests
# must be run in separate processes
current = str(Path(__file__).resolve().parents[0]) + "\\"
t1 = "pytest " + current + "jvmHandler_1.py"
t2 = "pytest " + current + "jvmHandler_2.py"

os.system(t1)
os.system(t2)
