# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """

    import jpype
    from game import Directions
    from pyToJava import JavaConverter
    from searchAgents import PositionSearchProblem, CornersProblem, FoodSearchProblem

    conv = JavaConverter(problem)

    if isinstance(problem, PositionSearchProblem):
        print("Running Java DFS on PositionSearchProblem")
        j_problem = conv.position_search_problem()

    elif isinstance(problem, CornersProblem):
        j_problem = conv.corners_problem()
        print("Running Java DFS on CornersProblem")

    elif isinstance(problem, FoodSearchProblem):
        j_problem = conv.food_search_problem()
        print("Running Java DFS on FoodSearchProblem")

    else:
        raise Exception("Unknown problem type")

    # solve
    j_search = jpype.JClass("capstone.prototype.Search")()
    sol = j_search.depthFirstSearch(j_problem)
    sol_py = []

    if isinstance(problem, PositionSearchProblem) and problem.visualize:
        # display fix
        visitedList = []
        for posVisited in j_problem._visitedList:
            visitedList.append((int(posVisited.x), int(posVisited.y)))

        import __main__

        if "_display" in dir(__main__):
            if "drawExpandedCells" in dir(__main__._display):  # @UndefinedVariable
                __main__._display.drawExpandedCells(
                    visitedList
                )  # @UndefinedVariable

    for s in sol:
        if s.toString() == "NORTH":
            sol_py.append(Directions.NORTH)
        elif s.toString() == "SOUTH":
            sol_py.append(Directions.SOUTH)
        elif s.toString() == "EAST":
            sol_py.append(Directions.EAST)
        elif s.toString() == "WEST":
            sol_py.append(Directions.WEST)

    return sol_py


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    import jpype
    from game import Directions
    from pyToJava import JavaConverter
    from searchAgents import PositionSearchProblem, CornersProblem, FoodSearchProblem

    conv = JavaConverter(problem)

    if isinstance(problem, PositionSearchProblem):
        print("Running Java BFS on PositionSearchProblem")
        j_problem = conv.position_search_problem()

    elif isinstance(problem, CornersProblem):
        j_problem = conv.corners_problem()
        print("Running Java BFS on CornersProblem")

    elif isinstance(problem, FoodSearchProblem):
        j_problem = conv.food_search_problem()
        print("Running Java BFS on FoodSearchProblem")

    else:
        raise Exception("Unknown problem type")

    # solve
    j_search = jpype.JClass("capstone.prototype.Search")()
    sol = j_search.depthFirstSearch(j_problem)
    sol_py = []

    if isinstance(problem, PositionSearchProblem) and problem.visualize:
        # display fix
        visitedList = []
        for posVisited in j_problem._visitedList:
            visitedList.append((int(posVisited.x), int(posVisited.y)))

        import __main__

        if "_display" in dir(__main__):
            if "drawExpandedCells" in dir(__main__._display):  # @UndefinedVariable
                __main__._display.drawExpandedCells(
                    visitedList
                )  # @UndefinedVariable

    for s in sol:
        if s.toString() == "NORTH":
            sol_py.append(Directions.NORTH)
        elif s.toString() == "SOUTH":
            sol_py.append(Directions.SOUTH)
        elif s.toString() == "EAST":
            sol_py.append(Directions.EAST)
        elif s.toString() == "WEST":
            sol_py.append(Directions.WEST)

    return sol_py


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    import jpype
    from game import Directions
    from pyToJava import JavaConverter
    from searchAgents import PositionSearchProblem, CornersProblem, FoodSearchProblem

    conv = JavaConverter(problem)

    if isinstance(problem, PositionSearchProblem):
        print("Running Java UCS on PositionSearchProblem")
        j_problem = conv.position_search_problem()

    elif isinstance(problem, CornersProblem):
        j_problem = conv.corners_problem()
        print("Running Java UCS on CornersProblem")

    elif isinstance(problem, FoodSearchProblem):
        j_problem = conv.food_search_problem()
        print("Running Java UCS on FoodSearchProblem")

    else:
        raise Exception("Unknown problem type")

    # solve
    j_search = jpype.JClass("capstone.prototype.Search")()
    sol = j_search.uniformCostSearch(j_problem)
    sol_py = []

    if isinstance(problem, PositionSearchProblem) and problem.visualize:
        # display fix
        visitedList = []
        for posVisited in j_problem._visitedList:
            visitedList.append((int(posVisited.x), int(posVisited.y)))

        import __main__

        if "_display" in dir(__main__):
            if "drawExpandedCells" in dir(__main__._display):  # @UndefinedVariable
                __main__._display.drawExpandedCells(
                    visitedList
                )  # @UndefinedVariable

    for s in sol:
        if s.toString() == "NORTH":
            sol_py.append(Directions.NORTH)
        elif s.toString() == "SOUTH":
            sol_py.append(Directions.SOUTH)
        elif s.toString() == "EAST":
            sol_py.append(Directions.EAST)
        elif s.toString() == "WEST":
            sol_py.append(Directions.WEST)

    return sol_py


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


from util import PriorityQueue


class MyPriorityQueueWithFunction(PriorityQueue):
    """
    Implements a priority queue with the same push/pop signature of the
    Queue and the Stack classes. This is designed for drop-in replacement for
    those two classes. The caller has to provide a priority function, which
    extracts each item's priority.
    """

    def __init__(self, problem, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction  # store the priority function
        PriorityQueue.__init__(self)  # super-class initializer
        self.problem = problem

    def push(self, item, heuristic):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(
            self, item, self.priorityFunction(self.problem, item, heuristic)
        )


# Calculate f(n) = g(n) + h(n) #
def f(problem, state, heuristic):

    return problem.getCostOfActions(state[1]) + heuristic(state[0], problem)


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    import jpype

    from game import Directions
    from pyToJava import JavaConverter
    from searchAgents import PositionSearchProblem, CornersProblem, FoodSearchProblem

    conv = JavaConverter(problem)
    Heuristics = jpype.JClass("capstone.prototype.utils.heuristics.Heuristics")

    # resolve heuristic function
    jHeurFunc = None  # default: nullHeuristic
    if heuristic.__name__ == "nullHeuristic":
        pass
    elif heuristic.__name__ == "cornersHeuristic":
        jHeurFunc = Heuristics.getCornersHeuristic()
    elif heuristic.__name__ == "foodHeuristic":
        jHeurFunc = Heuristics.getFoodHeuristic()
    elif heuristic.__name__ == "manhattanHeuristic":
        jHeurFunc = Heuristics.getManhattanHeuristic()
    elif heuristic.__name__ == "euclideanHeuristic":
        jHeurFunc = Heuristics.getEuclideanHeuristic()
    else:
        raise Exception("Unknown heuristic function: " + heuristic.__name__)

    if isinstance(problem, PositionSearchProblem):
        j_problem = conv.position_search_problem()
        print("Running Java A* on PositionSearchProblem")
        # position search problems can only use manhattan, euclidean or null heuristic
        assert heuristic.__name__ in [
            "manhattanHeuristic",
            "euclideanHeuristic",
            "nullHeuristic",
        ], "Invalid heuristic function for PositionSearchProblem"

    elif isinstance(problem, CornersProblem):
        j_problem = conv.corners_problem()
        print("Running Java A* on CornersProblem")
        assert heuristic.__name__ in [
            "cornersHeuristic",
            "nullHeuristic",
        ], "Invalid heuristic function for CornersProblem"

    elif isinstance(problem, FoodSearchProblem):
        j_problem = conv.food_search_problem()
        print("Running Java A* on FoodSearchProblem")
        assert heuristic.__name__ in [
            "foodHeuristic",
            "nullHeuristic",
        ], "Invalid heuristic function for FoodSearchProblem"

    else:
        raise Exception("Unknown problem type")

    # solve
    Search = jpype.JClass("capstone.prototype.Search")()
    sol = Search.aStarSearch(j_problem, jHeurFunc)
    sol_py = []

    for s in sol:
        if s.toString() == "NORTH":
            sol_py.append(Directions.NORTH)
        elif s.toString() == "SOUTH":
            sol_py.append(Directions.SOUTH)
        elif s.toString() == "EAST":
            sol_py.append(Directions.EAST)
        elif s.toString() == "WEST":
            sol_py.append(Directions.WEST)

    return sol_py


# Editor:
# Sdi1500129
# Petropoulakis Panagiotis

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
