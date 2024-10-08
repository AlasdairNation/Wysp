package capstone.prototype.game;

import java.util.ArrayList;
import java.util.List;

import capstone.prototype.types.Direction;
import capstone.prototype.types.Grid;
import capstone.prototype.types.Layout;
import capstone.prototype.types.Position;
import capstone.prototype.types.Tuple;

public class GameStateData {

    public Position _foodEaten = null;
    public Tuple<Integer, Integer> _foodAdded = null;
    public Position _capsuleEaten = null;
    public boolean _lose = false;
    public boolean _win = false;
    public List<Boolean> _eaten = null;

    public int scoreChange = 0;
    public Grid food = null;
    public List<Position> capsules = null;
    public List<AgentState> agentStates = null;
    public Layout layout = null;
    public int score = -1;

    public int _agentMoved = -1;

    public GameStateData(GameStateData prevState) {
        this.food = prevState.food.shallowCopy();
        this.capsules = new ArrayList<>(prevState.capsules);
        this.agentStates = copyAgentStates(prevState.agentStates);
        this.layout = prevState.layout;
        this._eaten = prevState._eaten;
        this.score = prevState.score;
    }

    public GameStateData() {
    }

    public GameStateData deepCopy() {
        GameStateData state = new GameStateData(this);
        state.food = this.food.deepCopy();
        state.layout = this.layout.deepCopy();
        state._agentMoved = this._agentMoved;
        state._foodEaten = this._foodEaten;
        state._foodAdded = this._foodAdded;
        state._capsuleEaten = this._capsuleEaten;
        return state;
    }

    public List<Position> getCapsules() {
        return this.capsules;
    }

    public List<AgentState> copyAgentStates(List<AgentState> agentStates) {
        List<AgentState> copy = new ArrayList<>();
        for (AgentState agentState : agentStates) {
            copy.add(agentState.copy());
        }
        return copy;
    }

    public void initialize(Layout layout, int numGhostAgents) {
        this.food = layout.food.copy();
        this.capsules = layout.capsules;
        this.layout = layout;
        this.score = 0;
        this.scoreChange = 0;
        this.agentStates = new ArrayList<>();

        int numGhosts = 0;
        for (Tuple<Boolean, Position> agentPosition : layout.agentPositions) {
            boolean isPacman = agentPosition.first;
            if (!isPacman) {
                if (numGhosts == numGhostAgents) {
                    continue;
                }
                numGhosts += 1;
            }
            this.agentStates.add(new AgentState(new Configuration(agentPosition.second, Direction.STOP), isPacman));
        }
        // self._eaten = [False for a in self.agentStates]
        this._eaten = new ArrayList<>();
        for (int i = 0; i < this.agentStates.size(); i++) {
            this._eaten.add(false);
        }
    }

    @Override
    public boolean equals(Object other) {
        if (!(other instanceof GameStateData))
            return false;
        /**
         * if not self.agentStates == other.agentStates: return False
         * if not self.food == other.food: return False
         * if not self.capsules == other.capsules: return False
         * if not self.score == other.score: return False
         * return True
         */
        GameStateData otherState = (GameStateData) other;
        if (!this.agentStates.equals(otherState.agentStates) || !this.food.equals(otherState.food))
            return false;

        if (!this.capsules.equals(otherState.capsules) || this.score != otherState.score)
            return false;

        return true;
    }
}
