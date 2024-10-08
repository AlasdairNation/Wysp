package capstone.prototype.problem;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;

import capstone.prototype.Search;
import capstone.prototype.game.GameState;
import capstone.prototype.types.Direction;
import capstone.prototype.types.Position;

public class StayWestSearchAgent {
    /*
     * An agent for position search with a cost function that penalizes being in
     * positions on the East side of the board.
     * 
     * The cost function for stepping into a position (x,y) is 2^x.
     */
    public Function<SearchProblem, List<Direction>> searchFunction;
    public Function<GameState, PositionSearchProblem> searchType;
    public List<Direction> actions = new ArrayList<>();
    public Integer actionIndex = null;

    public StayWestSearchAgent() {
        this.searchFunction = (SearchProblem problem) -> {
            return Search.uniformCostSearch(problem);
        };

        Function<Position, Double> costFn = (Position pos) -> Math.pow(2d, pos.x);

        this.searchType = (GameState gameState) -> {
            return new PositionSearchProblem(gameState, costFn);
        };
    }

    public void registerInitialState(GameState state) {
        if (this.searchFunction == null)
            throw new RuntimeException("No search function provided for StayWestSearchAgent");

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