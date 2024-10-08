package capstone.prototype.game;

import capstone.prototype.types.Direction;
import capstone.prototype.types.Position;

public class AgentState {
    public Configuration start;
    public Configuration configuration;

    public boolean isPacman;
    public int scaredTimer;
    public int numCarrying;
    public int numReturned;

    public AgentState(Configuration startConfiguration, boolean isPacman) {
        this.start = startConfiguration;
        this.configuration = startConfiguration;
        this.isPacman = isPacman;

        this.scaredTimer = 0;
        this.numCarrying = 0;
        this.numReturned = 0;
    }

    public AgentState(Configuration startConfiguration, Configuration configuration, boolean isPacman, int scaredTimer,
            // constructor for converter
            int numCarrying, int numReturned) {
        this.start = startConfiguration;
        this.configuration = configuration;
        this.isPacman = isPacman;

        this.scaredTimer = scaredTimer;
        this.numCarrying = numCarrying;
        this.numReturned = numReturned;
    }

    public AgentState copy() {
        AgentState state = new AgentState(this.start, this.isPacman);
        state.configuration = this.configuration;
        state.scaredTimer = this.scaredTimer;
        state.numCarrying = this.numCarrying;
        state.numReturned = this.numReturned;
        return state;
    }

    public Position getPosition() {
        return this.configuration.getPosition();
    }

    public Direction getDirection() {
        return this.configuration.getDirection();
    }

    @Override
    public boolean equals(Object other) {
        if (!(other instanceof AgentState)) {
            return false;
        }

        AgentState o = (AgentState) other;
        return this.configuration.equals(o.configuration) && this.scaredTimer == o.scaredTimer;
    }

    @Override
    public String toString() {
        if (this.isPacman)
            return "Pacman: " + this.configuration.toString();
        else
            return "Ghost: " + this.configuration.toString();

    }
}
