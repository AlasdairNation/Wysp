package capstone.prototype.game;

import java.util.List;

import capstone.prototype.types.Direction;
import capstone.prototype.types.Position;
import capstone.prototype.types.Vector;
import capstone.prototype.utils.Utils;
public class GhostRules {
    public static int GHOST_SPEED = 1;
    public static double COLLISION_TOLERANCE = 0.5;
    public static List<Direction> getLegalActions(GameState state, int ghostIndex) {
        Configuration conf = state.getGhostState(ghostIndex).configuration;
        List<Direction> possibleActions = Actions.getPossibleActions(conf, state.getWalls());
        Direction reverse = Actions.reverseDirection(conf.direction);
        if(possibleActions.contains(Direction.STOP)) {
            possibleActions.remove(Direction.STOP);
        }
        if(possibleActions.contains(reverse) && possibleActions.size() > 1) {
            possibleActions.remove(reverse);
        }
        return possibleActions;
    }

    public static void applyAction(GameState state, Direction action, int ghostIndex) {
        List<Direction> legal = getLegalActions(state, ghostIndex);
        if(!legal.contains(action)) {
            throw new IllegalArgumentException("Illegal ghost action " + action.name());
        }
        AgentState ghostState = state.data.agentStates.get(ghostIndex);
        int speed = GHOST_SPEED;
        if(ghostState.scaredTimer > 0) {
            speed /= 2.0;
        }
        Vector vector = Actions.directionToVector(action, speed);
        ghostState.configuration = ghostState.configuration.generateSuccessor(vector);
    }

    public static void decrementTimer(AgentState ghostState) {
        int timer = ghostState.scaredTimer;
        if (timer == 1) {
            ghostState.configuration.pos = Utils.nearestPoint(ghostState.configuration.pos);
        }
        ghostState.scaredTimer = Math.max(0, timer - 1);
    }

    public static void checkDeath(GameState state, int agentIndex) {
        Position pacmanPosition = state.getPacmanPosition();
        if(agentIndex == 0) {
            for (int i = 0; i < state.data.agentStates.size(); i++) {
                AgentState ghostState = state.data.agentStates.get(i);
                Position ghostPosition = ghostState.configuration.getPosition();
                if(GhostRules.canKill(pacmanPosition, ghostPosition)) {

                }
            }
        }
    }
    public static void collide(GameState state, AgentState ghostState, int agentIndex) {
        if(ghostState.scaredTimer > 0) {
            state.data.scoreChange += 200;
            GhostRules.placeGhost(state, ghostState);
            ghostState.scaredTimer = 0;
            state.data._eaten.set(agentIndex, true);
        }
        else {
            if(!state.data._win) {
                state.data.scoreChange -= 500;
                state.data._lose = true;
            }
        }
    }

    public static Boolean canKill(Position pacmanPosition, Position ghostPosition) {
        return Utils.manhattanDistance( ghostPosition, pacmanPosition ) <= COLLISION_TOLERANCE;
        
    }

    public static void placeGhost(GameState state, AgentState ghostState) {
        ghostState.configuration = ghostState.start;
    }
}
