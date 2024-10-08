package capstone.prototype.utils;

import java.util.ArrayList;
import java.util.List;

import capstone.prototype.game.AgentState;
import capstone.prototype.game.Configuration;
import capstone.prototype.game.GameStateData;
import capstone.prototype.types.Direction;
import capstone.prototype.types.Grid;
import capstone.prototype.types.Layout;
import capstone.prototype.types.Position;
import capstone.prototype.types.Tuple;

public class Converter {

    public GameStateData fromPythonData(int width, int height, List<String> layoutText, List<List<Boolean>> foodArr,
            List<List<Long>> capsulePosInt, List<AgentState> agentStates) {
        GameStateData state = new GameStateData();

        state.layout = new Layout(layoutText);
        // state.food = new Grid(width, height, false, foodBits);
        state.food = new Grid(width, height, false);

        // assert that foodArr and food.data have the same dimensions
        assert foodArr.size() == state.food.width;
        assert foodArr.get(0).size() == state.food.height;
        // copy the foodArr to the food.data
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                state.food.data.get(x).set(y, foodArr.get(x).get(y));
            }
        }

        state.capsules = new ArrayList<>();
        state.agentStates = new ArrayList<>();

        for (AgentState agentState : agentStates)
            state.agentStates.add(agentState.copy());

        for (List<Long> pos : capsulePosInt)
            state.capsules.add(new Position(pos.get(0), pos.get(1)));

        return state;
    }

    public GameStateData otherPythonData(GameStateData prev, List<Integer> foodEaten, List<Integer> foodAdded,
            List<Integer> capsuleEaten, Boolean lose, Boolean win, List<Boolean> eaten, Integer scoreChange,
            Integer score) {
        if (!foodAdded.isEmpty())
            prev._foodEaten = new Position(foodEaten.get(0), foodEaten.get(1));

        if (!foodAdded.isEmpty())
            prev._foodAdded = new Tuple<Integer, Integer>(foodAdded.get(0), foodAdded.get(1));

        if (!capsuleEaten.isEmpty())
            prev._capsuleEaten = new Position(capsuleEaten.get(0), capsuleEaten.get(1));

        prev._lose = lose;
        prev._win = win;

        if (!eaten.isEmpty())
            prev._eaten = eaten;

        prev.scoreChange = scoreChange;
        prev.score = score;
        return prev;
    }

    /*
     * startConfigs, # ArrayList<ArrayList<String>>
     * configs, # ArrayList<ArrayList<String>>
     * isPacmans, # ArrayList<Boolean>
     * scaredTimers, # ArrayList<Integer>
     * numCarryings, # ArrayList<Integer>
     * numReturneds, # ArrayList<Integer>
     */
    public List<AgentState> agentStatesBuilder(List<List<String>> startConfigs, List<List<String>> configs,
            List<Boolean> isPacmans, List<Integer> scaredTimers, List<Integer> numCarryings,
            List<Integer> numReturneds) {
        List<AgentState> agentStates = new ArrayList<>();

        // startConfig builder
        for (int i = 0; i < startConfigs.size(); i++) {
            // each loop a new agentState is created and appended to the list
            List<String> currentStartConfig = startConfigs.get(i);
            List<String> currentConfig = configs.get(i);
            boolean isPacman = isPacmans.get(i);
            int scaredTimer = scaredTimers.get(i);
            int numCarrying = numCarryings.get(i);
            int numReturned = numReturneds.get(i);

            // startConfig
            /// pos
            double startConfigPosX = Double.parseDouble(currentStartConfig.get(0));
            double startConfigPosY = Double.parseDouble(currentStartConfig.get(1));
            Position startConfigPos = new Position(startConfigPosX, startConfigPosY);
            /// direction
            Direction startConfigDirection = Direction.fromString(currentStartConfig.get(2));
            Configuration startConfig = new Configuration(startConfigPos, startConfigDirection);

            // config
            /// pos
            double configPosX = Double.parseDouble(currentConfig.get(0));
            double configPosY = Double.parseDouble(currentConfig.get(1));
            Position configPos = new Position(configPosX, configPosY);
            /// direction
            Direction configDirection = Direction.fromString(currentConfig.get(2));
            Configuration config = new Configuration(configPos, configDirection);

            AgentState agentState = new AgentState(startConfig, config, isPacman, scaredTimer, numCarrying,
                    numReturned);
            agentStates.add(agentState);
        }
        return agentStates;
    }

    public void nothing() {
        System.out.println("[java] Converter class loaded");
    }
}
