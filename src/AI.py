from random import random



class AI:
    #Class Attributes

    #User selected AI difficult (Easy, Medium, Hard)
    aiDiff = None
    #Variable for tracking where the hard AI is at to know the next space to shoot at
    hardPlace = 0

    #prevShotInfo is a variable for storing if the medium AI previously hit a shot or not, the position of the previous shot if there is one, and where in recursion we are for tracking the shot (Left, Up, Right, or Down)
    # includes parameters [whether "last shot" was a hit (bool)    ,  position of last shot    ,  Which direction we need to check , First shot that was a hit   ]
    # last shot isn't always the most recent shot, but rather whether or not the firing from adjacent squares portion of the code needs to run. you could miss a shot and still be in last shot hit mode.
    prevShotInfo = [False, None, "Left", None]
    aiOpp = 'N'


    #Method for easy difficulty AI
    def easyAI(opponentBoard):
        #Array of possible column inputs for firing at
        colArr = ['A','B','C','D','E','F','G','H','I','J']
        # Generates a random number between 0-9 to index the array
        colRand = random.randrange(0,9,1)
        # Creates column value for firing based on the array and random number
        colTarget = colArr[colRand]

        #Creates row value for firing by generating random nmber from 1-9
        rowTarget = random.randrange(1,9,1)

        int_Col = ord(colTarget) - 64

        hitOrMiss = opponentBoard.shotOn(rowTarget - 1, int_Col - 1)
        results = [rowTarget, colTarget, hitOrMiss]
        return(results)

        




   # def hardFire(opponentBoard):


    #Shots previous are not taken into account
    #still need to add previous shot detection
    def mediumFire(opponentBoard, prevShot):
        #Array of possible column inputs for firing at
        colArr = ['A','B','C','D','E','F','G','H','I','J']
        # Generates a random number between 0-9 to index the array
        colRand = random.randrange(0,9,1)
        colTarget = None
        rowTarget = None
        #if the previous shot didn't hit, then shoot randomly
        if prevShot[0] is False:    
            colTarget = colArr[colRand]
            rowTarget = random.randrange(1,9,1)
            int_Col = ord(colTarget) - 64
            hitOrMiss = opponentBoard.shotOn(rowTarget - 1, int_Col - 1)
            results = [rowTarget, colTarget, hitOrMiss]
            return(results)
        if prevShot[0] is True:
            if 

            return

        return
        