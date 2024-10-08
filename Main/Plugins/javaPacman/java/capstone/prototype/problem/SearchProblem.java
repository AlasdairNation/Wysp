package capstone.prototype.problem;

import java.util.List;

import capstone.prototype.problem.states.ProblemState;
import capstone.prototype.types.Direction;
import capstone.prototype.types.Triple;

public abstract class SearchProblem {

    public abstract ProblemState getStartState();

    public abstract boolean isGoalState(ProblemState state);

    public abstract List<Triple<ProblemState, Direction, Integer>> getSuccessors(ProblemState state);

    public abstract int getCostOfActions(List<Direction> actions); // not implemented in src
}
