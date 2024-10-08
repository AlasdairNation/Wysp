package capstone.prototype.types;

public class Position {

    public final double x;
    public final double y;
    private static final double TOLERANCE = 0.001;

    public Position(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public String stringCoords() {
        return "(" + x + ", " + y + ")";
    }

    @Override
    public boolean equals(Object other) {
        if (!(other instanceof Position)) {
            return false;
        }

        Position o = (Position) other;
        return Math.abs(this.x - o.x) < TOLERANCE && Math.abs(this.y - o.y) < TOLERANCE;
    }

    @Override
    public String toString() {
        return "Position(" + x + ", " + y + ")";
    }
}
