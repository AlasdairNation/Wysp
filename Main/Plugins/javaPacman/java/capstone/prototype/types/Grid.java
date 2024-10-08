package capstone.prototype.types;

import java.util.ArrayList;
import java.util.List;

public class Grid {
    public final int width;
    public final int height;
    public List<List<Boolean>> data;
    private final int CELLS_PER_INT = 30;

    public Grid(int width, int height) {
        this(width, height, false);
    }

    public Grid(int width, int height, boolean initialValue) {
        this.width = width;
        this.height = height;
        this.data = new ArrayList<>();

        // fill the grid with the initial value
        for (int x = 0; x < width; x++) {
            List<Boolean> row = new ArrayList<>();
            for (int y = 0; y < height; y++) {
                row.add(initialValue);
            }
            this.data.add(row);
        }
    }

    public Grid(int width, int height, boolean initialValue, List<Long> bitRepresentation) {
        this(width, height, initialValue);
        if (bitRepresentation != null) {
            unpackBits(bitRepresentation);
        }
    }

    public Grid copy() {
        Grid g = new Grid(this.width, this.height, false);

        for (int x = 0; x < this.width; x++) {
            for (int y = 0; y < this.height; y++) {
                g.data.get(x).set(y, this.data.get(x).get(y));
            }
        }

        return g;
    }

    public Grid deepCopy() {
        return this.copy();
    }

    public Grid shallowCopy() {
        Grid g = new Grid(this.width, this.height, false);
        g.data = this.data;
        return g;
    }

    public int count(boolean item) {
        int count = 0;
        for (List<Boolean> row : this.data) {
            for (boolean cell : row) {
                if (cell == item) {
                    count++;
                }
            }
        }
        return count;
    }

    public int count() {
        return count(true);
    }

    public List<Tuple<Integer, Integer>> asList(boolean key) {
        List<Tuple<Integer, Integer>> l = new ArrayList<>();

        for (int x = 0; x < this.width; x++) {
            for (int y = 0; y < this.height; y++) {
                if (this.data.get(x).get(y) == key) {
                    l.add(new Tuple<>(x, y));
                }
            }
        }
        return l;
    }

    public List<Tuple<Integer, Integer>> asList() {
        return asList(true);
    }

    public List<Integer> packBits() {
        List<Integer> bits = new ArrayList<>();
        bits.add(this.width);
        bits.add(this.height);

        int currentInt = 0;

        for (int i = 0; i < (int) (this.height * this.width); i++) {
            int bit = this.CELLS_PER_INT - (i % this.CELLS_PER_INT) - 1;
            int x = (int) cellIndexToPosition(i).x;
            int y = (int) cellIndexToPosition(i).y;

            if (this.data.get(x).get(y))
                currentInt += (int) Math.pow(2, bit);

            if ((i + 1) % this.CELLS_PER_INT == 0) {
                bits.add(currentInt);
                currentInt = 0;
            }
        }
        bits.add(currentInt);
        return bits;
    }

    private Position cellIndexToPosition(int index) {
        int x = Math.floorDiv(index, this.height);
        int y = index % this.height;
        return new Position(x, y);
    }

    private void unpackBits(List<Long> bits) {
        int cell = 0;

        for (Long packed : bits) {
            for (boolean bit : unpackInt(packed, this.CELLS_PER_INT)) {
                if (cell == this.width * this.height)
                    break;

                int x = (int) cellIndexToPosition(cell).x;
                int y = (int) cellIndexToPosition(cell).y;

                this.data.get(x).set(y, bit);
                cell++;
            }
        }
    }

    private List<Boolean> unpackInt(Long packed, int size) {
        List<Boolean> bools = new ArrayList<>();
        if (packed < 0)
            throw new IllegalArgumentException("must be a positive integer");

        for (int i = 0; i < size; i++) {
            int n = (int) Math.pow(2, this.CELLS_PER_INT - i - 1);

            if (packed >= n) {
                bools.add(true);
                packed -= n;
            } else
                bools.add(false);
        }
        return bools;
    }

    @Override
    public String toString() {
        /**
         * Original Python code:
         * 
         * out = [[str(self.data[x][y])[0] for x in range(self.width)] for y in
         * range(self.height)]
         * out.reverse()
         * return '\n'.join([''.join(x) for x in out])
         */

        List<List<String>> outer = new ArrayList<>();

        for (int y = 0; y < this.height; y++) {
            List<String> inner = new ArrayList<>();
            for (int x = 0; x < this.width; x++) {
                inner.add(this.data.get(x).get(y) ? "T" : "F");
            }
            outer.add(inner);
        }

        // reverse outer and then join the inner lists
        StringBuilder sb = new StringBuilder();
        for (int i = outer.size() - 1; i >= 0; i--) {
            sb.append(String.join("", outer.get(i)));
            sb.append("\n");
        }

        // pray
        return sb.toString();
    }

    @Override
    public boolean equals(Object other) {
        if (!(other instanceof Grid))
            return false;

        Grid o = (Grid) other;
        return this.data.equals(o.data);
    }
}
