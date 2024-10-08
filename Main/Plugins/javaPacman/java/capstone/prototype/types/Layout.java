package capstone.prototype.types;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public class Layout {
    public List<String> layoutText;
    public int width;
    public int height;
    public Grid walls;
    public Grid food;
    public List<Position> capsules;

    public List<Tuple<Boolean, Position>> agentPositions;
    private List<Tuple<Integer, Tuple<Integer, Integer>>> tempAgentPositions;

    public int numGhosts;
    public int totalFood;

    public Layout(List<String> layoutText) {
        this.width = layoutText.get(0).length();
        this.height = layoutText.size();
        this.walls = new Grid(this.width, this.height, false);
        this.food = new Grid(this.width, this.height, false);
        this.capsules = new ArrayList<>();
        this.agentPositions = new ArrayList<>();
        this.tempAgentPositions = new ArrayList<>();
        this.numGhosts = 0;
        processLayoutText(layoutText);
        this.layoutText = layoutText;
        this.totalFood = this.food.data.size();
    }

    public int getNumGhosts() {
        return this.numGhosts;
    }

    public boolean isWall(Position pos) {
        return this.walls.data.get((int) pos.x).get((int) pos.y);
    }

    public Position getRandomLegalPosition() {
        Random random = new Random();
        int x = random.nextInt(this.width);
        int y = random.nextInt(this.height);
        Position pos = new Position(x, y);

        while (isWall(pos)) {
            x = random.nextInt(this.width);
            y = random.nextInt(this.height);
            pos = new Position(x, y);
        }
        return pos;
    }

    public Position getRandomCorner() {
        List<Position> poses = Arrays.asList(
                new Position(1, 1),
                new Position(1, this.height - 2),
                new Position(this.width - 2, 1),
                new Position(this.width - 2, this.height - 2));
        Random random = new Random();

        return poses.get(random.nextInt(poses.size()));
    }

    public double manhattanDistance(Position pos1, Position pos2) {
        // TODO: maybe move this to a utility class
        return Math.abs(pos1.x - pos2.x) + Math.abs(pos1.y - pos2.y);
    }

    public Position getFurthestCorner(Position pacPos) {
        /**
         * poses = [
         * (1, 1),
         * (1, self.height - 2),
         * (self.width - 2, 1),
         * (self.width - 2, self.height - 2),
         * ]
         * dist, pos = max([(manhattanDistance(p, pacPos), p) for p in poses])
         * return pos
         */
        List<Position> poses = Arrays.asList(
                new Position(1, 1),
                new Position(1, this.height - 2),
                new Position(this.width - 2, 1),
                new Position(this.width - 2, this.height - 2));

        double maxDist = 0;
        Position maxPos = null;

        for (Position p : poses) {
            double dist = manhattanDistance(p, pacPos);
            if (dist > maxDist) {
                maxDist = dist;
                maxPos = p;
            }
        }
        return maxPos;
    }

    public Layout deepCopy() {
        List<String> copy = new ArrayList<>();
        for (String s : this.layoutText) {
            copy.add(s + "");
        }
        return new Layout(copy);
    }

    private void processLayoutText(List<String> lt) {
        int maxY = this.height - 1;
        for (int y = 0; y < this.height; y++) {
            for (int x = 0; x < this.width; x++) {
                char layoutChar = lt.get(maxY - y).charAt(x);
                processLayoutChar(x, y, layoutChar);
            }
        }
        // self.agentPositions.sort() -> thanks python
        // tempAgentPositions has the format (numeric, (x, y))
        // sort by the numeric value, then x, then y
        this.tempAgentPositions.sort((a, b) -> {
            // if `numeric` is equal, check x
            if (a.first.equals(b.first)) {
                // if `x` is equal, check y
                if (a.second.first.equals(b.second.first)) {
                    // compare y
                    return a.second.second.compareTo(b.second.second);
                }
                return a.second.first.compareTo(b.second.first);
            }
            return a.first.compareTo(b.first);
        });

        // self.agentPositions = [(i == 0, pos) for i, pos in self.temp]
        for (Tuple<Integer, Tuple<Integer, Integer>> t : this.tempAgentPositions) {
            Position p = new Position(t.second.first, t.second.second);
            this.agentPositions.add(new Tuple<>(t.first == 0, p));
        }
    }

    private void processLayoutChar(int x, int y, char lc) {
        if (lc == '%') {
            this.walls.data.get(x).set(y, true);
        }
        if (lc == '.') {
            this.food.data.get(x).set(y, true);
        }
        if (lc == 'o') {
            this.capsules.add(new Position(x, y));
        }
        if (lc == 'P') {
            this.tempAgentPositions.add(new Tuple<>(0, new Tuple<Integer, Integer>(x, y)));
        }
        if (lc == 'G') {
            this.tempAgentPositions.add(new Tuple<>(1, new Tuple<Integer, Integer>(x, y)));
            this.numGhosts += 1;
        }
        if (lc == '1' || lc == '2' || lc == '3' || lc == '4') {
            this.tempAgentPositions.add(new Tuple<>(Integer.parseInt(String.valueOf(lc)), new Tuple<>(x, y)));
            this.numGhosts += 1;
        }
    }

    @Override
    public String toString() {
        return String.join("\n", this.layoutText);
    }
}
