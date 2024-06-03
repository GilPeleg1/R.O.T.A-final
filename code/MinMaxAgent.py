from Rota import Rota
from State import State
MAXSCORE = 100000

class MinMaxAgent:

    def __init__(self, player, depth = 3, environment: Rota = None):
        self.player = player
        if self.player == 1:
            self.opponent = -1
        else:
            self.opponent = 1
        self.depth = depth
        self.environment : Rota = environment

    def evaluate (self, gameState : State):
        player_score, opponent_score = gameState.score(player = self.player)
        score =  player_score - opponent_score
        if self.environment.is_end_of_game(gameState)[0] and self.player == self.environment.is_end_of_game(gameState)[1]:
            score = 1000
        elif self.environment.is_end_of_game(gameState)[0] and self.opponent == self.environment.is_end_of_game(gameState)[1]:
            score = -1000

        #if gameState.board[1,1] == self.player:
        #    score = score+15
        for row in range(0, 2):
            for col in range (0, 2):
                if gameState.board[row][col] == self.player:
                    score += 5
                elif gameState.board[row][col] == self.opponent:
                    score -= 5
        

        return score

    def get_Action(self, event = None, graphics = None, state = 1, train = False):
        reached = set()
        gameState = state
        value, bestAction = self.minMax(gameState, reached, 0)
        return bestAction

    def minMax(self, gameState, reached:set, depth):
        if self.player == gameState.player:
            value = -MAXSCORE
        else:
            value = MAXSCORE

        # stop state
        if depth == self.depth or self.environment.is_end_of_game(gameState)[0]:
            value = self.evaluate(gameState)
            return value, None
        
        # start recursion
        bestAction = None
        legal_actions = self.environment.get_all_legal_actions(gameState)
        for action in legal_actions:
            newGameState = self.environment.get_next_state(action, gameState)
            if newGameState not in reached:
                reached.add(newGameState)
                if self.player == gameState.player:         # maxNode - agent
                    newValue, newAction = self.minMax(newGameState, reached,  depth + 1)
                    if newValue >= value:
                        value = newValue
                        bestAction = action
                else:                       # minNode - opponent
                    newValue, newAction = self.minMax(newGameState, reached,  depth + 1)
                    if newValue <= value:
                        value = newValue
                        bestAction = action

        return value, bestAction 

