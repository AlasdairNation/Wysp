package capstone.prototype.game;

import java.util.*;
import java.util.stream.Collectors;

import capstone.prototype.types.Direction;
import capstone.prototype.types.Grid;
import capstone.prototype.types.Position;
import capstone.prototype.types.Tuple;
import capstone.prototype.types.Vector;

public class Actions {
    private static final Map<Direction, Tuple<Integer, Integer>> directions = Map.of(
            Direction.NORTH, new Tuple<>(0, 1),
            Direction.SOUTH, new Tuple<>(0, -1),
            Direction.EAST, new Tuple<>(1, 0),
            Direction.WEST, new Tuple<>(-1, 0),
            Direction.STOP, new Tuple<>(0, 0));

    private static final List<Tuple<Direction, Tuple<Integer, Integer>>> directionsAsList = directions.entrySet().stream()
            .map(entry -> new Tuple<>(entry.getKey(), entry.getValue()))
            .collect(Collectors.toList());

    public static final float TOLERANCE = 0.001f;

    public static Direction reverseDirection(Direction action) {
        if (action == Direction.NORTH)
            return Direction.SOUTH;
        if (action == Direction.SOUTH)
            return Direction.NORTH;
        if (action == Direction.EAST)
            return Direction.WEST;
        if (action == Direction.WEST)
            return Direction.EAST;
        return action;
    }

    public static Direction vectorToDirection(Vector vector) {
        double dx = vector.x;
        double dy = vector.y;

        if (dy > 0)
            return Direction.NORTH;
        if (dy < 0)
            return Direction.SOUTH;

        if (dx < 0)
            return Direction.WEST;
        if (dx > 0)
            return Direction.EAST;

        return Direction.STOP;
    }

    public static Vector directionToVector(Direction direction) {
        return Actions.directionToVector(direction, 1f);
    }

    public static Vector directionToVector(Direction direction, float speed) {
        Tuple<Integer, Integer> delta = Actions.directions.get(direction);
        int dx = delta.first;
        int dy = delta.second;
        return new Vector(dx * speed, dy * speed);
    }

    public static List<Direction> getPossibleActions(Configuration config, Grid walls) {
        List<Direction> possible = new ArrayList<>();
        double x = config.pos.x;
        double y = config.pos.y;
        int x_int = (int) (x + 0.5);
        int y_int = (int) (y + 0.5);

        if (Math.abs(x - x_int) + Math.abs(y - y_int) > Actions.TOLERANCE)
            return Collections.singletonList(config.getDirection());

        for (Tuple<Direction, Tuple<Integer, Integer>> entry : Actions.directionsAsList) {
            Tuple<Integer, Integer> delta = entry.second;
            int dx = delta.first;
            int dy = delta.second;
            int next_x = x_int + dx;
            int next_y = y_int + dy;

            if (!walls.data.get(next_x).get(next_y))
                possible.add(entry.first);
        }
        return possible;
    }

    public static List<Tuple<Integer, Integer>> getLegalNeighbors(Position position, Grid walls) {
        int x_int = (int) (position.x + 0.5);
        int y_int = (int) (position.y + 0.5);
        List<Tuple<Integer, Integer>> neighbors = new ArrayList<>();

        for (Tuple<Direction, Tuple<Integer, Integer>> entry : Actions.directionsAsList) {
            Tuple<Integer, Integer> delta = entry.second;
            int dx = delta.first;
            int dy = delta.second;
            int next_x = x_int + dx;

            if (next_x < 0 || next_x >= walls.width)
                continue;

            int next_y = y_int + dy;
            if (next_y < 0 || next_y >= walls.height)
                continue;

            if (!walls.data.get(next_x).get(next_y))
                neighbors.add(new Tuple<>(next_x, next_y));
        }
        return neighbors;
    }

    public static Tuple<Double, Double> getSuccessor(Position position, Direction action) {
        Vector v = Actions.directionToVector(action);
        return new Tuple<>(position.x + v.x, position.y + v.y);
    }
}
