import random
from gameBoard import *


class AI:
    #Class Attributes

    #User selected AI difficult (Easy, Medium, Hard)
    aiDiff = None
    
    #Bool variable for whether player is playing against AI
    aiOpp = False
   
    #def __init__(self):
	    #self.rows = 9
	    #self.columns = 10

    #prevShotInfo is a variable for storing if the medium AI previously hit a shot or not, the position of the previous shot if there is one, and where in recursion we are for tracking the shot (Left, Up, Right, or Down)
    # includes parameters [whether "last shot" was a hit (bool)    ,  position of last shot    ,  Which direction we need to check , First shot that was a hit   ]
    # last shot isn't always the most recent shot, but rather whether or not the firing from adjacent squares portion of the code needs to run. you could miss a shot and still be in last shot hit mode.
    prevShotInfo = [False, None, "Left", None]
    


    # return on coordinates
    #Method for easy difficulty AI
    def easyAI():
        # Generates a random number between 0-9 for the column coord
        colTarget = random.randint(0,9)
       
        #Generates a random int between 0-87 for the row coord
        rowTarget = random.randint(0,8)
       
        # reutrns the coordinates
        return(colTarget, rowTarget)

        







    #Shots previous are not taken into account
    #still need to add previous shot detection
    #functionality is supposed to be semi smart (shoot straight once you get a 2 streak)
    def mediumFire(opponentBoard, prevShotInfo):
        #Array of possible column inputs for firing at
        colArr = ['A','B','C','D','E','F','G','H','I','J']
        # Generates a random number between 0-9 to index the array
        colRand = random.randint(0,9,1)
        colTarget = None
        rowTarget = None
        int_Col = None
        validRowAI = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        validColAI = [1,2,3,4,5,6,7,8,9,10]
        #if the previous shot didn't hit, then shoot randomly
        if prevShotInfo[0] is False:    
            colTarget = colArr[colRand]
            rowTarget = random.randint(1,9,1)
            int_Col = ord(colTarget) - 64
            hitOrMiss = opponentBoard.shotOn(rowTarget - 1, int_Col - 1)
            if  (hitOrMiss != 0):
                prevShotInfo[0] = True
                prevShotInfo[1] = (rowTarget-1,int_Col-1)
                prevShotInfo[3] = (rowTarget-1,int_Col-1)
            results = [rowTarget, colTarget, hitOrMiss]
            return(results)
        if prevShotInfo[0] is True:
            if prevShotInfo[2] is "Left":
                if (rowTarget-2) in validRowAI:
                    hitOrMiss = opponentBoard.shotOn(rowTarget - 2, int_Col - 1)
                    if  (hitOrMiss != 0):
                        prevShotInfo[0] = True
                      #  prevShotInfo[1] = (rowTarget-1,int_Col-1)
                     #   prevShotInfo[3] = (rowTarget-1,int_Col-1)
                
                
            if prevShotInfo[2] is "Up" and (int_Col-2) > -1:
                return
            if prevShotInfo[2] is "Right":
                return
            if prevShotInfo[2] is "Down":
                return

            
        return
        





    def hardAI(board):
        for i in range(9):
            for j in range(10):
                if (board[i][j] == '1') or (board[i][j]== '2') or (board[i][j] == '3') or (board[i][j] == '4') or (board[i][j] == '5') or (board[i][j] == '6'):
                    return(j,i)  
