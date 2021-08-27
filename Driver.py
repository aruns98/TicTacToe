from Board import Board
import time

def playGame(board):
    # Whoever is assigned 'X' is the first player. 
    # So if computerPeg is 'X', computer plays a random first move
    if(board.computerPeg=='X'):
        while(True):
            board.computerMove()
            time.sleep(1)   
            board.userMove()
            time.sleep(1)
    else:
        while(True):
            board.userMove()
            time.sleep(1)
            board.computerMove()
            time.sleep(1)

if __name__=='__main__':
    board = Board()
    print("Starting Game!!")
    # sleep for 1 second to slow down display
    time.sleep(1)
    board.printBoard()
    # Defining flag and while loop in order to prevent unsuitable inputs
    flag=0
    while flag==0:
        userInput = input("Play first? (Y/N):")
        if(userInput.upper() == 'Y'):
            # user plays first
            board.userPeg='X'
            board.computerPeg='0'
            flag=1
        elif(userInput.upper() == 'N'):
            # computer plays first
            board.computerPeg='X'
            board.userPeg='0'
            flag=1
        else:
            print("invalid input")
        
    playGame(board)
