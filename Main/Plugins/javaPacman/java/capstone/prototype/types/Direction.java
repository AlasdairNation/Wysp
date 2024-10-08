package capstone.prototype.types;

import java.util.EnumMap;
import java.util.Map;

public enum Direction {
    NORTH, SOUTH, EAST, WEST, STOP;

    public static final Map<Direction, Direction> LEFT = new EnumMap<>(Direction.class);
    public static final Map<Direction, Direction> RIGHT = new EnumMap<>(Direction.class);
    public static final Map<Direction, Direction> REVERSE = new EnumMap<>(Direction.class);

    public static Direction fromString(String s) {
        s = s.toUpperCase();

        switch (s) {
            case "N":
                return NORTH;

            case "S":
                return SOUTH;

            case "E":
                return EAST;

            case "W":
                return WEST;

            case "X":
            case "STOP":
                return STOP;

            default:
                throw new IllegalArgumentException("Invalid direction string: " + s);
        }
    }

    static {
        // LEFT
        LEFT.put(NORTH, WEST);
        LEFT.put(SOUTH, EAST);
        LEFT.put(EAST, NORTH);
        LEFT.put(WEST, SOUTH);
        LEFT.put(STOP, STOP);

        // RIGHT
        for (Map.Entry<Direction, Direction> entry : LEFT.entrySet()) {
            RIGHT.put(entry.getValue(), entry.getKey());
        }

        // REVERSE
        REVERSE.put(NORTH, SOUTH);
        REVERSE.put(SOUTH, NORTH);
        REVERSE.put(EAST, WEST);
        REVERSE.put(WEST, EAST);
        REVERSE.put(STOP, STOP);
    }
}
