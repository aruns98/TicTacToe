from Board import Board
from Cell import Cell
from Agent import Agent
import random
import time


# Initializing board.
board=Board()

# Initializing agent.
agent1=Agent()
agent1.gamma=1
print('\nWelcome to Tic-Tac-Toe with reinforcement learning!\nAn agent has been created.\n')

# Starting game. Game loops till user chooses to exit.
game_flag=0
while game_flag==0:
    input_flag=0
    while input_flag==0:
        ip=input('Input 0 if you would like to train the agent.\nInput 1 if you would like to play against the agent.\nInput 2 if you would like to exit.\n\n')
        if ip=='0' or ip=='1' or ip=='2':
            ip=int(ip)
            input_flag=1
            continue
        else:
            continue

    # Training agent.
    if ip==0:
        print('You have chosen to train the agent!')
        agent1.winCount=0
        agent1.lossCount=0
        agent1.tieCount=0
        epsilon_flag=0
        # Requests exploration rate.
        while epsilon_flag==0:
            try:
                agent1.epsilon=float(input("Please choose the agent's exploration rate (0 to 1): "))
            except ValueError:
                continue
            if agent1.epsilon >=0 and agent1.epsilon <= 1:
                epsilon_flag=1
                continue
            else:
                continue
        
        iter_flag=0
        # Requests number of iterations.
        while iter_flag==0:
            try:
                agent1.iter=int(input('Please enter the number of games to be played for training: '))
                if agent1.iter >=1:
                    iter_flag=1
                    continue
                else:
                    continue
            except ValueError:
                continue
    
        opp_flag=0
        # Requests an opponent.
        while opp_flag==0:
            try:
                opp=int(input("Enter 0 to train against the Random Mover.\nEnter 1 to train against MiniMax.\nEnter 2 to train against the agent against itself\n"))
            except ValueError:
                continue
            if opp==0 or opp==1 or opp==2:
                opp_flag=1
                continue
            else:
                continue
        if opp==0:
            # Trains against the random mover.
            agent1.trainAgent(board,0)
        elif opp==1:
            # Trains against Minimax.
            agent1.trainAgent(board,1)
        elif opp==2:
            # Trains against itself.
            agent1.trainAgent(board,2)
        # Prints training statistics.
        print('\nHere are the statistics after ',agent1.iter,' games:')
        print('Wins: ',agent1.winCount)
        print('Losses: ',agent1.lossCount)
        print('Ties: ',agent1.tieCount)
        print('\nFor an exploration rate of ',agent1.epsilon,', the agent had a win rate of ',100*(agent1.winCount/agent1.iter),'%\n')

    # Playing against agent.
    if ip==1:
        # Exploration rate set to 0
        agent1.epsilon=0
        agent1.playAgent(board)

    # Exiting game.
    if ip==2:
        game_flag=1
        continue










