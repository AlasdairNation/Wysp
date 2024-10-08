package capstone.prototype.problem;

import java.util.*;

import capstone.prototype.game.Actions;
import capstone.prototype.game.GameState;
import capstone.prototype.problem.states.FoodSearchProblemState;
import capstone.prototype.problem.states.ProblemState;
import capstone.prototype.types.Direction;
import capstone.prototype.types.Grid;
import capstone.prototype.types.Position;
import capstone.prototype.types.Triple;
import capstone.prototype.types.Tuple;
import capstone.prototype.types.Vector;

// TODO: make java version of the comments
public class FoodSearchProblem extends SearchProblem {

    private Grid walls;
    private ProblemState start;
    public int _expanded;
    public Map<String, Object> heuristicInfo;

    public FoodSearchProblem(GameState startingGameState_) {
        /*
         * A search problem associated with finding the a path that collects all of the
         * food (dots) in a Pacman game.
         * 
         * A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
         * * pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
         * * foodGrid: a Grid (see game.py) of either True or False, specifying
         * * remaining food
         */
        this.start = new FoodSearchProblemState(startingGameState_.getPacmanPosition(), startingGameState_.getFood());
        this.walls = startingGameState_.getWalls();
        this._expanded = 0;
        this.heuristicInfo = new HashMap<String, Object>();
    }

    @Override
    public ProblemState getStartState() {
        return this.start;
    }

    @Override
    public boolean isGoalState(ProblemState problemState) {
        Tuple<Position, Grid> state = ((FoodSearchProblemState) problemState).state;
        return state.second.count() == 0;
    }

    @Override
    public List<Triple<ProblemState, Direction, Integer>> getSuccessors(ProblemState problemState) {
        Tuple<Position, Grid> state = ((FoodSearchProblemState) problemState).state;
        List<Triple<ProblemState, Direction, Integer>> successors = new ArrayList<>();
        this._expanded++;

        for (Direction action : Direction.values()) {
            if (action == Direction.STOP)
                continue;

            double x = state.first.x;
            double y = state.first.y;
            double dx = ((Vector) Actions.directionToVector(action)).x;
            double dy = ((Vector) Actions.directionToVector(action)).y;

            int nextX = (int) (x + dx);
            int nextY = (int) (y + dy);

            if (!this.walls.data.get(nextX).get(nextY)) {
                Grid nextFood = state.second.copy();
                nextFood.data.get(nextX).set(nextY, false);

                // creating next state
                Position nextPos = new Position((double) nextX, (double) nextY);
                FoodSearchProblemState nextState = new FoodSearchProblemState(nextPos, nextFood);
                successors.add(new Triple<>(nextState, action, 1));
            }
        }
        return successors;
    }

    @Override
    public int getCostOfActions(List<Direction> actions) {

        // Returns the cost of a particular sequence of actions. If those actions
        // include an illegal move, return 999999

        // get position.x
        double x = ((FoodSearchProblemState) this.getStartState()).state.first.x;
        // get position.y
        double y = ((FoodSearchProblemState) this.getStartState()).state.first.y;
        int cost = 0;

        for (Direction dir : actions) {
            double dx = ((Vector) Actions.directionToVector(dir)).x;
            double dy = ((Vector) Actions.directionToVector(dir)).y;
            int tempX = (int) (x + dx);
            int tempY = (int) (y + dy);
            if (this.walls.data.get(tempX).get(tempY)) {
                return 999999;
            }
            cost += 1;
        }
        return cost;
    }
}