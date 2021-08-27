class Cell:
    def __init__(self,position):
        # pegPlaced can be 'X' or '0' or '#'
        self.pegPlaced='#'
        self.position=position
        # score can be 1,-1,0
        self.score=0

    # function to place a peg in an empty cell
    def placePeg(self, peg):
        self.pegPlaced=peg
    
        
        