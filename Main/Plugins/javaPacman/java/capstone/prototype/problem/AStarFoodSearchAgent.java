package capstone.prototype.problem;

import java.util.*;
import java.util.function.Function;

import capstone.prototype.Search;
import capstone.prototype.game.GameState;
import capstone.prototype.types.Direction;
import capstone.prototype.utils.heuristics.Heuristics;


public class AStarFoodSearchAgent {
    public Function<FoodSearchProblem, List<Direction>> searchFunction;
    public Function<GameState, FoodSearchProblem> searchType;
    public List<Direction> actions = new ArrayList<>();
    public Integer actionIndex = null;

    public AStarFoodSearchAgent() {
        initialize();
    }

    public void registerInitialState(GameState state) {
        if (this.searchFunction == null) throw new IllegalStateException("No search function provided for AStarFoodSearchAgent");
        long startTime = System.currentTimeMillis();
        FoodSearchProblem problem = this.searchType.apply(state);
        this.actions = this.searchFunction.apply(problem);
        int totalCost = problem.getCostOfActions(this.actions);

        System.out.println(String.format("Path found with total cost of %d in %.1f seconds", totalCost,
        (System.currentTimeMillis() - startTime) / 1000d));
    }

    private void initialize() {
        // Assuming a static method aStarSearch exists in a class called Search that accepts a search problem and a heuristic
        // and Heuristics class has a method to get foodHeuristic
        // Assuming that the problem is a FoodSearchProblem and that aStarSearch has an int for its second parameter since foodHeuristic returns a number.
        this.searchFunction = (FoodSearchProblem prob) -> { 
            return Search.aStarSearch(prob, Heuristics::foodHeuristic);
        };
        this.searchType = (GameState gameState) -> { return new FoodSearchProblem(gameState); } ; // Referencing the FoodSearchProblem class
    }

    public Direction getAction(GameState state) {
        if(this.actionIndex == null) {
            this.actionIndex = 0;
        }
        int i = this.actionIndex;
        this.actionIndex++;

        if(i < this.actions.size()) {
            return this.actions.get(i);
        }
        else {
            return Direction.STOP;
        }
    }
}
