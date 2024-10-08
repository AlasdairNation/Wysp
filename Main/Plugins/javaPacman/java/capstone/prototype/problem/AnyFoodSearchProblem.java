package capstone.prototype.problem;

import java.util.*;

import capstone.prototype.game.GameState;
import capstone.prototype.problem.states.PositionSearchProblemState;
import capstone.prototype.problem.states.ProblemState;
import capstone.prototype.types.Grid;
import capstone.prototype.types.Position;
import capstone.prototype.types.Tuple;

public class AnyFoodSearchProblem extends PositionSearchProblem {
    public Grid food;

    public AnyFoodSearchProblem(GameState gameState) {
        super();

        this.food = gameState.getFood(); // Store the food for later reference
        this.walls = gameState.getWalls();
        this.startState = new PositionSearchProblemState(gameState.getPacmanPosition());
        this.costFn = (Position state) -> 1.0d;
    }

    @Override
    public boolean isGoalState(ProblemState inProblemState) {
        // The state is Pacman's position. Fill this in with a goal test that will
        // complete the problem definition.
        PositionSearchProblemState problemState = (PositionSearchProblemState) inProblemState;
        int x = (int) problemState.position.x;
        int y = (int) problemState.position.y;

        // TODO: remove impl after testing, before submission
        List<Tuple<Integer, Integer>> foodL = this.food.asList();
        for (Tuple<Integer, Integer> f : foodL) {
            if (f.first == x && f.second == y)
                return true;
        }
        return false;

        // You can get rid of this once you have a return statement vvv
        // throw new UnsupportedOperationException("Unimplemented method 'isGoalState()
        // in AnyFoodSearchProblem.'");
    }
}