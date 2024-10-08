package capstone.prototype.game;

import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;

import capstone.prototype.types.Direction;
import capstone.prototype.types.Grid;
import capstone.prototype.types.Position;

public class GameState {

    public HashSet<GameState> explored = new HashSet<>();
    public GameStateData data;

    public GameState(GameStateData prevState) {
        this.data = prevState;
    }

    public HashSet<GameState> getAndResetExplored() {
        HashSet<GameState> temp = new HashSet<>(explored);
        explored.clear();
        return temp;
    }

    public List<AgentState> getGhostStates() {
        List<AgentState> ghostStates = this.data.agentStates;
        ghostStates.remove(0);
        return ghostStates;
    };

    public AgentState getGhostState(int agentIndex) {
        if (agentIndex == 0 || agentIndex >= this.getNumAgents())
            throw new IllegalArgumentException("Invalid index passed to getGhostState");
        return this.data.agentStates.get(agentIndex);

    };

    public GameState generateSuccessor(int agentIndex, Direction action) {
        // Check that successors exist
        if (this.data._win || this.data._lose) {
            throw new IllegalArgumentException("Can't generate a successor of terminal state");
        }
        GameState state = new GameState(this.data);
        if (agentIndex == 0) {
            List<Boolean> agentsEaten = new LinkedList<>();
            for (int i = 0; i < state.getNumAgents(); i++) {
                agentsEaten.add(false);
            }
            state.data._eaten = agentsEaten;
            PacmanRules.applyAction(state, action);
        } else {
            GhostRules.applyAction(state, action, agentIndex);
        }

        if (agentIndex == 0) {
            state.data.scoreChange += -1;
        } else {
            GhostRules.decrementTimer(state.data.agentStates.get(agentIndex));
        }
        GhostRules.checkDeath(state, agentIndex);

        state.data._agentMoved = agentIndex;
        state.data.score += state.data.scoreChange;
        explored.add(this);
        explored.add(state);
        return state;
    };

    public AgentState getPacmanState() {
        return this.data.agentStates.get(0);
    };

    public int getNumFood() {
        return this.data.food.data.size();
    };

    public int getNumAgents() {
        return this.data.agentStates.size();
    };

    public Grid getWalls() {
        return this.data.layout.walls;
    };

    public Position getPacmanPosition() {
        return this.data.agentStates.get(0).getPosition();
    };

    public boolean hasFood(Position pos) {
        return this.data.food.data.get((int) pos.x).get((int) pos.y);
    };

    public Grid getFood() {
        return this.data.food;
    };
}
