package capstone.prototype.game;

import java.util.List;

import capstone.prototype.types.Direction;
import capstone.prototype.types.Position;
import capstone.prototype.types.Vector;
import capstone.prototype.utils.Utils;

public class PacmanRules {
    public static int PACMAN_SPEED = 1;

    public static List<Direction> getLegalActions(GameState state) {
        return Actions.getPossibleActions(state.getPacmanState().configuration, state.getWalls());
    }

    public static void applyAction(GameState state, Direction action) {
        List<Direction> legal = getLegalActions(state);
        if (!legal.contains(action)) {
            throw new IllegalArgumentException("Illegal action " + action.toString());
        }
        AgentState pacmanState = state.data.agentStates.get(0);

        Vector vector = Actions.directionToVector(action, PACMAN_SPEED);
        pacmanState.configuration = pacmanState.configuration.generateSuccessor(vector);

        Position next = pacmanState.getPosition();
        Position nearest = Utils.nearestPoint(next);
        if (Utils.manhattanDistance(nearest, next) <= 0.5) {
            PacmanRules.consume(nearest, state);
        }
    }

    public static void consume(Position pos, GameState state) {
        int x = (int) pos.x;
        int y = (int) pos.y;

        if (state.data.food.data.get(x).get(y)) {
            state.data.scoreChange += 10;
            state.data.food = state.data.food.copy();
            state.data.food.data.get(x).set(y, false);
            state.data._foodEaten = pos;

            int numFood = state.getNumFood();
            if (numFood == 0 && !state.data._lose) {
                state.data.scoreChange += 500;
                state.data._win = true;
            }
        }
        if (state.data.getCapsules().contains(pos)) {
            state.data.capsules.remove(pos);
            state.data._capsuleEaten = pos;
            for (int i = 0; i < state.data.agentStates.size(); i++) {
                state.data.agentStates.get(i).scaredTimer = 40;
            }
        }
    }
}
