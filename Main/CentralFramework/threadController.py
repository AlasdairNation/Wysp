# Thread Controller parent class that defines core thread controller functionality
# Called thread controller, but uses multiprocessing (I found out you can't forcefully kill threads, but you can processes)
# All thread controllers will inherit from this class
import threading
import queue
class ThreadController:
    def __init__(self, api):
        self.api = api
        self.close = threading.Event()
        self.resultQ = queue.Queue(maxsize=1)
        self.currThread = None

    # Returns current process
    def getThread(self):
        return self.currThread

    # Starts process with an inputted method, args passed to method.
    def startThread(self, method, methodArgs):
        success = True
        if ((not self.isRunning()) and (self.resultQ.empty())):
            try:
                self.currThread = threading.Thread(target = self._runThread, args= (method,methodArgs,self.resultQ) )
                self.currThread.start()
            except Exception as e:
                print("Threading error:",e,"\nAborting thread...")
                self.closeThread()
                success = False
        return success
    
        # thread Runner method that returns sets a value
    def _runThread(self, method, methodArgs,resultQ):
        result = None
        try:
            if (methodArgs==None):
                result = method()
            else:
                result = method(methodArgs) 
        except Exception as e:
            print("Error in thread: ",e,"\nAborting Thread..")
            result = None
        finally:
            resultQ.put(result)
    
    # Wrapper method for children to write over
    def closeThread(self):
        self.close.set
        return self.joinThread()

    # Blocks until process is finished, returns result if any
    def joinThread(self):
        result = None
        if (self.isRunning()):
            self.currThread.join()
        if (self.resultQ.full()):
            result = self.resultQ.get()
        self.close.clear()
        self.currThread = None
        return result
    
    # checks if process is running
    def isRunning(self):
        running = False
        if (self.currThread != None):
            running = self.currThread.is_alive()
        return running

