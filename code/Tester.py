from Random_Agent import Random_Agent
#from Fix_Agent import Fix_Agent
from Rota import Rota
from DQN_Agent import DQN_Agent
from MinMaxAgent import MinMaxAgent
from AlphaBetaAgent import AlphaBetaAgent

class Tester:
    def __init__(self, env, player1, player2) -> None:
        self.env = env
        self.player1 = player1
        self.player2 = player2
        

    def test (self, games_num):
        env = self.env
        player = self.player1
        player1_win = 0
        player2_win = 0
        games = 0
        while games < games_num:
            action = player.get_Action(state=env.state, train = False)
            env.move(action, env.state)
            player = self.switchPlayers(player)
            if env.is_end_of_game(env.state)[0]:
                score = env.state.score()[0]
                if env.is_end_of_game(env.state)[1] == 1:
                    player1_win += 1
                else:
                    player2_win += 1 
                env.state = env.get_init_state()
                games += 1
                player = self.player1
        return player1_win, player2_win        

    def switchPlayers(self, player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1

    def __call__(self, games_num):
        return self.test(games_num)

if __name__ == '__main__':
    env = Rota()
    #player1 = Random_Agent(env, player=1)
    player2 = AlphaBetaAgent(environment= env, depth= 3, player= -1)
    #test = Tester(env,player1, player2)
    #print(test.test(100))
    player1 = MinMaxAgent(player = 1,depth = 3, environment=env)
    #player1 = Random_Agent(player=1, env=env)
    #player1 = Random_Agent(player=1, env=env)
    #player2 = DQN_Agent(player=-1,env = env, parametes_path ="Data\\Black\\params_vs_random_v2.pth", train=False) #black against random
    #player2 = DQN_Agent(player=-1,env = env, parametes_path ="Data\\Black\\params_vs_MinMax.pth", train=False) #black against minmax
    #player1 = DQN_Agent(player=1,env = env, parametes_path ="Data\\params_1.pth") #against random
    #player1 = DQN_Agent(player=1,env = env, parametes_path ="Data\\params_11.pth") #against himself #minmax
    test = Tester(env,player1, player2)
    print(test.test(100))