package capstone.prototype.problem;

import java.util.*;
import java.util.function.*;

import capstone.prototype.Search;
import capstone.prototype.game.GameState;
import capstone.prototype.types.Direction;
import capstone.prototype.utils.heuristics.Heuristics;

public class AStarCornersAgent {
    public Function<SearchProblem, List<Direction>> searchFunction;
    public Function<GameState, SearchProblem> searchType;
    public List<Direction> actions;
    public Integer actionIndex;

    public AStarCornersAgent() {
        this.searchFunction = (SearchProblem problem) -> {
            return Search.aStarSearch(problem, Heuristics::cornersHeuristic);
        };

        this.searchType = (GameState state) -> {
            return new CornersProblem(state);
        };

        this.actions = new ArrayList<>();
    }

    public void registerInitialState(GameState state) {
        if (this.searchFunction == null)
            throw new RuntimeException("No search function provided for StayEastSearchAgent");

        long startTime = System.currentTimeMillis();
        CornersProblem problem = (CornersProblem) this.searchType.apply(state);
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