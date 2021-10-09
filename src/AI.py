import random
from gameBoard import *


class AI:
    """This class handles all AI-related functionality."""

    aiDiff = None
    """User selected AI difficult (Easy, Medium, Hard)."""
    
    aiOpp = False
    """Bool variable for whether player is playing against AI."""
   
    #def __init__(self):
	    #self.rows = 9
	    #self.columns = 10

    
    prevShotInfo = [False, None, "Left", None]
    """
    variable for storing if the medium AI previously hit a shot or not, the position of the previous shot if there is one, and where in recursion we are for tracking the shot (Left, Up, Right, or Down).
    Includes parameters [whether "last shot" was a hit (bool), position of last shot, Which direction we need to check, First shot that was a hit].
    Last shot isn't always the most recent shot, but rather whether or not the firing from adjacent squares portion of the code needs to run. you could miss a shot and still be in last shot hit mode..
    """
    
    def easyAI():
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





    #Shots previous are not taken into account
    #still need to add previous shot detection
    #functionality is supposed to be semi smart (shoot straight once you get a 2 streak)
    def mediumFire(opponentBoard, prevShotInfo):
        #Array of possible column inputs for firing at
        # Generates a random number between 0-9 to index the array
        colTarget = None
        rowTarget = None
        int_Col = None
        validRowAI = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        validColAI = [1,2,3,4,5,6,7,8,9,10]
        #if the previous shot didn't hit, then shoot randomly
        if prevShotInfo[0] is False:    
            colTarget = random.randint(0,9)
            rowTarget = random.randint(0,8)
            hitOrMiss = opponentBoard[rowTarget][colTarget]
            if  (hitOrMiss != "0" and hitOrMiss != "X" and hitOrMiss != "*"):
                prevShotInfo[0] = True
                prevShotInfo[1] = (rowTarget,colTarget)
                prevShotInfo[3] = (rowTarget,colTarget)
            results = (rowTarget, colTarget)
            return(results)
        if prevShotInfo[0] is True:
            rowTarget = prevShotInfo[1][0]
            colTarget = prevShotInfo[1][1]
            if prevShotInfo[2] == "Left":
                if (rowTarget-1) in validRowAI:
                    hitOrMiss = opponentBoard[rowTarget-1][colTarget]
                    if  (hitOrMiss != "0" and hitOrMiss != "X" and hitOrMiss != "*"):
                        prevShotInfo[0] = True
                      #  prevShotInfo[1] = (rowTarget-1,int_Col-1)
                    #   prevShotInfo[3] = (rowTarget-1,int_Col-1)
                
                
            if prevShotInfo[2] == "Up" and (int_Col-2) > -1:
                return
            if prevShotInfo[2] == "Right":
                return
            if prevShotInfo[2] == "Down":
                return

            
        return
        

    def subMediumFire(opponentBoard, prevShotInfo, validRowAI, validColAI):
        return



    def hardAI(board):
        """
        Hard AI method.
        Loops through columns and rows and checks whether value at each 2d index is equal to a ship value (1,2,3,4,5,6).
        Returns j and i as coordinates to call fire method in executive.
        """
        for i in range(9):
            for j in range(10):
                if (board[i][j] == '1') or (board[i][j]== '2') or (board[i][j] == '3') or (board[i][j] == '4') or (board[i][j] == '5') or (board[i][j] == '6'):
                    return(j,i)  
