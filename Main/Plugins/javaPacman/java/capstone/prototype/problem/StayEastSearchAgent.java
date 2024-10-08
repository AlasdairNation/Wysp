package capstone.prototype.problem;

import java.util.*;

import java.util.function.Function;

import capstone.prototype.Search;
import capstone.prototype.game.GameState;
import capstone.prototype.types.Direction;
import capstone.prototype.types.Position;

public class StayEastSearchAgent {

    public Function<SearchProblem, List<Direction>> searchFunction;
    public Function<GameState, PositionSearchProblem> searchType;
    public List<Direction> actions = new ArrayList<>();
    public Integer actionIndex = null;
    
    public StayEastSearchAgent(){   
        this.searchFunction = (SearchProblem problem) -> {
            return Search.uniformCostSearch(problem);
        };

        Function<Position, Double> costFn = (Position pos) -> Math.pow(0.5d, pos.x);
        
        this.searchType = (GameState state) -> {
            return new PositionSearchProblem(state, costFn);
        };
    }

    public void registerInitialState(GameState state) {
        if (this.searchFunction == null)
            throw new RuntimeException("No search function provided for StayEastSearchAgent");

        long startTime = System.currentTimeMillis();
        PositionSearchProblem problem = this.searchType.apply(state);
        this.actions = this.searchFunction.apply(problem);
        int totalCost = problem.getCostOfActions(this.actions);

        /*
         * print('Path found with total cost of %d in %.1f seconds' % (totalCost,
         * time.time() - starttime))
         */
        System.out.println(String.format("Path found with total cost of %d in %.1f seconds", totalCost,
                (System.currentTimeMillis() - startTime) / 1000d));
    }

    public Direction getAction(GameState state) {
        if (this.actionIndex == null)
            this.actionIndex = 0;

        int i = this.actionIndex;
        this.actionIndex++;

        if (i < this.actions.size())
            return this.actions.get(i);
        else
            return Direction.STOP;
    }
}