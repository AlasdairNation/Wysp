package capstone.prototype.types;

public class Triple<A, B, C> {

    public A first;
    public B second;
    public C third;

    public Triple(A first, B second, C third) {
        this.first = first;
        this.second = second;
        this.third = third;
    }

    @Override
    public boolean equals(Object other) {
        if (!(other instanceof Triple)) {
            return false;
        }

        Triple<?, ?, ?> o = (Triple<?, ?, ?>) other;
        return this.first.equals(o.first) && this.second.equals(o.second) && this.third.equals(o.third);
    }
}
