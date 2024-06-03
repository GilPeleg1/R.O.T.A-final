import pygame
from Graphics import *
from Constant import *

class Human_Agent:

    def __init__(self, player: int) -> None:
        self.player = player

    def get_Action (self, event= None, graphics: Graphics = None, state = None, train = False):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pygame.event.clear()
            row_col = graphics.calc_row_col(pos)
            if state.board[row_col] == self.player and event.type == pygame.MOUSEBUTTONDOWN:
                    #print(row_col, "not skipped")
                    
                    #print("blue", "row_col=",row_col) 
                    return ((row_col),"tomove")
            #print("skipped")
            return ((row_col),(row_col))
        else:
            return None
        


    def get_Move_Action (self, event= None, graphics: Graphics = None, state = None):
        running = True
        liftfinger = False
        pygame.event.clear()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    liftfinger = True
                if event.type == pygame.MOUSEBUTTONDOWN and liftfinger:
                    pos = pygame.mouse.get_pos()
                    row_col = graphics.calc_row_col(pos)
                    return (row_col)
        a = 1