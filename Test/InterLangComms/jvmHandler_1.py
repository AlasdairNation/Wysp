import traceback

# ImportError hotfix
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from Main.Plugins.javaPacman.handler import JVMHandler


def test_load_jvm_valid_path():
    # replace with your own path if testing locally
    path = r"C:\Program Files\Java\jre1.8.0_311_copy\bin\server\jvm.dll"
    handler = JVMHandler(path)
    error = False
    message = ""

    try:
        handler.start()
        handler.stop()
    except OSError as e:
        error = True
        message = "Error during JVM start"
        traceback.print_exc()
    except RuntimeError:
        error = True
        message = "Error during JVM stop"

    assert not error, message


def test_load_jvm_invalid_path():
    handler = JVMHandler("invalid_path")
    error = False
    message = ""

    try:
        handler.start()
        handler.stop()
    except OSError:
        error = True
        message = "Error during JVM start"
    except RuntimeError:
        error = True
        message = "Error during JVM stop"

    assert error, message
