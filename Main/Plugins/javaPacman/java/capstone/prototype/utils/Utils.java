package capstone.prototype.utils;

import capstone.prototype.types.Position;

public class Utils {
    public static Position nearestPoint(Position pos) {
        double currentRow = pos.x;
        double currentCol = pos.y;

        int gridRow = (int) (currentRow + 0.5);
        int gridCol = (int) (currentCol + 0.5);

        Position newPos = new Position(gridRow, gridCol);
        return newPos;
    }

    public static Double manhattanDistance(Position pos1, Position pos2) {
        return Math.abs(pos1.x - pos2.x) + Math.abs(pos1.y - pos2.y);
    }
}
