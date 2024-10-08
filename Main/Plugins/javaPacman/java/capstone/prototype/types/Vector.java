package capstone.prototype.types;

public class Vector {

    public final double x;
    public final double y;

    public Vector(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public Direction toDirection() {
        double dx = this.x;
        double dy = this.y;

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
}
