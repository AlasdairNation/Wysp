import jpype
from javaPacman import GameState


class JavaConverter:
    def __init__(self, problem):
        self.problem = problem
        # to construct PositionSearchProblem we need GameState, Position (goal), Position (start)
        # goal and start are tuples (float_x, float_y), can easily be built
        # GameState is constructed from GameStateData(prevState)
        # this file attempts to break down the original Python GameStateData object into its components
        # and reconstructed in GameStateData.java special constructor

    def convert_layout(self):
        l = self.problem.gameState.data.layout.layoutText
        textArray = jpype.java.util.ArrayList()

        for row in l:
            textArray.add(row)
        return textArray

    def convert_food(self):
        food = self.problem.gameState.data.food.data
        # returns a 2d arrayList of bools
        food2d = jpype.java.util.ArrayList()

        for f in food:
            row = jpype.java.util.ArrayList()
            for x in f:
                row.add(jpype.JBoolean(x))
            food2d.add(row)

        return food2d

    def convert_capsules(self):
        capsules = self.problem.gameState.data.capsules
        capsules2d = jpype.java.util.ArrayList()

        for c in capsules:
            pos = jpype.java.util.ArrayList()
            pos.add(c[0])
            pos.add(c[1])
            capsules2d.add(pos)

        return capsules2d

    def convert_score(self):
        return jpype.JInt(self.problem.gameState.data.score)

    def convert_eaten_(self):
        e = self.problem.gameState.data._eaten
        arr = jpype.java.util.ArrayList()
        for x in e:
            arr.add(x)
        return arr

    def convert_agentStates(self):
        # agentStates is a list of AgentState objects
        # each AgentState object has:
        # - startConfig (2d array of strings length 3. 0 & 1 will be pos x and y, 2 will be direction)
        # - - pos
        # - - - int1
        # - - - int2
        # - - direction
        # - - - str (N, S, E, W, X (Stop))

        # - config (array of strings length 3. 0 & 1 will be pos x and y, 2 will be direction)
        # - - pos
        # - - - int1
        # - - - int2
        # - - direction
        # - - - str (N, S, E, W, X (Stop))

        # - isPacman
        # - scaredTimer
        # - numCarrying
        # - numReturned
        states = self.problem.gameState.data.agentStates
        dir_dict = {
            "North": "N",
            "South": "S",
            "East": "E",
            "West": "W",
            "Stop": "X",
        }

        startConfigs = jpype.java.util.ArrayList()
        configs = jpype.java.util.ArrayList()
        isPacmans = jpype.java.util.ArrayList()
        scaredTimers = jpype.java.util.ArrayList()
        numCarryings = jpype.java.util.ArrayList()
        numReturneds = jpype.java.util.ArrayList()

        for state in states:
            # startConfig
            startConfg = jpype.java.util.ArrayList()
            startConfg.add(str(state.start.pos[0]))
            startConfg.add(str(state.start.pos[1]))
            startConfg.add(dir_dict[state.start.direction])
            startConfigs.add(startConfg)

            # config
            config = jpype.java.util.ArrayList()
            config.add(str(state.configuration.pos[0]))
            config.add(str(state.configuration.pos[1]))
            config.add(dir_dict[state.start.direction])
            configs.add(config)

            # all the rest
            isPacmans.add(jpype.JBoolean(state.isPacman))
            scaredTimers.add(jpype.JInt(state.scaredTimer))
            numCarryings.add(jpype.JInt(state.numCarrying))
            numReturneds.add(jpype.JInt(state.numReturned))

        return (
            startConfigs,  # ArrayList<ArrayList<String>>
            configs,  # ArrayList<ArrayList<String>>
            isPacmans,  # ArrayList<Boolean>
            scaredTimers,  # ArrayList<Integer>
            numCarryings,  # ArrayList<Integer>
            numReturneds,  # ArrayList<Integer>
        )

    def convert_rest(self):
        # List<Integer> foodEaten
        foodEaten = jpype.java.util.ArrayList()
        if self.problem.gameState.data._foodEaten is not None:
            for x in self.problem.gameState.data._foodEaten:
                foodEaten.add(x)

        # List<Integer> foodAdded
        foodAdded = jpype.java.util.ArrayList()
        if self.problem.gameState.data._foodAdded is not None:
            for x in self.problem.gameState.data._foodAdded:
                foodAdded.add(x)

        # List<Integer> capsuleEaten
        capsuleEaten = jpype.java.util.ArrayList()
        if self.problem.gameState.data._capsuleEaten is not None:
            for x in self.problem.gameState.data._capsuleEaten:
                capsuleEaten.add(x)

        # Boolean lose & win
        lose = jpype.JBoolean(self.problem.gameState.data._lose)
        win = jpype.JBoolean(self.problem.gameState.data._win)

        # List<Boolean> eaten
        eaten = jpype.java.util.ArrayList()
        if self.problem.gameState.data._eaten is not None:
            for x in self.problem.gameState.data._eaten:
                eaten.add(x)

        # Integer scoreChange
        scoreChange = jpype.JInt(self.problem.gameState.data.scoreChange)

        # Integer score
        score = jpype.JInt(self.problem.gameState.data.score)

        return (
            foodEaten,  # ArrayList<Integer>
            foodAdded,  # ArrayList<Integer>
            capsuleEaten,  # ArrayList<Integer>
            lose,  # Boolean
            win,  # Boolean
            eaten,  # ArrayList<Boolean>
            scoreChange,  # Integer
            score,  # Integer
        )

    def get_game_state(self):
        layout = self.convert_layout()
        food = self.convert_food()
        capsules = self.convert_capsules()
        score = self.convert_score()
        startConfigs, configs, isPacmans, scaredTimers, numCarryings, numReturneds = (
            self.convert_agentStates()
        )

        jConverter = jpype.JClass("capstone.prototype.utils.Converter")()

        # agent states builder
        jAgentStates = jConverter.agentStatesBuilder(
            startConfigs, configs, isPacmans, scaredTimers, numCarryings, numReturneds
        )

        # Create a new game state data object
        jGameStateData = jConverter.fromPythonData(
            layout.get(0).length(),
            layout.size(),
            layout,
            food,
            capsules,
            jAgentStates,
        )

        foodEaten, foodAdded, capsuleEaten, lose, win, eaten, scoreChange, score = (
            self.convert_rest()
        )

        # Convert the rest of the data
        jGameStateData = jConverter.otherPythonData(
            jGameStateData,
            foodEaten,
            foodAdded,
            capsuleEaten,
            lose,
            win,
            eaten,
            scoreChange,
            score,
        )

        # GameState
        jGameState = jpype.JClass("capstone.prototype.game.GameState")(jGameStateData)

        return jGameState

    @staticmethod
    def py_gamestate_to_java(state: GameState):
        data = state.data

        # layout
        layout = jpype.java.util.ArrayList()
        for row in data.layout.layoutText:
            layout.add(row)

        # food
        food = jpype.java.util.ArrayList()
        for f in data.food.data:
            row = jpype.java.util.ArrayList()
            for x in f:
                row.add(jpype.JBoolean(x))
            food.add(row)

        # capsules
        capsules = jpype.java.util.ArrayList()
        for c in data.capsules:
            pos = jpype.java.util.ArrayList()
            pos.add(c[0])
            pos.add(c[1])
            capsules.add(pos)

        # score
        score = jpype.JInt(data.score)

        # agentStates
        startConfigs = jpype.java.util.ArrayList()
        configs = jpype.java.util.ArrayList()
        isPacmans = jpype.java.util.ArrayList()
        scaredTimers = jpype.java.util.ArrayList()
        numCarryings = jpype.java.util.ArrayList()
        numReturneds = jpype.java.util.ArrayList()

        for state in data.agentStates:
            # startConfig
            startConfg = jpype.java.util.ArrayList()
            startConfg.add(str(state.start.pos[0]))
            startConfg.add(str(state.start.pos[1]))
            startConfg.add(state.start.direction)
            startConfigs.add(startConfg)

            # config
            config = jpype.java.util.ArrayList()
            config.add(str(state.configuration.pos[0]))
            config.add(str(state.configuration.pos[1]))
            config.add(state.start.direction)
            configs.add(config)

            # all the rest
            isPacmans.add(jpype.JBoolean(state.isPacman))
            scaredTimers.add(jpype.JInt(state.scaredTimer))
            numCarryings.add(jpype.JInt(state.numCarrying))
            numReturneds.add(jpype.JInt(state.numReturned))

        jConverter = jpype.JClass("capstone.prototype.utils.Converter")()

        # agent states builder
        jAgentStates = jConverter.agentStatesBuilder(
            startConfigs, configs, isPacmans, scaredTimers, numCarryings, numReturneds
        )

        # Create a new game state data object
        jGameStateData = jConverter.fromPythonData(
            layout.get(0).length(),
            layout.size(),
            layout,
            food,
            capsules,
            jAgentStates,
        )

        # convert rest - foodEaten, foodAdded, capsuleEaten, lose, win, eaten, scoreChange, score
        # List<Integer> foodEaten
        foodEaten = jpype.java.util.ArrayList()
        if data._foodEaten is not None:
            for x in data._foodEaten:
                foodEaten.add(x)

        # List<Integer> foodAdded
        foodAdded = jpype.java.util.ArrayList()
        if data._foodAdded is not None:
            for x in data._foodAdded:
                foodAdded.add(x)

        # List<Integer> capsuleEaten
        capsuleEaten = jpype.java.util.ArrayList()
        if data._capsuleEaten is not None:
            for x in data._capsuleEaten:
                capsuleEaten.add(x)

        # Boolean lose & win
        lose = jpype.JBoolean(data._lose)
        win = jpype.JBoolean(data._win)

        # List<Boolean> eaten
        eaten = jpype.java.util.ArrayList()
        if data._eaten is not None:
            for x in data._eaten:
                eaten.add(x)

        # Integer scoreChange
        scoreChange = jpype.JInt(data.scoreChange)
        
        # Integer score
        score = jpype.JInt(data.score)

        # Convert the rest of the data
        jGameStateData = jConverter.otherPythonData(
            jGameStateData,
            foodEaten,
            foodAdded,
            capsuleEaten,
            lose,
            win,
            eaten,
            scoreChange,
            score,
        )

        # GameState
        jGameState = jpype.JClass("capstone.prototype.game.GameState")(jGameStateData)

        return jGameState

    def position_search_problem(self):
        jGameState = self.get_game_state()

        # goal
        goal = jpype.JClass("capstone.prototype.types.Position")(
            jpype.JInt(self.problem.goal[0]), jpype.JInt(self.problem.goal[1])
        )

        # start
        startState = jpype.JClass("capstone.prototype.types.Position")(
            jpype.JInt(self.problem.startState[0]),
            jpype.JInt(self.problem.startState[1]),
        )

        # PositionSearchProblem
        jPositionSearchProblem = jpype.JClass(
            "capstone.prototype.problem.PositionSearchProblem"
        )(jGameState, goal, startState)
        return jPositionSearchProblem

    def corners_problem(self):
        jGameState = self.get_game_state()
        jCornersProblem = jpype.JClass("capstone.prototype.problem.CornersProblem")(
            jGameState
        )
        return jCornersProblem

    def food_search_problem(self):
        jGameState = self.get_game_state()
        jFoodSearchProblem = jpype.JClass(
            "capstone.prototype.problem.FoodSearchProblem"
        )(jGameState)
        return jFoodSearchProblem
