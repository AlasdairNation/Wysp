# Behaviours to test:
# - a)Producing and consuming requests without error
# - b)graceful closure of queue, without processing further requests
# - c)expected number of calls per request
# - d)Opening and closing threads without error or side-effects
# Additional Path Coverage:
# - (See attached pathing diagram in sprint report for more)
# - [1,2,5] =  Immediate shutdown (deemed not needed as is subpath of other 2 )
# - [1,2,3,1,2,3,1,2,5] = 2 commands with arguments, then shutdown
# - [1,2,3,4,1,2,3,4,1,2,5] = 2 commands with no args, then shutdown

import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from Main.CentralFramework.projectThreadController import ProjectThreadController
from Main.ProjectHandler.projectHandler import ProjectHandlerAPI

@pytest.fixture
def projectMaster():
    class mockedAPI(ProjectHandlerAPI): #magicMock struggles to work with threading, so I made my own to allow for api call num tracking
        def __init__(self):
            self.compileNum = 0
            self.updateNum = 0
            self.runNum = 0
            self.saveProjectNum = 0
            super().__init__()

        def runProject(self,args):
            self.runNum = self.runNum + 1
            return self.runNum 
        
        def compile(self):
            self.compileNum = self.compileNum + 1
            return self.compileNum
        
        def saveProject(self, FilesToSave):
            self.saveProjectNum = self.saveProjectNum + 1
            return self.saveProjectNum 
        
        def update(self,NewText):
            self.updateNum = self.updateNum + 1
            return self.updateNum 

    return ProjectThreadController(mockedAPI())

# tests b) & d)
def test_StartAndCloseThread(projectMaster): #Also tests path [1,2,1,5]
    projectMaster.startThread()
    assert projectMaster.isRunning() 
    projectMaster.closeThread()
    assert not projectMaster.isRunning()

# tests a) b) c) d)
def test_CommandQueue(projectMaster): 
    projectMaster.startThread()
    projectMaster.requestRun("") 
    projectMaster.requestSave("") 
    projectMaster.requestUpdate("") 
    projectMaster.api = projectMaster.closeThread() # tests each major path then shuts down

    assert projectMaster.api.runNum == 1
    assert projectMaster.api.saveProjectNum == 1
    assert projectMaster.api.updateNum == 1
    assert not projectMaster.isRunning()
    
    projectMaster.startThread()
    projectMaster.requestRun("")
    projectMaster.requestRun("") # 2 loops of args test path 

    projectMaster.requestCompile() 
    projectMaster.requestCompile() # 2 loops of no args

    projectMaster.requestRun("") 
    projectMaster.requestShutdown() # args then shutdown

    projectMaster.requestUpdate("")
    projectMaster.requestSave("") # tests post-shutdown commands failing

    projectMaster.api = projectMaster.joinThread()

    assert not projectMaster.isRunning()
    assert projectMaster.api.runNum == 4 # previous loop commands + this one
    assert projectMaster.api.compileNum == 2 # ensures 2 loops
    assert projectMaster.api.saveProjectNum == 1 # previous loops commands
    assert projectMaster.api.updateNum == 1 # previous loops commands