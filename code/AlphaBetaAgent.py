from Rota import Rota
from State import State
MAXSCORE = 100000

class AlphaBetaAgent:

    def __init__(self, player, depth = 4, environment: Rota = None):
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


    def get_Action(self,state: State,event = None,graphics = None, train=False):
        visited = set()
        value, bestAction = self.minMax(state, visited)
        return bestAction

    def minMax(self, state:State, visited:set):
        depth = 0
        alpha = -MAXSCORE
        beta = MAXSCORE
        return self.max_value(state, visited, depth, alpha, beta)
        
    def max_value (self, state:State, visited:set, depth, alpha, beta):
        
        value = -MAXSCORE
        bestAction = None
        # stop state
        if depth == self.depth or self.environment.is_end_of_game(state)[0]:
            value = self.evaluate(state)
            return value, bestAction
        
        # start recursion
        
        legal_actions = self.environment.get_all_legal_actions(state)
        for action in legal_actions:
            newState = self.environment.get_next_state(action, state)
            if newState not in visited:
                visited.add(newState)
                newValue, newAction = self.min_value(newState, visited,  depth + 1, alpha, beta)
                if newValue > value:
                    value = newValue
                    bestAction = action
                    alpha = max(alpha, value)
                if value >= beta:
                    return value, bestAction
                    

        return value, bestAction 

    def min_value (self, state:State, visited:set, depth, alpha, beta):
        
        value = MAXSCORE
        bestAction = None
        # stop state
        if depth == self.depth or self.environment.is_end_of_game(state)[0]:
            value = self.evaluate(state)
            return value, bestAction
        
        # start recursion

        legal_actions = self.environment.get_all_legal_actions(state)
        for action in legal_actions:
            newState = self.environment.get_next_state(action, state)
            if newState not in visited:
                visited.add(newState)
                newValue, newAction = self.max_value(newState, visited,  depth + 1, alpha, beta)
                if newValue < value:
                    value = newValue
                    bestAction = action
                    beta = min(beta, value)
                if value <= alpha:
                    return value, bestAction

        return value, bestAction 

