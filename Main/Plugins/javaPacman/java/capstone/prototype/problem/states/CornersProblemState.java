package capstone.prototype.problem.states;

import java.util.List;

import capstone.prototype.types.Position;
import capstone.prototype.types.Tuple;

public class CornersProblemState implements ProblemState {
    public Tuple<Position, List<Integer>> state;

    public CornersProblemState(Position pos, List<Integer> corners) {
        this.state = new Tuple<Position, List<Integer>>(pos, corners);
    }
}
