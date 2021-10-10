import random
from gameBoard import *


class AI:
    """This class handles all AI-related functionality."""
	
    def __init__(self, diff):
        self.aiDiff = diff
        """User selected AI difficult (Easy, Medium, Hard)."""
        self.currHitShip = []
        self.currDir = "L"
    
    prevShotInfo = [False, None, "Left", None]
    """
    variable for storing if the medium AI previously hit a shot or not, the position of the previous shot if there is one, and where in recursion we are for tracking the shot (Left, Up, Right, or Down).
    Includes parameters [whether "last shot" was a hit (bool), position of last shot, Which direction we need to check, First shot that was a hit].
    Last shot isn't always the most recent shot, but rather whether or not the firing from adjacent squares portion of the code needs to run. you could miss a shot and still be in last shot hit mode..
    """
    
    def takeTurn(self, opponentBoard):
        if self.aiDiff == "E":
            return self.easyAI()
        elif self.aiDiff == "M":
            return self.mediumAI(opponentBoard)
        else:
            return self.hardAI(opponentBoard)

    def easyAI(self):
        """Method for easy difficulty AI. Returns random coordinates."""
        # Generates a random number between 0-9 for the column coord
        colTarget = random.randint(0,9)
       
        #Generates a random int between 0-87 for the row coord
        rowTarget = random.randint(0,8)
       
        # returns the coordinates
        return(colTarget, rowTarget)

        

    def randomPlace(boardVar, shipNumber):
        """Method for placing ships. Takes in the board being placed on and the number of ships to place."""
        i = 1
        randOrient = 0
        randRow = 0
        randCol = 0
        falseCheck = True
        while i <= shipNumber:
            while (falseCheck == True):
                randOrient =  random.randint(0,1)
                randRow =  random.randint(0,8)
                randCol =  random.randint(0,9)
                falseCheck = boardVar.placeShip(i, randOrient, randRow, randCol)
            i = i+1
            falseCheck = True
        return



    def mediumAI(self, opponentBoard):
        """
        Method for medium AI.
        Goes through a basic algorithm when a shot is hit to check each direction for another ship coordinate, starting with left.
        Returns coordinates for shot.
        """
        colTarget = None
        rowTarget = None
        validRowAI = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        validColAI = [0,1,2,3,4,5,6,7,8,9]
        if not self.currHitShip:
            colTarget = random.randint(0,9)
            rowTarget = random.randint(0,8)
            while opponentBoard[rowTarget][colTarget] == "X" or opponentBoard[rowTarget][colTarget] == "*": # do not shoot on already shot positions
                colTarget = random.randint(0,9)
                rowTarget = random.randint(0,8)
            if opponentBoard[rowTarget][colTarget] != "0":
                self.currHitShip.append((colTarget, rowTarget))
            results = (colTarget, rowTarget)
            return(results)
        else:
            if self.currDir == "L":
                colTarget = self.currHitShip[-1][0]-1
                rowTarget = self.currHitShip[-1][1]
                if colTarget in validColAI and opponentBoard[rowTarget][colTarget] != "X" and opponentBoard[rowTarget][colTarget] != "*":
                    if opponentBoard[rowTarget][colTarget] != "0":
                        self.currHitShip.append((colTarget, rowTarget))
                    else:
                        self.currHitShip = [self.currHitShip[0]]
                        self.currDir = "R"
                    results = (colTarget, rowTarget)
                    return(results) # early return is important to not continue checking directions
                else:
                    self.currHitShip = [self.currHitShip[0]]
                    self.currDir = "R"
            
            if self.currDir == "R":
                colTarget = self.currHitShip[-1][0]+1
                rowTarget = self.currHitShip[-1][1]
                if colTarget in validColAI and opponentBoard[rowTarget][colTarget] != "X" and opponentBoard[rowTarget][colTarget] != "*":
                    if opponentBoard[rowTarget][colTarget] != "0":
                        self.currHitShip.append((colTarget, rowTarget))
                    elif len(self.currHitShip) == 1: # if we still only have one hit after checking left/right, we need to check up/down
                        self.currHitShip = [self.currHitShip[0]]
                        self.currDir = "U"
                    else: # if we have gotten multiple hits moving to the right/left, we should not check up/down
                        self.currHitShip = []
                        self.currDir = "L"
                    results = (colTarget, rowTarget)
                    return(results) # early return is important to not continue checking directions
                else:
                    self.currHitShip = [self.currHitShip[0]]
                    self.currDir = "U"
                    
            if self.currDir == "U":
                colTarget = self.currHitShip[-1][0]
                rowTarget = self.currHitShip[-1][1]-1
                if rowTarget in validRowAI and opponentBoard[rowTarget][colTarget] != "X" and opponentBoard[rowTarget][colTarget] != "*":
                    if opponentBoard[rowTarget][colTarget] != "0":
                        self.currHitShip.append((colTarget, rowTarget))
                    else:
                        self.currHitShip = [self.currHitShip[0]]
                        self.currDir = "D"
                    results = (colTarget, rowTarget)
                    return(results) # early return is important to not continue checking directions
                else:
                    self.currHitShip = [self.currHitShip[0]]
                    self.currDir = "D"
                    
            if self.currDir == "D":
                colTarget = self.currHitShip[-1][0]
                rowTarget = self.currHitShip[-1][1]+1
                if rowTarget in validRowAI and opponentBoard[rowTarget][colTarget] != "X" and opponentBoard[rowTarget][colTarget] != "*":
                    if opponentBoard[rowTarget][colTarget] != "0":
                        self.currHitShip.append((colTarget, rowTarget))
                    else: # if we have checked left, right, up, and down and we still miss then we know we are done
                        self.currHitShip = []
                        self.currDir = "L"
                    results = (colTarget, rowTarget)
                    return(results)
                else:
                    self.currHitShip = []
                    self.currDir = "L"
            
    def hardAI(self, board):
        """
        Hard AI method.
        Loops through columns and rows and checks whether value at each 2d index is equal to a ship value (1,2,3,4,5,6).
        Returns j and i as coordinates to call fire method in executive.
        """
        for i in range(9):
            for j in range(10):
                if (board[i][j] == '1') or (board[i][j]== '2') or (board[i][j] == '3') or (board[i][j] == '4') or (board[i][j] == '5') or (board[i][j] == '6'):
                    return(j,i)  
