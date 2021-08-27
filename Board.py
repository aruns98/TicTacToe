from Cell import Cell
from MinMax import MinMax
import random

class Board:
    def __init__(self):
        # 9 cells for the board
        self.cells = []
        self.isEmpty = True
        # set these values to 'X' and '0' at runtime
        self.computerPeg='#'
        self.userPeg='#'
        self.banner=""
        for i in range(9):
            self.cells.append(Cell(i))

    def printBoard(self):
        print('\n')
        print(self.banner)
        for i in range(9):
            print(self.cells[i].pegPlaced,end='\t')
            if(i%3==2):
                # print newline after every row
                print()
        print('\n')
        score = self.calcScore()
        if(score!=0):
            if score==0:
                print("It is a tie!")
            elif score==100:
                print("Player X has won!")
            elif score==-100:
                print("Player 0 has won!")
            exit(0)

    # Prints board without evaluating winner.
    def printBoard_noCheck(self):
        print('\n')
        print(self.banner)
        for i in range(9):
            print(self.cells[i].pegPlaced,end='\t')
            if(i%3==2):
                # print newline after every row
                print()
        print('\n')

    # User plays a move against the agent.
    def userVsAgent(self):
        self.banner="Your move"
        # Checking if user inputs a valid position
        flag=0
        posList=['0','1','2','3','4','5','6','7','8']
        vacCells=self.getVacantCells()
        while flag==0:
            position=(input("Enter position to place peg (0-8):"))
            if (position) not in posList:
                print('Please enter a valid position')
                continue
            position=int(position)
            if (self.cells[position]) not in vacCells:
                print('That cell is occupied!')
                continue
            self.cells[position].placePeg(self.computerPeg)
            self.isEmpty = False
            flag=1

    # Minimax plays a move against the agent.
    def minimaxVsAgent(self):
        self.banner="Computer's move"
        MinMax.count=0
        if(self.isEmpty):
            position = random.randint(0,8)
            self.cells[position].placePeg(self.computerPeg)
            self.isEmpty = False

        else:
            if(self.computerPeg=='X'):
                # Maximizer called with depth=0, alpha=-1000 and beta=1000
                listVal = MinMax.maximizer(self,0,-1000,+1000)
                pos = listVal[1]
            else:
                # Minimizer called with depth=0, alpha=-1000 and beta=1000
                listVal = MinMax.minimizer(self,0,-1000,+1000)
                pos = listVal[1]
            self.cells[pos].placePeg(self.computerPeg)

    # Used by the agent to check if the game is over. If it is, terminal updates are made.
    def agentBoardEval(self,agent):
        # Checks for winner.
        winner= self.calcScore()
        if winner==100:
            # X has won. Updates agent.
            if agent.pegDict['A']=='X':
                agent.winCount+=1
                agent.updateAgent(0, self, 100,1)
            else:
                agent.lossCount+=1
                agent.updateAgent(0, self, -100,1)
            # Agent will exit the game.
            agent.flag=1
        elif winner==-100:
            # 0 has won. Updates agent.
            if agent.pegDict['A']=='X':
                agent.lossCount+=1
                agent.updateAgent(0, self, -100,1)
            else:
                agent.winCount+=1
                agent.updateAgent(0, self, 100,1)
            # Agent will exit the game.
            agent.flag=1
        elif(len(self.getVacantCells())==0):
            if winner==0:
                # Game is a tie. Updates agent.
                agent.tieCount+=1
                agent.updateAgent(0, self,-10,1)
            # Agent will exit the game.
            agent.flag=1

    # Returns 1 if game is over. Otherwise returns 0.     
    def gameOver(self):
        winner=self.calcScore
        if winner==100 or winner== -100:
            return(1)
        elif (len(self.getVacantCells())==0):
            return(1)
        else:
            return(0)

    # place peg on random position if first move, else use minMax algo
    def computerMove(self):
        self.banner="Computer's move"
        MinMax.count=0
        if(self.isEmpty):
            position = random.randint(0,8)
            self.cells[position].placePeg(self.computerPeg)
            self.isEmpty = False
        elif(len(self.getVacantCells())==0):
            # board is full
            winner = self.calcScore()
            if winner==0:
                print("It is a tie!")
            elif winner==100:
                print("Player X has won!")
            elif winner==-100:
                print("Player 0 has won!")
            exit(0)
        else:
            if(self.computerPeg=='X'):
                # Maximizer called with depth=0, alpha=-1000 and beta=1000
                listVal = MinMax.maximizer(self,0,-1000,+1000)
                pos = listVal[1]
            else:
                # Minimizer called with depth=0, alpha=-1000 and beta=1000
                listVal = MinMax.minimizer(self,0,-1000,+1000)
                pos = listVal[1]
            self.cells[pos].placePeg(self.computerPeg)
        print('Number of iterations evaluated: ',MinMax.count)
        self.printBoard()

    def userMove(self):
        self.banner="Your move"
        if(len(self.getVacantCells())==0):
            # board is full
            winner = self.calcScore()
            if winner==0:
                print("It is a tie!")
            elif winner==100:
                print("Player X has won!")
            elif winner==-100:
                print("Player 0 has won!")
            exit(0)
        else:
            # Checking if user inputs a valid position
            flag=0
            posList=['0','1','2','3','4','5','6','7','8']
            vacCells=self.getVacantCells()
            while flag==0:
                position=(input("Enter position to place peg (0-8):"))
                if (position) not in posList:
                    print('Please enter a valid position')
                    continue
                position=int(position)
                if (self.cells[position]) not in vacCells:
                    print('That cell is occupied!')
                    continue
                self.cells[position].placePeg(self.userPeg)
                self.isEmpty = False
                flag=1
        self.printBoard()

    def getVacantCells(self):
        vacantCells = []
        for i in range(9):
            if(self.cells[i].pegPlaced=='#'):
                vacantCells.append(self.cells[i])
        return vacantCells

    def checkDiagonals(self):
        leftDiagonalPositions = [0,4,8]
        rightDiagonalPositions = [2,4,6]

        # check winner in left diagonal
        xorValue = ord(self.cells[0].pegPlaced)
        for i in leftDiagonalPositions:
            if((self.cells[i]).pegPlaced == '#'):
                xorValue = 1
                break
            if(i==0):
                continue
            xorValue = Board.XOR_helper_string(self.cells[0].pegPlaced,self.cells[i].pegPlaced)
            if(xorValue!=0):
                    break
        if(xorValue == 0):
            # winner found
            return self.cells[0].pegPlaced

        # check winner in right diagonal 
        xorValue = ord(self.cells[2].pegPlaced)
        for i in rightDiagonalPositions:
            if((self.cells[i]).pegPlaced == '#'):
                xorValue = 1
                break
            if(i==2):
                continue
            xorValue = Board.XOR_helper_string(self.cells[2].pegPlaced,self.cells[i].pegPlaced)
            if(xorValue!=0):
                    break
        if(xorValue == 0):
            # winner found
            return self.cells[2].pegPlaced

        # no winner found
        return '#'

    def checkRows(self):
        rowStartingPositions = [0,3,6]
        for x in rowStartingPositions:
            xorValue = ord(self.cells[x].pegPlaced)
            for i in range(x,x+3):
                if((self.cells[i]).pegPlaced == '#'):
                    xorValue = 1
                    break
                if(i==x):
                    continue
                xorValue = Board.XOR_helper_string(self.cells[x].pegPlaced,self.cells[i].pegPlaced)
                if(xorValue!=0):
                    break
            if(xorValue == 0):
                # winner found
                return self.cells[x].pegPlaced
        return '#'

    def checkCols(self):
        colStartingPositions = [0,1,2]
        for x in colStartingPositions:
            xorValue = ord(self.cells[x].pegPlaced)
            for i in range(x,x+7,3):
                if((self.cells[i]).pegPlaced == '#'):
                    xorValue = 1
                    break
                if(i==x):
                    continue
                xorValue = Board.XOR_helper_string(self.cells[x].pegPlaced,self.cells[i].pegPlaced)
                if(xorValue!=0):
                    break
            if(xorValue == 0):
                # winner found
                return self.cells[x].pegPlaced
        return '#'

    def calcScore(self):
        # return +100 if X wins, -100 if 0 wins, 0 for tie
        # check diagonals
        winner = self.checkDiagonals()
        if(winner == '#'):
            winner = self.checkRows()
        if(winner == '#'):
            winner = self.checkCols()
        
        if(winner == '#'):
            return 0
        if(winner == 'X'):
            return 100
        if(winner == '0'):
            return -100
        
    # Takes board as input. Obtains list of all possible moves. Picks a move at random. Plays that move.
    def randomMove(self, peg):
        self.isEmpty=False   
        action_list=self.getVacantCells()
        if len(action_list)<2:
            pos=action_list[0].position
        else:
            randPos=random.randint(0,len(action_list)-1)
            pos=action_list[randPos].position
        self.cells[pos].placePeg(peg)
        self.isEmpty = False

    # Retrieves a random move WITHOUT playing it.
    def return_randomMove(self, peg):   
        action_list=self.getVacantCells()
        if len(action_list)<2:
            pos=action_list[0].position
        else:
            randPos=random.randint(0,len(action_list)-1)
            pos=action_list[randPos].position
        return(pos)

    @staticmethod
    def XOR_helper_string(s1,s2):
        return ord(s1)^ord(s2)