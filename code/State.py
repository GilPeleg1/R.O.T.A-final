import numpy as np
import torch
from Graphics import *
from copy import deepcopy

class State:
    def __init__(self, board= None, player = 1,env = None) -> None:
        self.board = board
        self.player = player
        self.action : tuple[int, int] = None
        # self.legal_actions = legal_actions


    def get_opponent (self):
        if self.player == 1:
            return -1
        else:
            return 1

    def switch_player(self):
        if self.player == 1:
            self.player = -1
        else:
            self.player = 1

    def score (self, player = 1) -> tuple[int, int]:
        if player == 1:
            opponent = -1
        else:
            opponent = 1

        player_score = np.count_nonzero(self.board == player)
        opponent_score = np.count_nonzero(self.board == opponent)
        return player_score, opponent_score

    def __eq__(self, other) ->bool:
        #b1 = np.equal(self.board, ).all()
        #b2 = self.player == other.player
        return np.equal(self.board, other.board).all() and self.player == other.player

    def __hash__(self) -> int:
        return hash(repr(self.board) + repr(self.player))
    
    def copy (self):
        newBoard = np.copy(self.board)
        state = State(board=newBoard, player=self.player)
        # state.legal_actions = deepcopy(self.legal_actions)
        # print("copied =", state.legal_actions)
        return state
    
    def reverse (self):
        reversed = self.copy()
        reversed.board = reversed.board * -1
        reversed.player = reversed.player * -1
        return reversed

    def toTensor (self, device = torch.device('cpu')) -> tuple:
        board_np = self.board.reshape(-1)
        board_tensor = torch.tensor(board_np, dtype=torch.float32, device=device)
        # actions_np = np.array(self.legal_actions)
        # print(actions_np)
        # actions_tensor = torch.from_numpy(actions_np)
        return board_tensor
    
    [staticmethod]
    def tensorToState (state_tensor, player):
        board = state_tensor.reshape([3,3]).cpu().numpy()
        return State(board, player=player)
    