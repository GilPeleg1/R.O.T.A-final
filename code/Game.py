import pygame
from Graphics import *
from Rota import Rota
from Human_Agent import Human_Agent
from Random_Agent import Random_Agent
from MinMaxAgent import MinMaxAgent
from DQN_Agent import DQN_Agent
from AlphaBetaAgent import AlphaBetaAgent 
import time

FPS = 60
pygame_icon = pygame.image.load('shield.png')
pygame.display.set_icon(pygame_icon)
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Roman tic tac toe')
environment = Rota()
graphics = Graphics(win, board = environment.state.board)

#Human Agent
#player1 = Human_Agent(player=1)
#player2 = Human_Agent(player=-1)

#Random Agent
#player1 = Random_Agent(player=1,env=environment)
#player2 = Random_Agent(player=-1,env=environment)

#MinMax Agent
#player2 = MinMaxAgent(player = -1,depth = 3, environment=environment)
player1 = MinMaxAgent(player = 1,depth = 3, environment=environment)

#Alpha Beta Agent
#player1 = AlphaBetaAgent(player = 1,depth = 3, environment=environment)
#player2 = AlphaBetaAgent(player = -1,depth = 3, environment=environment)

#DQN White Agent
#player1 = DQN_Agent(player=1,env = environment, parametes_path ="Data\\params_1.pth") #against random
#player1 = DQN_Agent(player=1,env = environment, parametes_path ="Data\\params_2.pth") #against minmax

#DQN Black Agent
#player2 = DQN_Agent(player=-1,env = environment, parametes_path ="Data\\Black\\params_vs_random_v2.pth", train=False) #black against random
player2 = DQN_Agent(player=-1,env = environment, parametes_path ="Data\\Black\\params_vs_MinMax.pth", train=False) #black against minmax depth 3

#DQN BlackWhite
#player1 = DQN_Agent(player=1,env = environment, parametes_path ="Data\\params_11.pth")
#player2 = DQN_Agent(player=-1,env = environment, parametes_path ="Data\\params_11.pth")

def main(p1,p2):
    pygame.mixer.music.load('bmusic.mp3')
    pygame.mixer.music.play()
    environment.resetboard()
    player1 = p1
    player2 = p2
    start = time.time()
    run = True
    clock = pygame.time.Clock()
    graphics.draw()
    time.sleep(0.7)
    player = player1
    action = None
    exp = False
    while(run):
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               run = False
            if event.type == pygame.K_ESCAPE and exp:
                exp = False
                pygame.event.clear()          


        if action and action[1] == "tomove":
            graphics.human_moves(environment.human_moves(action[0],environment.state))
            pygame.display.update()
            action= (action[0],player.get_Move_Action(event, graphics, environment.state))    
        else:
            action = player.get_Action(event = event,graphics= graphics, state = environment.state, train = False)

#        if action and len(action)>1 and action[1] == "tomove":
#            print("continued")
#            continue
        if action and len(action)>1 and action[1]!="tomove":
            #print(action,"action","    player=",player.player)
            if (environment.move(action, environment.state)):
                #graphics.blink(action, GREEN)
                player = switchPlayers(player)
                time.sleep(0.15)
                
            else: 
                a = 1 # to not make an error
                #graphics.blink(action, RED)
                
        elif action:
            blue = (0, 0, 255)
            temp = (action[0],action[0])
            pygame.display.update()
            #graphics.blink(temp,blue)

        #display functions, check if end of game.    
        graphics.draw()
        pygame.display.update()
        #time.sleep(0.2)
        if environment.is_end_of_game(environment.state)[0]:
            run = False
    
    print ("end of game!")
    time.sleep(1.5)
    #pygame.quit()
    score1, score2 = environment.state.score()
    pygame.mixer.music.stop()
    pygame.mixer.music.load('wmusic.mp3')
    pygame.mixer.music.play(1)
    return(environment.state.board[1,1],True)


def switchPlayers(player):
    if player == player1:
       return player2
    else:
        return player1


    
def GUI ():

    global player1, player2
    player1 = Human_Agent(player=1)
    player2 = Human_Agent(player=-1)
    # player1 = MinMaxAgent(player = 1,depth = 3, environment=environment)
    # player2 = MinMaxAgent(player = 2,depth = 3, environment=environment)
    # player1 = MinMaxAgent2(player = 1,depth = 3, environment=environment)
    # player2 = MinMaxAgent2(player = 2,depth = 3, environment=environment)
    # player1 = AlphaBetaAgent(player = 1,depth = 3, environment=environment)
    # player2 = AlphaBetaAgent(player = 2,depth = 3, environment=environment)
    # player1 = RandomAgent(environment)
    # player2 = RandomAgent(environment)
    # player1 = FixAgent(environment, player=1)
    # player2 = FixAgent(environment, player=2, train=True)
    # player1 = FixAgent2(environment, player=1, train=True)
    # player2 = FixAgent2(environment, player=2)

    # model = DQN(environment)
    # model = torch.load(file)
    # player1 = DQNAgent(model, player=1, train=False)
    # player2 = DQNAgent(model, player=2, train=False)

    colors = [['blue', 'gray', 'gray', 'gray'], ['blue', 'gray', 'gray', 'gray']]
    player1_chosen = 0
    player2_chosen = 0
    clock = pygame.time.Clock()
    run = True
    whowon = 1
    ifwon = False
    while(run):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                #play select
                if 300<pos[0]<500 and 570<pos[1]<610:
                    if ifwon:
                        ifwon =False
                    else:
                        if type(player2) == DQN_Agent:
                            if type(player1) == Random_Agent:
                                player2 = DQN_Agent(player=-1,env = environment, parametes_path ="Data\\Black\\params_vs_random_v2.pth", train=False)
                                #print("DQN B VS R W")
                            else:
                                player2 = DQN_Agent(player=-1,env = environment, parametes_path ="Data\\Black\\params_vs_MinMax.pth", train=False)

                        if type(player1) == DQN_Agent:
                            if type(player2) == Random_Agent:
                                player1 = DQN_Agent(player=1,env = environment, parametes_path ="Data\\params_1.pth")
                                #print("DQN W VS R B")
                            else:
                                player1 = DQN_Agent(player=1,env = environment, parametes_path ="Data\\params_2.pth")
                        whowon,ifwon= main(player1, player2)
                        
                #Human agent select        
                if 100<pos[0]<300 and 200<pos[1]<240:
                    player1 = Human_Agent(player=1)
                    player1_chosen=0
                if 500<pos[0]<800 and 200<pos[1]<240:
                    player2 = Human_Agent(player=-1)
                    player2_chosen=0

                #minmax agent select
                if 100<pos[0]<300 and 250<pos[1]<290:
                    player1 = MinMaxAgent(player = 1,depth = 3, environment=environment)
                    player1_chosen=1
                if 500<pos[0]<800 and 250<pos[1]<290:
                    player2 = MinMaxAgent(player = -1,depth = 3, environment=environment)
                    player2_chosen=1

                #alphabeta agent select
                if 100<pos[0]<300 and 300<pos[1]<340:
                    player1 = AlphaBetaAgent(player = 1,depth = 3, environment=environment)
                    player1_chosen=2
                if 500<pos[0]<800 and 300<pos[1]<340:
                    player2 = AlphaBetaAgent(player = -1,depth = 3, environment=environment)
                    player2_chosen=2
                
                #DQN agent select
                if 100<pos[0]<300 and 350<pos[1]<390:
                    player1 = DQN_Agent(player = 1, env=environment)
                    player1_chosen=3
                if 500<pos[0]<800 and 350<pos[1]<390:
                    player2 = DQN_Agent(player = -1, env=environment)
                    player2_chosen=3

                #Random agent select
                if 100<pos[0]<300 and 400<pos[1]<440:
                    player1 = Random_Agent(player = 1, env=environment)
                    player1_chosen=4
                if 500<pos[0]<800 and 400<pos[1]<440:
                    player2 = Random_Agent(player = -1, env=environment)
                    player2_chosen=4
            
                    

        colors = [['gray', 'gray', 'gray', 'gray', 'gray'], ['gray', 'gray', 'gray', 'gray', 'gray']]
        colors[0][player1_chosen]='BLUE'
        colors[1][player2_chosen]='BLUE'


        backgroundimage = pygame.image.load('background.jpg')
        backgroundimage = pygame.transform.scale(backgroundimage, (HEIGHT,WIDTH))
        win.blit(backgroundimage,(0,0))

        if ifwon:
            #win.fill('LightGray')
            graphics.write(win, "Roman tic tac toe", pos=(260, 50), color=BLACK, background_color=None)   
            if whowon == -1:
                pygame.draw.rect(win, 'gray', (255,200,290,40))
                graphics.write(win, 'Red player Won!', (265,200),color=RED)
            else:
                pygame.draw.rect(win, 'gray', (255,200,290,40))
                graphics.write(win, 'Blue player Won!', (260,200),color=BLUE)

            pygame.draw.rect(win, 'gray', (300,570,200,40))
            graphics.write(win, 'continue', (335,570),color=BLACK) 

            graphics.draw_piece((1,1),whowon)
            
        else:
            #win.fill('LightGray')
            graphics.write(win, "Roman tic tac toe", pos=(260, 50), color=BLACK, background_color=None)  

            graphics.write(win, 'Player 1',(150,150),color=BLACK)
            pygame.draw.rect(win, colors[0][0], (100,200,200,40))
            graphics.write(win, 'Human', (120,200),color=BLACK)
            pygame.draw.rect(win, colors[0][1], (100,250,200,40))
            graphics.write(win, 'MinMax', (120,250),color=BLACK)
            pygame.draw.rect(win, colors[0][2], (100,300,200,40))
            graphics.write(win, 'Alpha_Beta', (120,300),color=BLACK)
            pygame.draw.rect(win, colors[0][3], (100,350,200,40))
            graphics.write(win, 'DQN', (120,350),color=BLACK)
            pygame.draw.rect(win, colors[0][4], (100,400,200,40))
            graphics.write(win, 'Random', (120,400),color=BLACK)

            graphics.write(win, 'Player 2',(550,150),color=BLACK)
            pygame.draw.rect(win, colors[1][0], (500,200,200,40))
            graphics.write(win, 'Human', (520,200),color=BLACK)
            pygame.draw.rect(win, colors[1][1], (500,250,200,40))
            graphics.write(win, 'MinMax', (520,250),color=BLACK)
            pygame.draw.rect(win, colors[1][2], (500,300,200,40))
            graphics.write(win, 'Alpha_Beta', (520,300),color=BLACK)
            pygame.draw.rect(win, colors[1][3], (500,350,200,40))
            graphics.write(win, 'DQN', (520,350),color=BLACK)
            pygame.draw.rect(win, colors[1][4], (500,400,200,40))
            graphics.write(win, 'Random', (520,400),color=BLACK)

            
            pygame.draw.rect(win, 'gray', (300,570,200,40))
            graphics.write(win, 'Play', (360,570),color=BLACK)


        pygame.display.update()

    pygame.quit()



if __name__ == '__main__':
    GUI()



