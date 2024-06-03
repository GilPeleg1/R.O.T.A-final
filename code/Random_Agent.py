import pygame
from Rota import Rota
from State import State
import random
from Graphics import *

class Random_Agent:

    def __init__(self, player, env: Rota = None):
        self.player = player
        if self.player == 1:
            self.opponent = -1
        else:
            self.opponent = 1
        self.environment : Rota = env

    def get_Action (self, event= None, graphics: Graphics = None, state = None, train = False):
        temp = self.environment.get_all_legal_actions(state)
        length = len(temp)
        if length < 2:
            #print("temp=",temp)
            a= 1
        rnd = random.randrange(0,length)-1
        return temp[rnd]