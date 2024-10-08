# test threads 
# Methods to test
# startThread: successfully starts a thread, and completes the method inputted with given args: DONE
# closeThread: successfully closes thread without regards for completion: DONE
# joinThread: waits for completion of task, returning result successfully: DONE

# behaviour to test
# - retrieving thread result that finishes before joining (successfully gets value): DONE
# - attempt a second time (checks item is cleared and replaced): DONE
# - attempting to start a thread while another is running does nothing: DONE
# - attempting to join or close a non-existent thread does nothing but return None: DONE
# - retrieving results from method with 1+ args: DONE
# - retrieving results from method with 0 args: DONE
# - thread error exception handling: DONE

# Testing Notes: Thread safety doesn't need to be tested, as it's handled by multiprocessing.queue, which is a thread safe blocking queue.


import os
import sys
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from Main.CentralFramework.threadController import ThreadController

def test_threads():
    print("testing threads")
    tester = threadControllerTester(None)
    coreFunctionsT, waitT, doubleUpT, argT, errortT = tester.runTests()
    assert coreFunctionsT
    assert waitT
    assert doubleUpT
    assert argT
    assert errortT
    assert True

class threadControllerTester(ThreadController):
    def __init__(self,api):
        super().__init__(api)

    def runTests(self):
        return self.coreFunctionsTest(), self.waitTests(), self.doubleUpTests(), self.argTests(), self.errorTests()

    # Tests creating threads, joining threads, and recieving results from those threads
    def coreFunctionsTest(self):
        self.startThread(self.dummyTask, methodArgs=None)
        result = self.joinThread()==True
        print("Test 1: core functions test (creating & joining): ",result)
        return result

    # Tests waiting for results and interupting threads
    def waitTests(self):
        # Waiting for results
        self.startThread(self.dummyTaskWait1, methodArgs= None)
        result = self.joinThread()==True
        print("Test 2: Waiting for result: ", result)

        # Killing threads has been depreciated
        #=================================================
        # # Interrupting for results
        # self.startThread(self.dummyTaskWait1, methodArgs= None)
        # time.sleep(0.5)
        # result = result and (self.killThread()==False)
        # print("Test 3: interupting for result (may be unstable): ",result)

        # Waiting for no results
        self.startThread(self.dummyTaskWait1NoResult, methodArgs= None)
        result = result and (self.joinThread()==None)
        print("Test 4: waiting for no result: ",result)

        # Killing threads has been depreciated
        #=================================================
        # # Interrupting for no results
        # self.startThread(self.dummyTaskWait1True, methodArgs= None)
        # result = result and (self.killThread()==None)
        # print("Test 5: interupting for no result: ",result)
        
        return result

    def doubleUpTests(self):
        # attempting to run 1 thread over the other
        self.startThread(self.dummyTaskWait1NoResult, methodArgs= None)
        self.startThread(self.dummyTask, methodArgs= None)
        result = self.joinThread() == None
        print("Test 6: ensuring only 1 thread at a time: ",result)

        # attempting double join to check value retrieval
        self.startThread(self.dummyTask, methodArgs= None)
        self.joinThread()
        print("part1done")
        result = result and (self.joinThread()==None)
        print("Test 7: ensuring value clearing after thread finish: ",result)

        return result

    def argTests(self):
        # checking if task doubles value to see 1 arg usable
        self.startThread(self.dummyTaskDoubleInt, methodArgs= (8))
        result = self.joinThread()==16
        print("Test 8: changing and returning value: ",result)

        # checking if 2 args are able to be taken
        self.startThread(self.dummyTaskAdd2Int, methodArgs= (1,4))
        result = result and (self.joinThread()==5)
        print("Test 9: changing and returning two values: ",result)
        return result

    def errorTests(self):
        # closes thread if invalid method or method arguments are used
        print("--INTENTIONAL EXCEPTION THROW--")
        self.startThread(self.dummyTask, methodArgs=("blah"))
        result = self.joinThread() == None
        print("Test 10: ensures handling of thread method errors: ", result)
        return result

    def dummyTask(self): 
        return True
    
    def dummyTaskWait1(self): # Used for closing before completion, and acquiring result
        time.sleep(1)
        return True

    def dummyTaskWait1NoResult(self): # Used for acquiring value before completion
        time.sleep(1)
        return None

    def dummyTaskWait1True(self):
        time.sleep(1)
        return True

    def dummyTaskDoubleInt(self, intVal): # Used for checking args usage
        return intVal*2

    def dummyTaskAdd2Int(self, vals): # Used for checking args usage
        return vals[0]+vals[1]
