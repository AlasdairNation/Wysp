package capstone.prototype.utils.heuristics;

import java.lang.Double;
import java.util.List;
import java.util.function.BiFunction;

import capstone.prototype.problem.CornersProblem;
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
        List<Position> corners = problem.corners;
        Grid walls = problem.walls;

        // *** YOUR CODE HERE *** //
        return 0;
    }

    public static double foodHeuristic(ProblemState problemState, SearchProblem problem) {
        /*
         * A search problem associated with finding the a path that collects all of the
         * food (dots) in a Pacman game.
         * 
         * A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
         * * pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
         * * foodGrid: a Grid (see game.py) of either True or False, specifying
         * remaining food
         */
        FoodSearchProblemState foodSearchProblemState = (FoodSearchProblemState) problemState;
        Tuple<Position, Grid> state = foodSearchProblemState.state;
        Position position = state.first;
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

    /*
     * def euclideanHeuristic(position, problem, info={}):
     * "The Euclidean distance heuristic for a PositionSearchProblem"
     * xy1 = position
     * xy2 = problem.goal
     * return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5
     */
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
