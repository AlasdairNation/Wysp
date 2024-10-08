package capstone.prototype.problem.states;

import capstone.prototype.types.Grid;
import capstone.prototype.types.Position;
import capstone.prototype.types.Tuple;

public class FoodSearchProblemState implements ProblemState {
    public Tuple<Position, Grid> state;

    public FoodSearchProblemState(Position pos, Grid foodGrid) {
        this.state = new Tuple<Position, Grid>(pos, foodGrid);
    }
}
