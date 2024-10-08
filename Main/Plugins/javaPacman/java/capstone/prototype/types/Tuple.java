package capstone.prototype.types;

public class Tuple<A, B> {
    public A first;
    public B second;

    public Tuple(A x, B y) {
        this.first = x;
        this.second = y;
    }

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof Tuple)) {
            return false;
        }

        Tuple<?, ?> other = (Tuple<?, ?>) obj;
        return this.first.equals(other.first) && this.second.equals(other.second);
    }
}
