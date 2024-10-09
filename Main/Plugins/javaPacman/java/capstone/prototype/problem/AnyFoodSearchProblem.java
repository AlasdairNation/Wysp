package capstone.prototype.problem;

import java.util.*;

import capstone.prototype.game.GameState;
import capstone.prototype.problem.states.PositionSearchProblemState;
import capstone.prototype.problem.states.ProblemState;
import capstone.prototype.types.Grid;
import capstone.prototype.types.Position;
import capstone.prototype.types.Tuple;

/* A search problem for finding a path to any food.
 * 
 * This search problem is just like the PositionSearchProblem, but has a
 * different goal test, which you need to fill in below.  The state space and
 * successor function do not need to be changed.
 * 
 * The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
 * inherits the methods of the PositionSearchProblem.
 * 
 * You can use this search problem to help you fill in the findPathToClosestDot
 * method.
 */

public class AnyFoodSearchProblem extends PositionSearchProblem {
    
    public Grid food;

    public AnyFoodSearchProblem(GameState gameState) {
        super();

        // Store the food for later reference
        this.food = gameState.getFood(); 
        // Store info for the PositionSearchProblem (no need to change this)
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

        //Your Code Here

        // You can get rid of this once you have a return statement vvv
        throw new UnsupportedOperationException("Unimplemented method 'isGoalState()in AnyFoodSearchProblem.'");
    }
}