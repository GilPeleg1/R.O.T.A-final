import numpy as np
import pygame
import time

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 3, 3
SQUARE_SIZE = WIDTH//COLS
LINE_WIDTH = 2
PADDING = SQUARE_SIZE //5


#RGB
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHTGRAY = (211,211,211)
GREEN = (0, 128, 0)
TESTCOLOR = (201, 199, 155)


pygame.init()

class Graphics:
    def __init__(self, win, board):
        self.board = board
        rows, cols = board.shape
        self.win = win
        self.rows = rows
        self.cols = cols

    def draw_Lines(self):


        for i in range(ROWS):
            pygame.draw.line(self.win, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE , WIDTH), width=LINE_WIDTH)
            pygame.draw.line(self.win, BLACK, (0, i * SQUARE_SIZE), (HEIGHT, i * SQUARE_SIZE ), width=LINE_WIDTH)

    def draw_all_pieces(self):

        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] !=0 :
                    self.draw_piece((row, col), self.board[row][col])
            
    def draw_piece(self, row_col, player):

                # Load image
        imageteam1 = pygame.image.load('shield.png')
        imageteam2 = pygame.image.load('shield.png')
        # Set the size for the image
        DEFAULT_IMAGE_SIZE = (WIDTH/ROWS-80, HEIGHT/COLS-80)
        
        # Scale the image to your needed size
        imageteam1 = pygame.transform.scale(imageteam1, DEFAULT_IMAGE_SIZE)
        imageteam2 = pygame.transform.scale(imageteam2, DEFAULT_IMAGE_SIZE)
        center = self.calc_pos(row_col)

        pos = self.calc_image_pos(row_col)
        radius = (SQUARE_SIZE) // 1.5 - PADDING
        color = self.calc_color(player)
        #print("player=",player)
        pygame.draw.circle(self.win,color , center, radius)
        if player == 1:
            self.win.blit(imageteam1,pos)
        else:
            self.win.blit(imageteam2,pos)
        #pygame.draw.circle(self.win, BLUE, center, radius+2)
    def explaination(self):
                # Load image
        expan = pygame.image.load('explaination.png')
        # Set the size for the image
        DEFAULT_IMAGE_SIZE = (WIDTH, HEIGHT)
        
        # Scale the image to your needed size
        expan = pygame.transform.scale(expan, DEFAULT_IMAGE_SIZE)

        self.win.blit(expan,(0,0))

    def calc_pos(self, row_col):
        row, col = row_col
        y = row * SQUARE_SIZE + SQUARE_SIZE//2
        x = col * SQUARE_SIZE + SQUARE_SIZE//2
        return x, y

    def calc_image_pos(self, row_col):
        row, col = row_col
        y = row * SQUARE_SIZE+40
        x = col * SQUARE_SIZE+40
        return x, y

    def calc_base_pos(self, row_col):
        row, col = row_col
        y = row * SQUARE_SIZE
        x = col * SQUARE_SIZE
        return x, y

    def calc_row_col(self, pos):
        x, y = pos
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        return row, col

    def calc_color(self, player):
        if player == 1:
            return BLUE
        elif player == -1:
            return RED
        else:
            return LIGHTGRAY

    def draw(self):
        self.win.fill(TESTCOLOR)
        self.draw_Lines()
        self.draw_all_pieces()

    def draw_square(self, row_col, color):
        pos = self.calc_base_pos(row_col)
        pygame.draw.rect(self.win, color, (*pos, SQUARE_SIZE, SQUARE_SIZE))

    def blink(self, action, color):
        row, col = action[1]
        player = self.board[row][col]
        for i in range (2):
            self.draw_square((row, col), color)
            if player:
                self.draw_piece((row ,col), player) 
            pygame.display.update()
            time.sleep(0.2)
            self.draw_square((row, col), LIGHTGRAY)
            if player:
                self.draw_piece((row,col), player) 
            pygame.display.update()
            time.sleep(0.2)

    def write (self,surface, text, pos = (50, 20), color = BLACK, background_color = None):
        font = pygame.font.SysFont("rubikbold", 31)
        text_surface = font.render(text, True, color, background_color)
        surface.blit(text_surface, pos)

    def human_moves(self,actions):
        print(actions)
        for row in range(ROWS):
            for col in range(COLS):
                for i in actions:
                    if (row,col) == i:
                        self.draw_square((row, col), GREEN)
        self.draw_Lines()







