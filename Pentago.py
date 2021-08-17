# Brandon Soledad, Pentago game with an AI using AlphaBetaPruning and MiniMax search algorithms
import random
import re
import random
from copy import deepcopy
from itertools import product

maxDepth = 1

# Choose between AlphaBetaPruning or MiniMax
searchMethod = 'AlphaBetaPruning'

class game:
    board = ['.'] * 36 # The amount of board spaces not indlcuding the edges of the board
    # Prints the board to console
    def __str__(self):
        newBoard = ''
        newBoard += '+-------+-------+\n'
        for i, j in product(range(2), range(3)):
                newBoard += '| '
                for k, l in product(range(2), range(3)):
                        newBoard += self.board[l + k * 3 + j * 6 + i * 18] + ' '
                        if(l == 2):
                            newBoard += '| '
                newBoard += '\n'
                if(j == 2):
                    newBoard += '+-------+-------+\n'
        return newBoard

    def __eq__(self, b):
        return self.board == b.board

    # Places a piece on the board based on user's input
    def setPiece(self, player, move):
        boardSquare = int(move[0])-1
        index = int(move[2])-1
        self.board[self.boardIndexValues(boardSquare, index)] = player
    
    # Check if a move can be made
    def validMove(self, move):
        boardSquare = int(move[0]) - 1
        index = int(move[2]) - 1
        if(self.board[self.boardIndexValues(boardSquare, index)] == '.'): 
            return True 
        else: 
            return False
    
    # Rotate a game square   
    def rotate(self, move):
        boardSquare = int(move[4]) - 1
        direction = move[5]
        rotated = []
        
        for i in range(3):
            line = []
            for j in range(3):
                line.append(self.board[self.boardIndexValues(boardSquare, j + i * 3)])
            rotated.append(line)
        
        # rotates square either left or right
        if(direction == 'r'):
            rotated = list(zip(*rotated[::-1]))
        else:
            rotated = list(reversed(list(zip(*rotated))))
        
        # places pieces after rotation
        for i, j in product(range(3), range(3)):
                self.board[self.boardIndexValues(boardSquare, j + i * 3)] = rotated[i][j]
    
    # Check to see if game is won by either player or AI   
    def gameWon(self, player):
        winConditionsMet = False
        for i, j in product(range(6), range(6)):
                if self.board[j + i * 6] == player:
                    if(j < 2 and not winConditionsMet):
                        line = []
                        for k in range(5): 
                            line += self.board[j + k + i * 6]
                        winConditionsMet = all(x == player for x in line)
                    if(i < 2 and not winConditionsMet):
                        line = []
                        for k in range(5): 
                            line += self.board[j + (i + k)* 6]
                        winConditionsMet = all(x == player for x in line)
                    if(i < 2  and j < 2 and not winConditionsMet):  
                        line = []
                        for k in range(5): 
                            line += self.board[j + k + (i + k) * 6]
                        winConditionsMet = all(x == player for x in line)
                    if(i < 2 and j > 3 and not winConditionsMet):
                        line = []
                        for k in range(5): 
                            line += self.board[j - k + (i + k)* 6]
                        winConditionsMet = all(x == player for x in line)
                    if(winConditionsMet): 
                        return True
        return False
    
    # returns possible moves on the board
    def possibleMoves(self):
        moves = []
        for boardSquare, index in product(range(1,5), range(1,10)):
            if(self.board[self.boardIndexValues(boardSquare-1, index-1)] == '.'):
                for rotate in range(1, 5):
                    for direction in ['l', 'r']:
                        move = str(boardSquare) + '/' + str(index) + ' ' + str(rotate) + direction
                        moves.append(move)
        return moves        
    
    # Gets board utility based on horizontal and vertical score values
    def boardUtility(self, aiColor, playerColor):
        score = 0
        lines = []
        for i in range(6):
            lines.append(self.board[i * 6: (i + 1) * 6])
        
        score += self.utilityValue(lines, aiColor, playerColor)
        
        lines = []
        for i in range(6):
            line = []
            for j in range(6):
                line.append(self.board[j * 6 + i])
            lines.append(line)
        
        score += self.utilityValue(lines, aiColor, playerColor)
        
        lines = []
        for i in range(1,6):
            line = []
            j = 0
            while ((i + j) * 6 + j) < len(self.board):
                line.append(self.board[(i+j) * 6 + j])
                j += 1
            lines.append(line)
            
        for i in range(6):
            line = []
            j = 0
            while (i + j) < 6:
                line.append(self.board[j * 6 + i + j])
                j += 1
            lines.append(line)
            
        score += self.utilityValue(lines, aiColor, playerColor)
        
        lines = []
        for i in range(1,6):
            line = []
            j = 0
            while (((i + j) * 6 + 5 - j)) < len(self.board):
                line.append(self.board[(i + j) * 6 + 5 - j])
                j += 1
            lines.append(line)

        for i in range(6):
            line = []
            j = 0
            while i - j >= 0:
                line.append(self.board[i + j * 6 - j])
                j += 1
            lines.append(line)
        
        score += self.utilityValue(lines, aiColor, playerColor)
        
        if(score == 0):
            for location in [7, 10, 25, 28]:
                if(self.board[location] == aiColor):
                    score += 2
                if(self.board[location] == playerColor):
                    score -= 2
        
        return score
    
    # Count number of repeating elements and compute utility value
    def utilityValue(self, lines, aiColor, playerColor):
        values = [0, 1, 10, 100, 1000, 1000] 
        utility = 0
        for line in lines:
            if(len(line) > 1):
                count = 0
                for i in range(1, len(line)):
                    if(line[i-1] == line[i]):
                        count += 1
                    else:
                        if(line[i-1] == aiColor):
                            utility += values[count]
                        elif(line[i-1] == playerColor):
                            utility -= values[count]
                        count = 0
                if(count != 0):
                    if(line[i-1] == aiColor):
                        utility += values[count]
                    elif(line[i-1] == playerColor):
                        utility -= values[count]
        return utility
    
    # Board indexes excludes lines separating the board squares
    def boardIndexValues(self, boardSquare, index):
        boardIndex = [[ 0,  1,  2,  6,  7,  8, 12, 13, 14],
                  [ 3,  4,  5,  9, 10, 11, 15, 16, 17],
                  [18, 19, 20, 24, 25, 26, 30, 31, 32],
                  [21, 22, 23, 27, 28, 29, 33, 34, 35]]
        return boardIndex[boardSquare][index]

'+--------------------------------------------------------------------------------------------------+'

# NodeTree class to create a tree
class NodeTree:
    state = None
    previousmove = None
    depth = 0
    value = 0
    children = []
    instance = game()

    # Populates list of children from current game state
    def getChildNode(self, color):
        # Get list of possible moves
        moves = self.state.possibleMoves()
        
        # Create a child for each move and add it to the list
        for move in moves:
            child = NodeTree()
            child.state = game()
            child.state.board = deepcopy(self.state.board)
            child.state.setPiece(color, move)
            child.state.rotate(move)
            child.previousmove = move
            child.depth = self.depth + 1
            child.children = []
            
            boardExists = False
            for i in self.children:
                if(child.state == i.state):
                    boardExists = True
                    break
                
            # Add the new state if it does not exist yet
            if(not boardExists):
                self.children.append(child)


# AI PentagoBot class containing MiniMax and AlphaBeta search algorithms
class PentagoBot:
    tree = None
    currentNode = None
    aiColor = ''
    playerColor = ''
    limit = -1
    nodesVisited = 0
    
    #Used to determine pentago AI move
    def getMove(self, current):
        if(self.tree == None):
            self.tree = NodeTree()
            self.tree.state = current
            self.tree.depth = 0
            self.tree.previousmove = ''
            self.currentNode = self.tree
        else:
            for child in self.currentNode.children:
                if(child.state == current):
                    self.currentNode = child
                    break
                
        # Updates depth limit
        self.limit = self.currentNode.depth + maxDepth
        
        if(searchMethod == 'AlphaBetaPruning'):
            nextNode = self.alphaBeta(self.currentNode)
        if(searchMethod == "MiniMax"):
            nextNode = self.minMax(self.currentNode)
        
        self.nodesVisited = 0
        
        self.currentNode = nextNode
        
        return nextNode.previousmove
        
    # Alpha beta algorithm    
    def alphaBeta(self, node):
        if(len(node.children) == 0):
            node.getChildNode(self.aiColor)
            self.nodesVisited += 1
        
        beta = float('inf')
        alpha = -float('inf')
        prefNode = node.children[0]
        
        for child in node.children:
            child.value = self.alphaBetaMinimize(child, alpha, beta)
            if(child.value > alpha):
                alpha = child.value
                prefNode = child
        return prefNode

    # Finds max value node
    def alphaBetaMaximize(self, node, alpha, beta):
        if(node.depth < self.limit):
            if(len(node.children) == 0):
                node.getChildNode(self.aiColor)
                self.nodesVisited += 1
        
        if(len(node.children) == 0):
            return node.state.boardUtility(self.aiColor, self.playerColor)
        value = -float('inf')
        for child in node.children:
            child.value = self.alphaBetaMinimize(child, alpha, beta)
            value = max(value, child.value)
            if(value >= beta):
                return value
            alpha = max(alpha, value)
        return value

    # Finds min value node    
    def alphaBetaMinimize(self, node, alpha, beta):
        if(node.depth < self.limit):
            if (len(node.children) == 0):
                node.getChildNode(self.playerColor)
                self.nodesVisited += 1

        if(len(node.children) == 0):
            return node.state.boardUtility(self.aiColor, self.playerColor)
        
        value = float('inf')
        for child in node.children:
            child.value = self.alphaBetaMaximize(child, alpha, beta)
            value = min(value, child.value)
            if(value <= alpha):
                return value
            beta = min(beta, value)
        return value
    
    # MiniMax algorithm
    def minMax(self, node):
        if(len(node.children) == 0):
            node.getChildNode(self.aiColor)
            self.nodesVisited += 1
        
        bestValue = self.minMaxMazimize(node)
        prefNode = node.children[0]
        
        for child in node.children:
            if(child.value == bestValue):
                prefNode = child
                break
        return prefNode
    
    def minMaxMazimize(self, node):
        if(node.depth < self.limit):
            if(len(node.children) == 0):
                node.getChildNode(self.aiColor)
                self.nodesVisited += 1
        
        if(len(node.children) == 0):
            return node.state.boardUtility(self.aiColor, self.playerColor)
           
        maxValue = -float('inf')
        for child in node.children:
            child.value = self.minMaxMinimize(child)
            maxValue = max(maxValue, child.value)
        return maxValue
    
    def minMaxMinimize(self, node):
        if(node.depth < self.limit):
            if(len(node.children) == 0):
                node.getChildNode(self.playerColor)
                self.nodesVisited += 1
        
        if(len(node.children) == 0):
            return node.state.boardUtility(self.aiColor, self.playerColor)
          
        minValue = float('inf')
        for child in node.children:
            child.value = self.minMaxMazimize(child)
            minValue = min(minValue, child.value)
        return minValue
    
'+------------------------------------------------------------------------------------------------+'
def main():
    player = ''
    pentagoAI = ''
    turn = ''
    move = ''
    
    newGame = game()
    opponent = PentagoBot()
    
    while player not in ['w', 'b']:
        player = input('Choose Player Color white or black (enter w for white b for black): ').lower() # To choose what pieces player wants
    if(player == 'w'): 
        pentagoAI = 'b'
    else: 
        pentagoAI = 'w'
    
    # Board piece color assign
    opponent.playerColor = player
    opponent.aiColor = pentagoAI
    
    # Determines whether AI or player makes first move
    turn = [player, pentagoAI][random.randint(0,1)]
    if(turn is player): 
        print('Player moves first')
    else: 
        print('pentagoAI moves first')
    print(newGame)
    
    # Game loop, breaks once win condition's by either AI or Player have been met
    while(True):
        if(turn is player):
            valid = False
            # Gets user input for their move and checks if the move is valid
            while not valid:
                move = input('Player turn (%s): ' %player)
                valid = re.match('^[1-4]\/[1-9] [1-4][RrLl]', move)
                if(valid): 
                    valid = newGame.validMove(move)
                if(not valid):
                    print('Invalid move, try again')
        else:
            print("pentagoAI's Turn (%s) Calculating move" %pentagoAI) 
            move = opponent.getMove(newGame)
            
        # Place the piece on the board
        newGame.setPiece(turn, move)
            
        if(newGame.gameWon(player) or newGame.gameWon(pentagoAI)): 
            break
            
        # Rotates square on board
        newGame.rotate(move)
            
        if(newGame.gameWon(player) or newGame.gameWon(pentagoAI)): 
            break
            
        gameTie = False
        if(all(x != '.' for x in newGame.board)):
            gameTie = True
            break
            
        print(move)
        print(newGame)
            
        # Swap who's turn it is
        if(turn is player): 
            turn = pentagoAI
        else: 
            turn = player
        
    print(move)
    print(newGame)
        
    #Checks to see who won meaning who has met the winning conditions
    if(newGame.gameWon(player) and not newGame.gameWon(pentagoAI)): 
        print('Player has won')
    elif(newGame.gameWon(pentagoAI) and not newGame.gameWon(player)): 
        print('pentagoAI has won')
    else: 
        print('Board is filled, game tied')

               
if __name__ == '__main__':
    main()
    