package capstone.prototype.problem;

import java.util.ArrayList;
import java.util.List;

import capstone.prototype.Search;
import capstone.prototype.game.Actions;
import capstone.prototype.game.GameState;
import capstone.prototype.types.Direction;
import capstone.prototype.types.Grid;
import capstone.prototype.types.Position;

// TODO: remove agent methods if not implemented in python ver.
public class ClosestDotSearchAgent {
    public List<Direction> actions;
    public Integer actionIndex;

    public ClosestDotSearchAgent() {
        this.actions = new ArrayList<>();
        this.actionIndex = 0;
    }

    //Search for all food using a sequence of searches
    public void registerInitialState(GameState state) {
        GameState currentState = state;
        while (currentState.getFood().count(true) > 0) {
            List<Direction> nextPathSegment = findPathToClosestDot(currentState);

            if (nextPathSegment.isEmpty() && currentState.getFood().count(true) > 0) {
                throw new IllegalStateException("[java] [ClosestDotSearchAgent] No path found");
            }

            actions.addAll(nextPathSegment);
            for (Direction action : nextPathSegment) {
                if (!Actions.getPossibleActions(currentState.getPacmanState().configuration, currentState.getWalls())
                        .contains(action)) {
                    throw new IllegalStateException(
                            "[java] [ClosestDotSearchAgent] findPathToClosestDot returned an illegal move: " + action);
                }
                currentState = currentState.generateSuccessor(0, action);
            }
        }
        System.out.println("Path found with cost " + actions.size() + ".");
    }

    private List<Direction> findPathToClosestDot(GameState gameState) {
        /*  Returns a path (a list of actions) to the closest dot, starting from
            gameState.

            Here are some useful elements of the startState below:
        */
        Position startPosition = gameState.getPacmanPosition();
        Grid food = gameState.getFood();
        Grid walls = gameState.getWalls();
        AnyFoodSearchProblem problem = new AnyFoodSearchProblem(gameState);

        //Your Code Here
        throw new UnsupportedOperationException(
                "Unimplemented method 'findPathToClosestDot() in ClosestDotSearchAgent.java'");
    }

    public Direction getAction(GameState state) {
        if (this.actionIndex == null) {
            this.actionIndex = 0;
        }
        int i = this.actionIndex;
        this.actionIndex++;

        if (i < this.actions.size()) {
            return this.actions.get(i);
        } else {
            return Direction.STOP;
        }
    }
}