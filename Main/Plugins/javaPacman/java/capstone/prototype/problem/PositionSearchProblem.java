package capstone.prototype.problem;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

import capstone.prototype.game.Actions;
import capstone.prototype.game.GameState;
import capstone.prototype.problem.states.PositionSearchProblemState;
import capstone.prototype.problem.states.ProblemState;
import capstone.prototype.types.Direction;
import capstone.prototype.types.Grid;
import capstone.prototype.types.Position;
import capstone.prototype.types.Triple;

public class PositionSearchProblem extends SearchProblem {

    public Function<Position, Double> costFn;
    public Grid walls;
    protected ProblemState startState;
    public Position goal;
    public Map<Position, Boolean> _visited = new HashMap<>();
    public List<Position> _visitedList = new ArrayList<>();
    public int _expanded = 0;

    public PositionSearchProblem(GameState gameState, Position goal, Position start) {
        this.walls = gameState.getWalls();
        // if start != None: self.startState = start
        this.startState = new PositionSearchProblemState(start);
        this.goal = goal;

        // default costFn just returns 1
        this.costFn = (Position state) -> 1.0d;
    }

    public PositionSearchProblem(GameState gameState, Position goal) {
        this.walls = gameState.getWalls();
        this.startState = new PositionSearchProblemState(gameState.getPacmanPosition());
        this.goal = goal;
        this.costFn = (Position state) -> 1.0d;
    }

    public PositionSearchProblem(GameState gameState, Function<Position, Double> costFn) {
        this.walls = gameState.getWalls();
        this.startState = new PositionSearchProblemState(gameState.getPacmanPosition());
        this.goal = gameState.getPacmanPosition();
        this.costFn = costFn;
    }

    // Empty constructor, for AnyFoodSearchProblem
    public PositionSearchProblem() {
    }

    @Override
    public ProblemState getStartState() {
        return this.startState;
    }

    @Override
    public boolean isGoalState(ProblemState problemState) {
        boolean isGoal = ((PositionSearchProblemState) problemState).position.equals(this.goal);

        if (isGoal) {
            this._visitedList.add(((PositionSearchProblemState) problemState).position);
        }

        return isGoal;
    }

    @Override
    public List<Triple<ProblemState, Direction, Integer>> getSuccessors(ProblemState problemState) {
        Position state = ((PositionSearchProblemState) problemState).position;
        /*
         * for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST,
         * Directions.WEST]:
         * * x,y = state
         * * dx, dy = Actions.directionToVector(action)
         * * nextx, nexty = int(x + dx), int(y + dy)
         * * if not self.walls[nextx][nexty]:
         * * * nextState = (nextx, nexty)
         * * * cost = self.costFn(nextState)
         * * * successors.append( ( nextState, action, cost) )
         */
        List<Triple<ProblemState, Direction, Integer>> successors = new ArrayList<>();
        int cost = 1;
        for (Direction action : Arrays.asList(Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST)) {
            double x = state.x;
            double y = state.y;
            double dx = Actions.directionToVector(action).x;
            double dy = Actions.directionToVector(action).y;

            int next_x = (int) (x + dx);
            int next_y = (int) (y + dy);

            if (!this.walls.data.get(next_x).get(next_y)) {
                Position nextState = new Position(next_x, next_y);
                cost += this.costFn.apply(nextState);

                PositionSearchProblemState pspState = new PositionSearchProblemState(nextState);
                successors.add(new Triple<>(pspState, action, cost));
            }
        }

        // Bookkeeping for display purposes
        this._expanded++;
        if (!this._visited.containsKey(state)) {
            this._visited.put(state, true);
            this._visitedList.add(state);
        }

        return successors;
    }

    @Override
    public int getCostOfActions(List<Direction> actions) {
        if (actions == null)
            return 999999;

        double x = ((PositionSearchProblemState) this.getStartState()).position.x;
        double y = ((PositionSearchProblemState) this.getStartState()).position.y;
        int cost = 0;

        for (Direction dir : actions) {
            double dx = Actions.directionToVector(dir).x;
            double dy = Actions.directionToVector(dir).y;
            int tempX = (int) (x + dx);
            int tempY = (int) (y + dy);

            if (this.walls.data.get(tempX).get(tempY))
                return 999999;

            x = tempX;
            y = tempY;
            cost += this.costFn.apply(new Position(x, y));
        }
        return cost;
    }
}