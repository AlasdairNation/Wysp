package capstone.prototype;

import java.util.*;
import java.util.function.BiFunction;

// import everything so that they all files get compiled
// TODO: finish
// capstone.prototype.game
import capstone.prototype.game.Actions;
import capstone.prototype.game.AgentState;
import capstone.prototype.game.Configuration;
import capstone.prototype.game.GameState;
import capstone.prototype.game.GameStateData;
import capstone.prototype.game.GhostRules;
import capstone.prototype.game.PacmanRules;

// capstone.prototype.problem
import capstone.prototype.problem.AnyFoodSearchProblem;
import capstone.prototype.problem.AStarCornersAgent;
import capstone.prototype.problem.AStarFoodSearchAgent;
import capstone.prototype.problem.ClosestDotSearchAgent;
import capstone.prototype.problem.CornersProblem;
import capstone.prototype.problem.FoodSearchProblem;
import capstone.prototype.problem.PositionSearchProblem;
import capstone.prototype.problem.SearchProblem;
import capstone.prototype.problem.StayEastSearchAgent;
import capstone.prototype.problem.StayWestSearchAgent;

// capstone.prototype.problem.states
import capstone.prototype.problem.states.CornersProblemState;
import capstone.prototype.problem.states.FoodSearchProblemState;
import capstone.prototype.problem.states.PositionSearchProblemState;
import capstone.prototype.problem.states.ProblemState;

// capstone.prototype.types
import capstone.prototype.types.Direction;
import capstone.prototype.types.Grid;
import capstone.prototype.types.Layout;
import capstone.prototype.types.Position;
import capstone.prototype.types.Triple;
import capstone.prototype.types.Tuple;
import capstone.prototype.types.Vector;

// capstone.prototype.utils
import capstone.prototype.utils.Converter;
import capstone.prototype.utils.Utils;

// capstone.prototype.utils.heuristics
import capstone.prototype.utils.heuristics.Heuristics;

public class Search {

    public static void main(String[] args) {
        System.out.println("[java] Search.java loaded");
        // assign unused variables so that java actually compiles them
        Converter unused = new Converter();

        unused.nothing();
        Heuristics.nothing();
    }

    public static List<Direction> tinyMazeSearch(SearchProblem problem) {
        // s, s, w, s, w, w, s, w
        return Arrays.asList(
                Direction.SOUTH, Direction.SOUTH, Direction.WEST, Direction.SOUTH,
                Direction.WEST, Direction.WEST, Direction.SOUTH, Direction.WEST);
    }

    public static List<Direction> depthFirstSearch(SearchProblem _problem) {
        /*
         * Search the deepest nodes in the search tree first.
         * 
         * Your search algorithm needs to return a list of actions that reaches the
         * goal. Make sure to implement a graph search algorithm.
         * 
         * To get started, you might want to try some of these simple commands to
         * understand the search problem that is being passed in:
         * 
         * NeededType problem = (NeededType) _problem;
         * System.out.println("Start:" + problem.getStartState());
         * System.out.println("Is the start a goal?" + problem.isGoalState(problem.getStartState()));
         * System.out.println("Start's successors:" + problem.getSuccessors(problem.getStartState()));
         */

        if (_problem instanceof PositionSearchProblem) {
            //Your Code Here
        }

        else if (_problem instanceof CornersProblem) {
            //Your Code Here
        }

        else if (_problem instanceof FoodSearchProblem) {
            //Your Code Here
        }

        throw new UnsupportedOperationException(
                "Unimplemented method 'depthFirstSearch' for unknown SearchProblem type");
    }

    public static List<Direction> breadthFirstSearch(SearchProblem _problem) {
        /* Search the shallowest nodes in the search tree first. */

        if (_problem instanceof PositionSearchProblem) {
            //Your Code Here
        }

        else if (_problem instanceof CornersProblem) {
            //Your Code Here
        }

        else if (_problem instanceof FoodSearchProblem) {
            //Your Code Here
        }

        throw new UnsupportedOperationException(
                "Unimplemented method 'breadthFirstSearch' for unknown SearchProblem type");
    }

    public static List<Direction> uniformCostSearch(SearchProblem _problem) {
        /* Search the node of least total cost first. */

        if (_problem instanceof PositionSearchProblem) {
            //Your Code Here
        }

        else if (_problem instanceof CornersProblem) {
            //Your Code Here
        }

        else if (_problem instanceof FoodSearchProblem) {
            //Your Code Here
        }

        // If the problem type is not supported, throw an error
        throw new UnsupportedOperationException("UniformCostSearch not implemented for this problem type");
    }

    public static List<Direction> aStarSearch(SearchProblem _problem,
            BiFunction<ProblemState, SearchProblem, Double> _heuristics) {
        if (_heuristics == null) {
            _heuristics = (state, problem) -> nullHeuristic(problem);
        }
        // Java(536871575)
        final BiFunction<ProblemState, SearchProblem, Double> heuristics = _heuristics;

        /* Search the node that has the lowest combined cost and heuristic first. */

        if (_problem instanceof PositionSearchProblem) {
            //Your Code Here
        }

        else if (_problem instanceof CornersProblem) {
            //Your Code Here
        }

        else if (_problem instanceof FoodSearchProblem) {
            //Your Code Here
        }

        throw new UnsupportedOperationException(
                "Unimplemented method 'aStarSearch' for unknown SearchProblem type");
    }

    public static double nullHeuristic(SearchProblem problem) {
        //A heuristic function estimates the cost from the current state to the nearest
        //goal in the provided SearchProblem. This heuristic is trivial.
        return 0d;
    }
}