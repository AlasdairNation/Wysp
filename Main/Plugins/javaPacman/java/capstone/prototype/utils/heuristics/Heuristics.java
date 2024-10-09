package capstone.prototype.utils.heuristics;

import java.lang.Double;
import java.util.List;
import java.util.function.BiFunction;

import capstone.prototype.problem.CornersProblem;
import capstone.prototype.problem.FoodSearchProblem;
import capstone.prototype.problem.PositionSearchProblem;
import capstone.prototype.problem.SearchProblem;
import capstone.prototype.problem.states.FoodSearchProblemState;
import capstone.prototype.problem.states.PositionSearchProblemState;
import capstone.prototype.problem.states.ProblemState;
import capstone.prototype.types.Grid;
import capstone.prototype.types.Position;
import capstone.prototype.types.Tuple;

public class Heuristics {
    // TODO: make java version of the comments
    public static double cornersHeuristic(ProblemState state, SearchProblem inProblem) {
        /*
         * A heuristic for the CornersProblem that you defined.
         * 
         * * state: The current search state
         * * (a data structure you chose in your search problem)
         * 
         * * problem: The CornersProblem instance for this layout.
         * 
         * This function should always return a number that is a lower bound on the
         * shortest path from the state to a goal of the problem; i.e. it should be
         * admissible (as well as consistent).
         */
        CornersProblem problem = (CornersProblem) inProblem;
        List<Position> corners = problem.corners; //These are the corner coordinates
        Grid walls = problem.walls; //These are the walls of the maze, as a Grid type.

        // *** YOUR CODE HERE *** //
        return 0; //Default to trivial solution
    }

    public static double foodHeuristic(ProblemState problemState, SearchProblem problem) {
        /*
         * Your heuristic for the FoodSearchProblem goes here.
         * 
         * This heuristic must be consistent to ensure correctness.  First, try to come
         * up with an admissible heuristic; almost all admissible heuristics will be
         * consistent as well.
         * 
         * If using A* ever finds a solution that is worse uniform cost search finds,
         * your heuristic is *not* consistent, and probably not admissible!  On the
         * other hand, inadmissible or inconsistent heuristics may find optimal
         * solutions, so be careful.
         * 
         * The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
         * (see Grid.java) of either True or False. You can call foodGrid.asList() to get
         * a list of food coordinates instead.
         * 
         * If you want access to info like walls, capsules, etc., you can query the
         * problem.  For example, Grid walls = foodSearchProblem.walls;.walls gives you 
         * a Grid of where the walls are.
         * 
         * If you want to *store* information to be reused in other calls to the
         * heuristic, there is a dictionary called foodSearchProblem.heuristicInfo that you can
         * use. For example, if you only want to count the walls once and store that
         * value, try: foodSearchProblem.heuristicInfo.put("wallCount", foodSearchProblem.walls.count())
         * Subsequent calls to this heuristic can access
         * foodSearchProblem.heuristicInfo.get("wallCount")
         */
        FoodSearchProblemState foodSearchProblemState = (FoodSearchProblemState) problemState;
        FoodSearchProblem foodSearchProblem = (FoodSearchProblem) problem;
        Tuple<Position, Grid> state = foodSearchProblemState.state;
        Position pacmanPosition = state.first;
        Grid foodGrid = state.second;
        // *** YOUR CODE HERE *** //
        return 0;
    }

    public static double manhattanHeuristic(ProblemState problemState, SearchProblem problem) {
        // only called if the problem is a PositionSearchProblem
        Position position = ((PositionSearchProblemState) problemState).position;
        Position goal = ((PositionSearchProblem) problem).goal;
        return Math.abs(position.x - goal.x) + Math.abs(position.y - goal.y);
    }

    public static double euclideanHeuristic(ProblemState problemState, SearchProblem problem) {
        Position position = ((PositionSearchProblemState) problemState).position;
        Position goal = ((PositionSearchProblem) problem).goal;
        return Math.sqrt(Math.pow(position.x - goal.x, 2) + Math.pow(position.y - goal.y, 2));
    }

    // No need to change any of the following methods
    public static BiFunction<ProblemState, SearchProblem, Double> getCornersHeuristic() {
        return Heuristics::cornersHeuristic;
    }

    public static BiFunction<ProblemState, SearchProblem, Double> getFoodHeuristic() {
        return Heuristics::foodHeuristic;
    }

    public static BiFunction<ProblemState, SearchProblem, Double> getManhattanHeuristic() {
        return Heuristics::manhattanHeuristic;
    }

    public static BiFunction<ProblemState, SearchProblem, Double> getEuclideanHeuristic() {
        return Heuristics::euclideanHeuristic;
    }

    public static void nothing() {
        System.out.println("[java] Heuristics class loaded");
    }
}
