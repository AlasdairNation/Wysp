import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from Main.Plugins.javaPacman.handler import JVMHandler


def test_load_jvm_default():
    handler = JVMHandler()
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

    assert not error, message
