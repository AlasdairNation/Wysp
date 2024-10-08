package capstone.prototype.problem.states;

import capstone.prototype.types.Position;

public class PositionSearchProblemState implements ProblemState {
    public Position position;

    public PositionSearchProblemState(Position state) {
        this.position = state;
    }
}
