package capstone.prototype.game;

import capstone.prototype.types.Direction;
import capstone.prototype.types.Position;
import capstone.prototype.types.Vector;

public class Configuration {
    public Position pos;
    public final Direction direction;

    public Configuration(Position pos, Direction direction) {
        this.pos = pos;
        this.direction = direction;
    }

    public Position getPosition() {
        return this.pos;
    }

    public Direction getDirection() {
        return this.direction;
    }

    public Configuration generateSuccessor(Vector vector) {
        Direction d = vector.toDirection();
        if (d == Direction.STOP)
            d = this.direction;

        return new Configuration(new Position(this.pos.x + vector.x, this.pos.y + vector.y), d);
    }

    @Override
    public boolean equals(Object other) {
        if (!(other instanceof Configuration)) {
            return false;
        }

        Configuration o = (Configuration) other;
        return this.pos.equals(o.pos) && this.direction == o.direction;
    }
}
