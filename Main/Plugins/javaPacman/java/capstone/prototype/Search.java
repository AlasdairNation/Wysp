package capstone.prototype;

import java.util.*;
import java.util.function.BiFunction;

// import everything so that they all files get compiled
// TODO: finish
// capstone.prototype.game
import capstone.prototype.game.Actions;
import capstone.prototype.game.AgentState;
import capstone.prototype.game.Configuration;
import capstone.prototype.game.GameState;
import capstone.prototype.game.GameStateData;
import capstone.prototype.game.GhostRules;
import capstone.prototype.game.PacmanRules;

// capstone.prototype.problem
import capstone.prototype.problem.AnyFoodSearchProblem;
import capstone.prototype.problem.AStarCornersAgent;
import capstone.prototype.problem.AStarFoodSearchAgent;
import capstone.prototype.problem.ClosestDotSearchAgent;
import capstone.prototype.problem.CornersProblem;
import capstone.prototype.problem.FoodSearchProblem;
import capstone.prototype.problem.PositionSearchProblem;
import capstone.prototype.problem.SearchProblem;
import capstone.prototype.problem.StayEastSearchAgent;
import capstone.prototype.problem.StayWestSearchAgent;

// capstone.prototype.problem.states
import capstone.prototype.problem.states.CornersProblemState;
import capstone.prototype.problem.states.FoodSearchProblemState;
import capstone.prototype.problem.states.PositionSearchProblemState;
import capstone.prototype.problem.states.ProblemState;

// capstone.prototype.types
import capstone.prototype.types.Direction;
import capstone.prototype.types.Grid;
import capstone.prototype.types.Layout;
import capstone.prototype.types.Position;
import capstone.prototype.types.Triple;
import capstone.prototype.types.Tuple;
import capstone.prototype.types.Vector;

// capstone.prototype.utils
import capstone.prototype.utils.Converter;
import capstone.prototype.utils.Utils;

// capstone.prototype.utils.heuristics
import capstone.prototype.utils.heuristics.Heuristics;

public class Search {

    public static void main(String[] args) {
        System.out.println("[java] Search.java loaded");
        // assign unused variables so that java actually compiles them
        Converter unused = new Converter();

        unused.nothing();
        Heuristics.nothing();
    }

    public static List<Direction> tinyMazeSearch(SearchProblem problem) {
        // s, s, w, s, w, w, s, w
        return Arrays.asList(
                Direction.SOUTH, Direction.SOUTH, Direction.WEST, Direction.SOUTH,
                Direction.WEST, Direction.WEST, Direction.SOUTH, Direction.WEST);
    }

    public static List<Direction> depthFirstSearch(SearchProblem _problem) {
        if (_problem instanceof PositionSearchProblem) {

            PositionSearchProblem problem = (PositionSearchProblem) _problem;
            Stack<Tuple<PositionSearchProblemState, List<Direction>>> stackXY = new Stack<>();
            List<Position> visited = new ArrayList<>();
            List<Direction> path = new ArrayList<>();

            if (problem.isGoalState(problem.getStartState()))
                return path;

            PositionSearchProblemState startState = (PositionSearchProblemState) problem.getStartState();
            stackXY.push(new Tuple<>(startState, new ArrayList<>()));

            while (true) {
                // can't find solution
                if (stackXY.isEmpty())
                    return new ArrayList<>();

                // get info about current state
                Tuple<PositionSearchProblemState, List<Direction>> entry = stackXY.pop();
                PositionSearchProblemState currentState = entry.first;
                Position xy = currentState.position;
                path = entry.second;
                visited.add(xy);

                // if reached goal
                if (problem.isGoalState(currentState))
                    return path;

                List<Triple<ProblemState, Direction, Integer>> succ = problem.getSuccessors(currentState);
                if (succ == null)
                    continue;

                for (Triple<ProblemState, Direction, Integer> item : succ) {
                    Position nextXY = ((PositionSearchProblemState) item.first).position;

                    if (!visited.contains(nextXY)) {
                        List<Direction> newPath = new ArrayList<>(path);
                        newPath.add(item.second);
                        stackXY.push(new Tuple<>((PositionSearchProblemState) item.first, newPath));
                    }
                }
            }
        }

        else if (_problem instanceof CornersProblem) {
            CornersProblem problem = (CornersProblem) _problem;
            Stack<Tuple<CornersProblemState, List<Direction>>> stackXY = new Stack<>();
            List<Position> visited = new ArrayList<>();
            List<Direction> path = new ArrayList<>();

            if (problem.isGoalState(problem.getStartState()))
                return path;

            CornersProblemState startState = (CornersProblemState) problem.getStartState();
            stackXY.push(new Tuple<>(startState, new ArrayList<>()));

            while (true) {
                if (stackXY.isEmpty())
                    return new ArrayList<>();

                // get info about current state
                Tuple<CornersProblemState, List<Direction>> entry = stackXY.pop();
                CornersProblemState cps = entry.first;
                Tuple<Position, List<Integer>> state = cps.state;
                path = entry.second;
                visited.add(state.first);

                // if reached goal
                if (problem.isGoalState(cps))
                    return path;

                List<Triple<ProblemState, Direction, Integer>> succ = problem.getSuccessors(cps);
                if (succ == null || succ.isEmpty())
                    continue;

                for (Triple<ProblemState, Direction, Integer> item : succ) {
                    Position temp = ((CornersProblemState) item.first).state.first;

                    if (!visited.contains(temp)) {
                        List<Direction> newPath = new ArrayList<>(path);
                        newPath.add(item.second);
                        CornersProblemState nextState = (CornersProblemState) item.first;
                        stackXY.push(new Tuple<>(nextState, newPath));
                    }
                }
            }
        }

        else if (_problem instanceof FoodSearchProblem) {
            FoodSearchProblem problem = (FoodSearchProblem) _problem;
            Stack<Tuple<FoodSearchProblemState, List<Direction>>> stackXY = new Stack<>();
            List<Position> visited = new ArrayList<>();
            List<Direction> path = new ArrayList<>();

            if (problem.isGoalState(problem.getStartState()))
                return path;

            FoodSearchProblemState startState = (FoodSearchProblemState) problem.getStartState();
            stackXY.push(new Tuple<>(startState, new ArrayList<>()));

            while (true) {
                if (stackXY.isEmpty())
                    return new ArrayList<>();

                // get info about current state
                Tuple<FoodSearchProblemState, List<Direction>> entry = stackXY.pop();
                FoodSearchProblemState fsp = entry.first;
                Tuple<Position, Grid> state = fsp.state;
                path = entry.second;
                visited.add(state.first);

                // if reached goal
                if (problem.isGoalState(fsp))
                    return path;

                List<Triple<ProblemState, Direction, Integer>> succ = problem.getSuccessors(fsp);
                if (succ == null)
                    continue;

                for (Triple<ProblemState, Direction, Integer> item : succ) {
                    Position temp = ((FoodSearchProblemState) item.first).state.first;

                    if (!visited.contains(temp)) {
                        List<Direction> newPath = new ArrayList<>(path);
                        newPath.add(item.second);
                        FoodSearchProblemState nextState = (FoodSearchProblemState) item.first;
                        stackXY.push(new Tuple<>(nextState, newPath));
                    }
                }
            }
        }

        throw new UnsupportedOperationException(
                "Unimplemented method 'depthFirstSearch' for unknown SearchProblem type");
    }

    public static List<Direction> breadthFirstSearch(SearchProblem _problem) {
        if (_problem instanceof PositionSearchProblem) {

            PositionSearchProblem problem = (PositionSearchProblem) _problem;
            Queue<Tuple<PositionSearchProblemState, List<Direction>>> queueXY = new LinkedList<>();
            List<Position> visited = new ArrayList<>();
            List<Direction> path = new ArrayList<>();

            if (problem.isGoalState(problem.getStartState()))
                return path;

            PositionSearchProblemState startState = (PositionSearchProblemState) problem.getStartState();
            queueXY.add(new Tuple<>(startState, new ArrayList<>()));

            while (true) {
                // can't find solution
                if (queueXY.isEmpty())
                    return new LinkedList<>();

                // get info about current state
                Tuple<PositionSearchProblemState, List<Direction>> entry = queueXY.poll();
                PositionSearchProblemState currentState = entry.first;
                Position xy = currentState.position;
                path = entry.second;
                visited.add(xy);

                // if reached goal terminate
                if (problem.isGoalState(currentState))
                    return path;

                List<Triple<ProblemState, Direction, Integer>> succ = problem.getSuccessors(currentState);
                if (succ == null)
                    continue;

                for (Triple<ProblemState, Direction, Integer> item : succ) {
                    PositionSearchProblemState successorState = (PositionSearchProblemState) item.first;
                    Direction direction = item.second;

                    // Check if the successor has been visited or is already in the queue
                    if (!visited.contains(successorState.position) &&
                            queueXY.stream().noneMatch(t -> t.first.position.equals(successorState.position))) {

                        List<Direction> newPath = new ArrayList<>(path); // Create a new path
                        newPath.add(direction); // Add the direction to the path
                        // Add the new state to the queue
                        queueXY.add(new Tuple<>(new PositionSearchProblemState(successorState.position), newPath));
                    }
                }
            }
        }

        else if (_problem instanceof CornersProblem) {
            CornersProblem problem = (CornersProblem) _problem;
            Queue<Tuple<CornersProblemState, List<Direction>>> queueXY = new LinkedList<>();
            List<Position> visited = new ArrayList<>();
            List<Direction> path = new ArrayList<>();

            if (problem.isGoalState(problem.getStartState()))
                return path;

            CornersProblemState startState = (CornersProblemState) problem.getStartState();
            queueXY.add(new Tuple<>(startState, new ArrayList<>()));

            while (true) {
                if (queueXY.isEmpty())
                    return new LinkedList<>();

                // get info about current state
                Tuple<CornersProblemState, List<Direction>> entry = queueXY.poll();
                CornersProblemState cps = entry.first;
                Tuple<Position, List<Integer>> state = cps.state;
                path = entry.second;
                visited.add(state.first);

                // if reached goal
                if (problem.isGoalState(cps))
                    return path;

                List<Triple<ProblemState, Direction, Integer>> succ = problem.getSuccessors(cps);
                if (succ == null || succ.isEmpty())
                    continue;

                for (Triple<ProblemState, Direction, Integer> item : succ) {
                    Position temp = ((CornersProblemState) item.first).state.first;

                    if (!visited.contains(temp)) {
                        List<Direction> newPath = new ArrayList<>(path);
                        newPath.add(item.second);
                        CornersProblemState nextState = (CornersProblemState) item.first;
                        queueXY.add(new Tuple<>(nextState, newPath));
                    }
                }
            }
        }

        else if (_problem instanceof FoodSearchProblem) {
            FoodSearchProblem problem = (FoodSearchProblem) _problem;
            Queue<Tuple<FoodSearchProblemState, List<Direction>>> queueXY = new LinkedList<>();
            List<Position> visited = new ArrayList<>();
            List<Direction> path = new ArrayList<>();

            if (problem.isGoalState(problem.getStartState()))
                return path;

            FoodSearchProblemState startState = (FoodSearchProblemState) problem.getStartState();
            queueXY.add(new Tuple<>(startState, new ArrayList<>()));

            while (true) {
                if (queueXY.isEmpty())
                    return new LinkedList<>();

                // get info about current state
                Tuple<FoodSearchProblemState, List<Direction>> entry = queueXY.poll();
                FoodSearchProblemState fsp = entry.first;
                Tuple<Position, Grid> state = fsp.state;
                path = entry.second;
                visited.add(state.first);

                // if reached goal
                if (problem.isGoalState(fsp))
                    return path;

                List<Triple<ProblemState, Direction, Integer>> succ = problem.getSuccessors(fsp);
                if (succ == null)
                    continue;

                for (Triple<ProblemState, Direction, Integer> item : succ) {
                    Position temp = ((FoodSearchProblemState) item.first).state.first;

                    if (!visited.contains(temp)) {
                        List<Direction> newPath = new ArrayList<>(path);
                        newPath.add(item.second);
                        FoodSearchProblemState nextState = (FoodSearchProblemState) item.first;
                        queueXY.add(new Tuple<>(nextState, newPath));
                    }
                }
            }
        }

        throw new UnsupportedOperationException(
                "Unimplemented method 'depthFirstSearch' for unknown SearchProblem type");
    }

    public static List<Direction> uniformCostSearch(SearchProblem _problem) {
        if (_problem instanceof PositionSearchProblem) {

            PositionSearchProblem problem = (PositionSearchProblem) _problem;
            // queueXY: ( (position),[path] ), priority
            PriorityQueue<Tuple<Tuple<Position, List<Direction>>, Integer>> queueXY = new PriorityQueue<>(
                    (a, b) -> Integer.compare(a.second, b.second));

            List<Position> visited = new ArrayList<>();
            List<Direction> path = new ArrayList<>();

            if (problem.isGoalState(problem.getStartState()))
                return path;

            PositionSearchProblemState startState = (PositionSearchProblemState) problem.getStartState();
            queueXY.add(new Tuple<>(new Tuple<>(startState.position, new ArrayList<>()), 0));

            while (true) {
                if (queueXY.isEmpty())
                    return new ArrayList<>();

                Tuple<Tuple<Position, List<Direction>>, Integer> entry = queueXY.poll();
                Position xy = entry.first.first;
                path = entry.first.second;
                visited.add(xy);

                if (problem.isGoalState(new PositionSearchProblemState(xy)))
                    return path;

                List<Triple<ProblemState, Direction, Integer>> succ = problem
                        .getSuccessors(new PositionSearchProblemState(xy));

                if (succ == null)
                    continue;

                for (Triple<ProblemState, Direction, Integer> item : succ) {
                    Position nextXY = ((PositionSearchProblemState) item.first).position;

                    // if item[0] not in visited:
                    // position not in `visited`

                    // item[0] not in (state[2][0] for state in queueXY.heap) :
                    // state[2] -> state[2][0] is pos and state[2][1] is path

                    if (!visited.contains(nextXY) && queueXY.stream().noneMatch(t -> t.first.first.equals(nextXY))) {
                        List<Direction> newPath = new ArrayList<>(path);
                        newPath.add(item.second);
                        queueXY.add(new Tuple<>(new Tuple<>(nextXY, newPath), item.third));
                    }

                    /*
                     * elif item[0] not in visited and (
                     * item[0] in (state[2][0] for state in queueXY.heap)
                     * ):
                     */
                    else if (!visited.contains(nextXY)
                            && queueXY.stream().anyMatch(t -> t.first.first.equals(nextXY))) {
                        // find old pri
                        /*
                         * for state in queueXY.heap:
                         * if state[2][0] == item[0]:
                         */
                        int oldPri = -1;
                        for (Tuple<Tuple<Position, List<Direction>>, Integer> state : queueXY) {
                            if (state.first.first.equals(nextXY)) {
                                oldPri = problem.getCostOfActions(state.first.second);
                            }
                        }
                        // newPri = problem.getCostOfActions(path + [item[1]])
                        List<Direction> newPath = new ArrayList<>(path);
                        newPath.add(item.second);
                        int newPri = problem.getCostOfActions(newPath);

                        // State is cheaper with his hew father -> update and fix parent
                        if (oldPri > newPri) {
                            // update by removing the old state and adding the new state
                            queueXY.removeIf(t -> t.first.first.equals(nextXY));
                            queueXY.add(new Tuple<>(new Tuple<>(nextXY, newPath), newPri));
                        }
                    }
                }
            }
        }

        else if (_problem instanceof CornersProblem) {
            CornersProblem problem = (CornersProblem) _problem;
            // queueXY: ( (position),[path] ), priority
            PriorityQueue<Tuple<Tuple<Position, List<Direction>>, Integer>> queueXY = new PriorityQueue<>(
                    (a, b) -> Integer.compare(a.second, b.second));

            List<Position> visited = new ArrayList<>();
            List<Direction> path = new ArrayList<>();

            if (problem.isGoalState(problem.getStartState()))
                return path;

            CornersProblemState startState = (CornersProblemState) problem.getStartState();
            queueXY.add(new Tuple<>(new Tuple<>(startState.state.first, new ArrayList<>()), 0));

            while (true) {
                if (queueXY.isEmpty())
                    return new ArrayList<>();

                Tuple<Tuple<Position, List<Direction>>, Integer> entry = queueXY.poll();
                Position xy = entry.first.first;
                path = entry.first.second;
                visited.add(xy);

                if (problem.isGoalState(new CornersProblemState(xy, startState.state.second)))
                    return path;

                List<Triple<ProblemState, Direction, Integer>> succ = problem
                        .getSuccessors(new CornersProblemState(xy, startState.state.second));

                if (succ == null)
                    continue;

                for (Triple<ProblemState, Direction, Integer> item : succ) {
                    Position nextXY = ((CornersProblemState) item.first).state.first;

                    if (!visited.contains(nextXY) && queueXY.stream().noneMatch(t -> t.first.first.equals(nextXY))) {
                        List<Direction> newPath = new ArrayList<>(path);
                        newPath.add(item.second);
                        queueXY.add(new Tuple<>(new Tuple<>(nextXY, newPath), item.third));
                    }

                    else if (!visited.contains(nextXY)
                            && queueXY.stream().anyMatch(t -> t.first.first.equals(nextXY))) {
                        int oldPri = -1;
                        for (Tuple<Tuple<Position, List<Direction>>, Integer> state : queueXY) {
                            if (state.first.first.equals(nextXY)) {
                                oldPri = problem.getCostOfActions(state.first.second);
                            }
                        }
                        List<Direction> newPath = new ArrayList<>(path);
                        newPath.add(item.second);
                        int newPri = problem.getCostOfActions(newPath);

                        if (oldPri > newPri) {
                            queueXY.removeIf(t -> t.first.first.equals(nextXY));
                            queueXY.add(new Tuple<>(new Tuple<>(nextXY, newPath), newPri));
                        }
                    }
                }
            }
        }

        else if (_problem instanceof FoodSearchProblem) {
            FoodSearchProblem problem = (FoodSearchProblem) _problem;
            PriorityQueue<Tuple<Tuple<Position, List<Direction>>, Integer>> queueXY = new PriorityQueue<>(
                    (a, b) -> Integer.compare(a.second, b.second));

            List<Position> visited = new ArrayList<>();
            List<Direction> path = new ArrayList<>();

            if (problem.isGoalState(problem.getStartState()))
                return path;

            FoodSearchProblemState startState = (FoodSearchProblemState) problem.getStartState();
            queueXY.add(new Tuple<>(new Tuple<>(startState.state.first, new ArrayList<>()), 0));

            while (true) {
                if (queueXY.isEmpty())
                    return new ArrayList<>();

                Tuple<Tuple<Position, List<Direction>>, Integer> entry = queueXY.poll();
                Position xy = entry.first.first;
                path = entry.first.second;
                visited.add(xy);

                if (problem.isGoalState(new FoodSearchProblemState(xy, startState.state.second)))
                    return path;

                List<Triple<ProblemState, Direction, Integer>> succ = problem
                        .getSuccessors(new FoodSearchProblemState(xy, startState.state.second));

                if (succ == null)
                    continue;

                for (Triple<ProblemState, Direction, Integer> item : succ) {
                    Position nextXY = ((FoodSearchProblemState) item.first).state.first;

                    if (!visited.contains(nextXY) && queueXY.stream().noneMatch(t -> t.first.first.equals(nextXY))) {
                        List<Direction> newPath = new ArrayList<>(path);
                        newPath.add(item.second);
                        queueXY.add(new Tuple<>(new Tuple<>(nextXY, newPath), item.third));
                    }

                    else if (!visited.contains(nextXY)
                            && queueXY.stream().anyMatch(t -> t.first.first.equals(nextXY))) {
                        int oldPri = -1;
                        for (Tuple<Tuple<Position, List<Direction>>, Integer> state : queueXY) {
                            if (state.first.first.equals(nextXY)) {
                                oldPri = problem.getCostOfActions(state.first.second);
                            }
                        }
                        List<Direction> newPath = new ArrayList<>(path);
                        newPath.add(item.second);
                        int newPri = problem.getCostOfActions(newPath);

                        if (oldPri > newPri) {
                            queueXY.removeIf(t -> t.first.first.equals(nextXY));
                            queueXY.add(new Tuple<>(new Tuple<>(nextXY, newPath), newPri));
                        }
                    }
                }
            }
        }

        // If the problem type is not supported, throw an error
        throw new UnsupportedOperationException("UniformCostSearch not implemented for this problem type");
    }

    public static List<Direction> aStarSearch(SearchProblem _problem,
            BiFunction<ProblemState, SearchProblem, Double> _heuristics) {
        if (_heuristics == null) {
            // holy hell i figured it out
            _heuristics = (state, problem) -> nullHeuristic(problem);
        }
        // Java(536871575)
        final BiFunction<ProblemState, SearchProblem, Double> heuristics = _heuristics;

        if (_problem instanceof PositionSearchProblem) {
            PositionSearchProblem problem = (PositionSearchProblem) _problem;

            // create a priority q, priority is determined by applying heuristics
            PriorityQueue<Tuple<PositionSearchProblemState, List<Direction>>> queueXY = new PriorityQueue<>(
                    // combining f() into one
                    (a, b) -> Double.compare(heuristics.apply(a.first, problem) + problem.getCostOfActions(a.second),
                            heuristics.apply(b.first, problem) + problem.getCostOfActions(b.second)));

            List<Direction> path = new ArrayList<>();
            List<Position> visited = new ArrayList<>();

            if (problem.isGoalState(problem.getStartState()))
                return path;

            // Add initial state. Path is an empty list
            Tuple<PositionSearchProblemState, List<Direction>> element = new Tuple<>(
                    (PositionSearchProblemState) problem.getStartState(), new ArrayList<>());
            queueXY.add(element);

            while (true) {
                if (queueXY.isEmpty())
                    return new ArrayList<>();

                Tuple<PositionSearchProblemState, List<Direction>> entry = queueXY.poll();
                Position xy = entry.first.position;
                path = entry.second;

                if (visited.contains(xy))
                    continue;
                visited.add(xy);

                if (problem.isGoalState(entry.first))
                    return path;

                List<Triple<ProblemState, Direction, Integer>> succ = problem.getSuccessors(entry.first);
                if (succ == null)
                    continue;

                for (Triple<ProblemState, Direction, Integer> item : succ) {
                    Position nextXY = ((PositionSearchProblemState) item.first).position;

                    if (!visited.contains(nextXY)) {
                        List<Direction> newPath = new ArrayList<>(path);
                        newPath.add(item.second);
                        queueXY.add(new Tuple<>((PositionSearchProblemState) item.first, newPath));
                    }
                }
            }
        }

        else if (_problem instanceof CornersProblem) {
            CornersProblem problem = (CornersProblem) _problem;

            // create a priority queue where the priority is determined by applying
            // heuristics
            PriorityQueue<Tuple<CornersProblemState, List<Direction>>> queueXY = new PriorityQueue<>(
                    (a, b) -> Double.compare(heuristics.apply(a.first, problem) + problem.getCostOfActions(a.second),
                            heuristics.apply(b.first, problem) + problem.getCostOfActions(b.second)));

            List<Direction> path = new ArrayList<>();
            List<Position> visited = new ArrayList<>();

            if (problem.isGoalState(problem.getStartState()))
                return path;

            // Add initial state. Path is an empty list
            Tuple<CornersProblemState, List<Direction>> element = new Tuple<>(
                    (CornersProblemState) problem.getStartState(), new ArrayList<>());
            queueXY.add(element);

            while (true) {
                if (queueXY.isEmpty())
                    return new ArrayList<>();

                Tuple<CornersProblemState, List<Direction>> entry = queueXY.poll();
                Tuple<Position, List<Integer>> state = entry.first.state;
                path = entry.second;

                if (visited.contains(state.first))
                    continue;
                visited.add(state.first);

                if (problem.isGoalState(entry.first))
                    return path;

                List<Triple<ProblemState, Direction, Integer>> succ = problem.getSuccessors(entry.first);
                if (succ == null)
                    continue;

                for (Triple<ProblemState, Direction, Integer> item : succ) {
                    Position nextXY = ((CornersProblemState) item.first).state.first;

                    if (!visited.contains(nextXY)) {
                        List<Direction> newPath = new ArrayList<>(path);
                        newPath.add(item.second);
                        queueXY.add(new Tuple<>((CornersProblemState) item.first, newPath));
                    }
                }
            }
        }

        else if (_problem instanceof FoodSearchProblem) {
            FoodSearchProblem problem = (FoodSearchProblem) _problem;

            // create a priority queue where the priority is determined by applying
            // heuristics
            PriorityQueue<Tuple<FoodSearchProblemState, List<Direction>>> queueXY = new PriorityQueue<>(
                    (a, b) -> Double.compare(heuristics.apply(a.first, problem) + problem.getCostOfActions(a.second),
                            heuristics.apply(b.first, problem) + problem.getCostOfActions(b.second)));

            List<Direction> path = new ArrayList<>();
            List<Position> visited = new ArrayList<>();

            if (problem.isGoalState(problem.getStartState()))
                return path;

            // Add initial state. Path is an empty list
            Tuple<FoodSearchProblemState, List<Direction>> element = new Tuple<>(
                    (FoodSearchProblemState) problem.getStartState(), new ArrayList<>());
            queueXY.add(element);

            while (true) {
                if (queueXY.isEmpty())
                    return new ArrayList<>();

                Tuple<FoodSearchProblemState, List<Direction>> entry = queueXY.poll();
                Tuple<Position, Grid> state = entry.first.state;
                path = entry.second;

                if (visited.contains(state.first))
                    continue;
                visited.add(state.first);

                if (problem.isGoalState(entry.first))
                    return path;

                List<Triple<ProblemState, Direction, Integer>> succ = problem.getSuccessors(entry.first);
                if (succ == null)
                    continue;

                for (Triple<ProblemState, Direction, Integer> item : succ) {
                    Position nextXY = ((FoodSearchProblemState) item.first).state.first;

                    if (!visited.contains(nextXY)) {
                        List<Direction> newPath = new ArrayList<>(path);
                        newPath.add(item.second);
                        queueXY.add(new Tuple<>((FoodSearchProblemState) item.first, newPath));
                    }
                }
            }
        }

        throw new UnsupportedOperationException(
                "Unimplemented method 'aStarSearch' for unknown SearchProblem type");
    }

    public static double nullHeuristic(SearchProblem problem) {
        return 0d;
    }
}