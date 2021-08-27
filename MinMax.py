class MinMax:
    # Counting the number of minimax function calls
    count=0

    @staticmethod
    def minimizer(board, depth, alpha, beta):
        # Increases count by one
        MinMax.count+=1
        posForMinimizer=0
        # minimize
        vacantCells = board.getVacantCells()
        minScore = 1000
        for cell in vacantCells:
            cell.placePeg('0')
            score = board.calcScore()
            if(score != 0): 
                # Adding depth to score penalizes moves that win after longer number of moves
                cell.score = score + depth
            elif(score==0 and len(vacantCells)==1):
                # last vacant cell was left, this means now the board is full with no winner
                cell.score = score + depth
            else:
                # We increase the depth everytime we call the function
                # min_list stores the score and best position information
                min_list=MinMax.maximizer(board, depth+1, alpha, beta)
                cell.score = min_list[0]
            
            # once the vacant cell has an associated score
            if(cell.score < minScore):
                minScore = cell.score
                # posForMinimizer stores the cell position
                posForMinimizer=cell.position

            # Beta is evaluated. If less than alpha, the branch breaks.
            beta=min(beta,cell.score)
            if beta <= alpha:
                cell.placePeg('#')
                cell.score=0
                break

            # unplace peg  
            cell.placePeg('#')
            cell.score=0
        
        # The function returns a list containing the score and the best position.
        return [minScore,posForMinimizer]

    @staticmethod
    def maximizer(board, depth, alpha, beta):
        # Increases count by one
        MinMax.count+=1
        posForMaximizer=0
        # maximize
        vacantCells = board.getVacantCells()
        maxScore = -1000
        for cell in vacantCells:
            cell.placePeg('X')
            score = board.calcScore()
            if(score != 0):
                # Subtracting depth from score penalizes moves that win after longer number of moves
                cell.score = score - depth
            elif(score==0 and len(vacantCells)==1):
                # last vacant cell was left, this means now the board is full with no winner
                cell.score = score - depth
            else:
                # We increase the depth everytime we call the function
                # max_list stores the score and best position information
                max_list = MinMax.minimizer(board, depth+1, alpha, beta)
                cell.score = max_list[0]
                
            
            # once the vacant cell has an associated score
            if(cell.score > maxScore):
                maxScore = cell.score
                # posForMinimizer stores the cell position
                posForMaximizer=cell.position

            # Alpha is evaluated. If beta is less than alpha, the branch breaks
            alpha=max(alpha,cell.score)
            if beta <= alpha:
                cell.placePeg('#')
                cell.score=0
                break

            # unplace peg
            cell.placePeg('#')
            cell.score=0

        # The function returns a list containing the score and the best position.
        return [maxScore,posForMaximizer]