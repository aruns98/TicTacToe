from Board import Board
from Cell import Cell
import random
import time

class Agent:
    def __init__(self):
        # Used for checking the agent's move number.
        self.counter=0

        # Keeping track of old (state,action) and new (state,action) for updates.
        self.old_state=0
        self.old_action=0
        self.new_state=0
        self.new_action=0

        # Exploration rate.
        self.epsilon=0.5

        # Learning rate.
        self.alpha=0.2
        self.alphaCounter=0

        # Discounting factor.
        self.gamma=.8

        # Iterations (used in training).
        self.iter=100

        # Used to determine when to leave current game.
        self.flag=0

        # Used for keep track of game statistics during training.
        self.winCount=0
        self.lossCount=0
        self.tieCount=0

        # Used for keeping track of which peg belongs to whom.
        self.pegDict={}

        # Used for storing all the actions possible from the current state of the agent.
        self.actionDict={}

        # Dictionary that contains all the values of each (state,action) pair. Will constantly be updated for each
        # new (state,action) encounter.
        self.State_Action_Table={}

        # Difference between target and current (state,action) value (used in agent update).
        self.delta=0

        # Used in Sarsa(lambda) algorithm
        self.Expectation_Table={}
        self.lamda=0.8

    # Tells the agent which peg belongs to whom.
    def setPeg(self,agentPeg,oppPeg):
        self.pegDict['A']=agentPeg
        self.pegDict['O']=oppPeg
    
    # Returns a unique string representing a particular state (board position).
    def getState(self, board):
        state=[]
        for i in range(9):
            state.append(board.cells[i].pegPlaced)
        state_str = ''.join(state)
        return state_str

    # Encodes a particular state. This means that the agents peg is always replaced with A
    # and the opponents peg is always replaced with O. This is useful for when the peg of the agent
    # switches with games.
    def codeState(self, state, agentPeg, oppPeg):
        state=state.replace(str(agentPeg),"A")
        state=state.replace(str(oppPeg),"O")
        return state

    # Used for decoding an encoded state. This is required for when an action must be chosen from a state.
    def decodeState(self, state, agentPeg, oppPeg):
        state=state.replace("A", str(agentPeg))
        state=state.replace("O", str(oppPeg))
        return state

    # Takes board as input. Checks value of all valid moves from look-up table. If (state,action) value is not
    # present in the table, then it adds it to the table with a value of 0. It outputs a dictionary containing
    # the value of all possible actions from the given state.
    def checkActionValue(self, board):
        state=self.getState(board)
        state=self.codeState(state, self.pegDict['A'], self.pegDict['O'])
        action_list=board.getVacantCells()
        action_value={}
        for i in action_list:
            if (state,i.position) not in self.State_Action_Table:
                self.State_Action_Table[(state,i.position)]=0
                self.Expectation_Table[(state,i.position)]=0
            action_value[(self.decodeState(state, self.pegDict['A'], self.pegDict['O']),i.position)]=self.State_Action_Table[(state,i.position)]
        return action_value

    # Used for updating the State_Action_Table of the agent. Uses the basic SARSA(1) algorithm.
    def updateAgent(self,actionDict, board, reward=0, end=0):
        # Encoding states.
        self.old_state=self.codeState(self.old_state, self.pegDict['A'], self.pegDict['O'])
        self.new_state=self.codeState(self.new_state, self.pegDict['A'], self.pegDict['O'])
        # Updating (state,action) values.
        if end==0:
            # Delta is the difference between target and current (state,action) estimate.
            self.delta=(reward+(self.gamma*actionDict[(self.decodeState(self.new_state, self.pegDict['A'],self.pegDict['O'] ),self.new_action)])-self.State_Action_Table[(self.old_state,self.old_action)])
            self.State_Action_Table[(self.old_state,self.old_action)]=self.State_Action_Table[(self.old_state,self.old_action)]+(self.alpha)*(self.delta)
        # Different update is made if the agent has reached the terminal state.
        if end==1:
            self.delta=(reward-self.State_Action_Table[(self.old_state,self.old_action)])
            self.State_Action_Table[(self.old_state,self.old_action)]=self.State_Action_Table[(self.old_state,self.old_action)]+(self.alpha)*(self.delta)

    # SARSA(lambda) algorithm.
    def updateAgent2(self,actionDict, board, reward=0, end=0):
        # Encoding states.
        self.old_state=self.codeState(self.old_state, self.pegDict['A'], self.pegDict['O'])
        self.new_state=self.codeState(self.new_state, self.pegDict['A'], self.pegDict['O'])
        # Updating (state,action) values.
        if end==0:
            # Delta is the difference between target and current (state,action) estimate.
            self.delta=(reward+(self.gamma*actionDict[(self.decodeState(self.new_state, self.pegDict['A'],self.pegDict['O'] ),self.new_action)])-self.State_Action_Table[(self.old_state,self.old_action)])
        # Different update is made if the agent has reached the terminal state.
        if end==1:
            self.delta=(reward-self.State_Action_Table[(self.old_state,self.old_action)])
        self.Expectation_Table[(self.old_state,self.old_action)]+=1
        for key in self.State_Action_Table:
            self.State_Action_Table[key]+=(self.alpha*self.delta*self.Expectation_Table[key])
            self.Expectation_Table[key]=(self.gamma*self.lamda*self.Expectation_Table[key])
            
    # Agent makes a single move.
    def agentMove(self, board):
        board.isEmpty=False
        # Retrieves dictionary containing value of all possible actions from current state.
        self.actionDict=self.checkActionValue(board)
        max_value=-1000
        for key in self.actionDict:
            # Finding best possible action (greedy move).
            if self.actionDict[key] > max_value:
                max_value=self.actionDict[key]
                (s,a)=key
                self.new_state=s
        # If random value(0,1) is > epsilon then use greedy move. Else use random move instead (exploration).
        if random.random() > self.epsilon:
            board.cells[a].placePeg(self.pegDict['A'])
            self.new_action=a
        # Exploration.
        else:
            a=board.return_randomMove(self.pegDict['A'])
            board.cells[a].placePeg(self.pegDict['A'])
            self.new_action=a
        # If game isn't over and if this isn't the agent's first move, update the agent.
        if board.gameOver==0 and self.counter>0:
            self.updateAgent(self.actionDict, board)

        # The previously new actions are now old.
        self.old_state=self.new_state
        self.old_action=self.new_action

    # Makes the agent train against an opponent.
    def trainAgent(self, board, oppType=0):
        # Creates a copy agent with the same epsilon and State_Action_Table IF oppType==2 is specified.
        if oppType==2:
            agent2=Agent()
            agent2.epsilon=self.epsilon
            agent2.State_Action_Table=self.State_Action_Table
        # Each iteration constitutes a single game.
        for i in range(0,self.iter):
            # Agent's flag is set to 0. This means that the game is not over yet. 
            self.flag=0
            # Board is initialized.
            board=Board()
            # Keeps track of the number of moves the agent makes in a game. This is required as
            # the agent cannot update for the first move of the game.
            self.counter=0
            # In case the opponent is playing against a copy agent, the second agent's counter is also
            # set to 0.
            if oppType==2:
                agent2.counter=0
            # This determines who starts.
            if random.random() > 0.5:
                # Agent starts.
                board.userPeg='X'
                board.computerPeg='0'
                # Agent knows which pegs belong to whom.
                self.setPeg(board.userPeg,board.computerPeg)
                # If the agent is playing against a copy, even it knows which pegs belong to whom.
                if oppType==2:
                    agent2.setPeg(board.computerPeg,board.userPeg)
                # Starting the game!
                while self.flag==0:
                    # Agent moves first.
                    self.agentMove(board)
                    self.counter+=1
                    # Agent uses this function to evaluate the board state and make necessary terminal updates.
                    board.agentBoardEval(self)
                    if oppType==2:
                        # In case copy agent is playing, it also needs to check the board state for terminal updates.
                        board.agentBoardEval(agent2)
                    # Checks if game is over after agent move.
                    if self.flag==1:
                        continue
                    # Opponent moves.
                    if oppType==0:
                        board.randomMove(board.computerPeg)
                    elif oppType==1:
                        board.minimaxVsAgent()
                    elif oppType==2:
                        agent2.agentMove(board)
                        agent2.counter+=1
                        board.agentBoardEval(agent2)
                    # Board evaluated after opponent made a move.
                    board.agentBoardEval(self)
                    if self.flag==1:
                        continue
            else:
                # Opponent starts.
                board.userPeg='0'
                board.computerPeg='X'
                self.setPeg(board.userPeg,board.computerPeg)
                if oppType==2:
                    agent2.setPeg(board.computerPeg,board.userPeg)
                # Game starts.
                while self.flag==0:
                    if oppType==0:
                        board.randomMove(board.computerPeg)
                    elif oppType==1:
                        board.minimaxVsAgent()
                    elif oppType==2:
                        agent2.agentMove(board)
                        agent2.counter+=1
                        board.agentBoardEval(agent2)
                    board.agentBoardEval(self)
                    if self.flag==1:
                        continue
                    self.agentMove(board)
                    self.counter+=1
                    board.agentBoardEval(self)
                    if oppType==2:
                        board.agentBoardEval(agent2)
                    if self.flag==1:
                        continue
                    
    # Allows user to play against the agent.
    def playAgent(self, board):
        self.flag=0
        board=Board()
        self.counter=0
        # Checks who starts the game.
        st=input('\nInput 1 if you would like to start the game.\n')
        if st=='1':
            # User starts.
            while self.flag==0:
                board.userPeg='0'
                board.computerPeg='X'
                self.setPeg(board.userPeg,board.computerPeg)
                # Prints board without evaluating anything.
                board.printBoard_noCheck()
                # Retrieves move from user and plays it.
                board.userVsAgent()
                board.printBoard_noCheck()
                board.agentBoardEval(self)
                if self.flag==1:
                    continue
                self.agentMove(board)
                board.agentBoardEval(self)
                if self.flag==1:
                    board.printBoard_noCheck()
                    continue
                self.counter+=1
        else:
            # Agent starts.
            while self.flag==0:
                board.userPeg='X'
                board.computerPeg='0'
                self.setPeg(board.userPeg,board.computerPeg)
                board.agentBoardEval(self)
                if self.flag==1:
                    continue
                self.agentMove(board)
                board.printBoard_noCheck()
                board.agentBoardEval(self)
                if self.flag==1:
                    continue
                board.userVsAgent()
                board.printBoard_noCheck()
                self.counter+=1

    def initializeExpectationTable(self):
        self.Expectation_Table=self.State_Action_Table
        for key in self.Expectation_Table:
            self.Expectation_Table[key]=0
        


        