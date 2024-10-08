import jpype


class Test:
    def __init__(self):
        print("[py] Hello, World!")
        self.run()

    def run(self):
        x = jpype.JClass("capstone.prototype.Search")
        x.main(jpype.JArray(jpype.JString)([]))


if __name__ == "__main__":
    jpype.startJVM(
        r"C:\Program Files\Java\jdk-11\bin\server\jvm.dll", classpath=["./capstone.jar"]
    )
    Test()
    jpype.shutdownJVM()
