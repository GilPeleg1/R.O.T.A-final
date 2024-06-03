import numpy as np
from State import State
from Graphics import *

class Rota:
    def __init__(self, state:State = None) -> None:
        if state == None:
            self.state = self.get_init_state()
            # self.state.legal_actions = self.get_all_legal_actions(self.state)
        else:
            self.state = state

    def get_init_state(self,):
        rows, cols = (ROWS,COLS)
        board = np.zeros([rows, cols],int)
        #board[0,1] = 1
        #board[0,2] = 2
        return State (board = board, player = 1)

    def is_free(self, row_col: tuple[int, int], state: State):
        row, col = row_col
        return state.board[row, col] != 0

    def is_inside(self, row_col, state: State):
        row, col = row_col
        board_row, board_col = state.board.shape
        return 0 <= row < board_row and 0 <= col < board_col

    def flip_piece(self, row_col, state: State):
        row, col = row_col
        if state.board[row][col] == 1:
            state.board[row][col] = -1
        else:
            state.board[row][col] = 1

    def check_legal_line(self, start_row_col: tuple[int, int], dir_row_col: tuple[int, int], state: State):
        count = 0
        opponent = state.get_opponent()
        row, col = start_row_col
        dir_row, dir_col = dir_row_col
        go = True
        while (go):
            row += dir_row
            col += dir_col
            if self.is_inside((row, col), state) and state.board[row, col] == opponent:
                count +=1
            else:
                go = False

        if self.is_inside((row, col), state) and state.board[row, col] == state.player and count > 0:
            return count
        
        return -1

    def move(self, action, state: State):
        if action == None:
            return False
        row, col = action[1]
        if state.board[action[1]] != 0 or(state.board[action[0]] == state.get_opponent):
            #print("terminate 111"),
            #print("turn",state.player)
            #print("ontile=",state.board[action[0]])
            #print("action",action)
            #print("board=",state.board)
            return False
            
        legal = self.is_legal_action(action, state)
#        for dir_row in directions:
#            for dir_col in directions:
#                if dir_row == dir_col == 0:
#                    continue
#                count = self.check_legal_line((row, col), (dir_row, dir_col), state)
#                if  count > 0:
#                    legal = True
#                    self.reverse_line((row, col), (dir_row, dir_col), count, state)
        if legal:
                #print("from:",action[0],"to:",action[1],"player:",state.player)
                state.board[action[0]] = 0
                state.board[row, col] = state.player
                state.switch_player()
                state.action = action[1]   
        return legal

    def is_legal_action(self, action, state: State):
        row, col = action[1]
        if state.board[row][col] !=0:
            #print("terminate 2")
            return False
        if action[0] == action[1] and state.board[action[0]] == 0:
            team = state.player
            unitcounter = 0
            #סופרים כמה כלים יש לך על הלוח
            for row1 in range(ROWS):
                for col1 in range(COLS):
                        if state.board[row1,col1] == team:
                            unitcounter = unitcounter + 1
            if unitcounter < 3:            
                return True
            else:
                return False
        legal_moves = self.all_legal_moves(action[0], state)
        #print("legal_moves=",legal_moves)
        #print("shape=",np.array(legal_moves).shape)
        if legal_moves != [] and len(np.array(legal_moves).shape) > 1:
            for i in legal_moves:
                if list(action[1]) == i:
                    return True
        elif legal_moves != [] and len(np.array(legal_moves).shape) == 1:
            if list(action[1])==legal_moves:
                return True
        #print("legal_moves=",legal_moves)
        #print("move to=", list(action[1]))
        #print("terminate 3")
        return False

    def all_legal_moves(self,row_col, state: State):
        row, col = row_col
        board = state.board
        if board[row, col] == 0:
            return [row,col]
        moves = []
        if board[1,1] == 0:
            moves.append([1,1])
        #אם הכלי לא באמצע
        if not(row == col == 1):
            for row1 in range(ROWS):
                for col1 in range(COLS):
                    if (abs(row-row1) == 1 and col-col1 == 0) or (abs(col-col1) == 1 and row-row1 == 0):
                        if board[row1,col1] == 0 and state.player == board[row,col]:
                            moves.append([row1,col1])
        else:
        #אם הכלי באמצע
            #print("working")
            for row1 in range(ROWS):
                for col1 in range(COLS):
                    if board[row1,col1] == 0 and state.player == board[row,col]:
                        moves.append([row1,col1])
        return moves

    def is_legal_move(self, row_col, state: State):
        row, col = row_col
        if state.board[row][col] !=0:
            return False
        directions = (-1 , 0 , 1)
        for dir_row in directions:
            for dir_col in directions:
                if dir_row == dir_col == 0:
                    continue
                count = self.check_legal_line((row, col), (dir_row, dir_col), state)
                if  count > 0:
                    return True
        return False
   
    def get_legal_actions(self, state: State):
        legal_action = []
        rows, cols = state.board.shape
        for row in range(rows):
            for col in range(cols):
                if self.is_legal_move((row,col), state):
                    legal_action.append((row, col))
        return legal_action

    def get_all_legal_actions(self, state: State):
        legal_action = []
        rows, cols = state.board.shape
        teamcounter = 0
        for row in range(ROWS):
            for col in range(COLS):
                if state.player == state.board[row,col]:
                    all_moves = self.all_legal_moves((row,col), state)
                    if len(all_moves)>0:
                        for i in all_moves:
                            if state.board[tuple(i)] == 0:
                                legal_action.append(((row,col),tuple(i)))

        for row in range(ROWS):
            for col in range(COLS):        
                if state.player == state.board[row,col]:
                    teamcounter = teamcounter + 1
        
        if teamcounter < 3:
            for row in range(ROWS):
                for col in range(COLS):
                    if state.board[row,col] == 0:
                        legal_action.append(tuple([(row,col),(row,col)]))
        return legal_action

    def is_end_of_game(self, state: State):
        board = state.board
        if (board[0,0] == board[1,1] == board[2,2]) and board[0,0] != 0:
                return (True,board[1,1])
        elif (board[2,0] == board[1,1] == board[0,2]) and board[2,0] != 0:
                return (True,board[1,1])
        elif (board[1,0] == board[1,1] == board[1,2]) and board[1,0] != 0:
                return (True,board[1,1])
        elif (board[0,1] == board[1,1] == board[2,1]) and board[2,1] != 0:
                return (True,board[1,1])
        return (False,0)
    def get_next_state(self, action, state:State):
        next_state = state.copy()
        self.move(action, next_state)
        next_state.switch_player
        return next_state
    
#    def GLOBAL_get_all_legal_actions(self, state: State):
        legal_action = []
        rows, cols = state.board.shape
        teamcounter = 0
        for row in range(ROWS):
            for col in range(COLS):
                if state.player == state.board[row,col]:
                        all_moves = self.all_legal_moves((row,col), state)
                if len(all_moves)>0:
                        for i in all_moves:
                            if state.board[all_moves[i]] == 0:
                                legal_action.append(((row,col),tuple(i)))

        for row in range(ROWS):
            for col in range(COLS):        
                if state.player == state.board[row,col]:
                    teamcounter = teamcounter + 1
            
        if teamcounter < 3:
            for row in range(ROWS):
                for col in range(COLS):
                    if state.board[row,col] == 0:
                        legal_action.append(tuple([(row,col),(row,col)]))
        return legal_action
    
    def reward (self, state : State, action = None) -> tuple:
        if action:
            next_state = self.get_next_state(action, state)
        else:
            next_state = state
        if (self.is_end_of_game(next_state)[0]):
            if next_state.board[1,1] == 1:
                return 1,True
            else:
                return -1,True
        #    sum =  next_state.board.sum()
        #    if sum > 0:
        #        return 1, True  
        #    elif sum < 0:
        #        return -1, True  
        #    else:
        #        return 0, True  
        return 0, False
    def resetboard(self):

        self.state.board[0,0] = 0
        self.state.board[0,1] = 0
        self.state.board[0,2] = 0
        self.state.board[1,0] = 0
        self.state.board[1,1] = 0
        self.state.board[1,2] = 0
        self.state.board[2,0] = 0
        self.state.board[2,1] = 0
        self.state.board[2,2] = 0
        self.state.player = 1

    def human_moves(self,action,state):
        legal_actions = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.is_legal_action((action,(row,col)),state):
                    legal_actions.append((row,col))
        return legal_actions
