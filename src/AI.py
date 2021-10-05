from random import random



class AI:
    #Class Attributes

    #User selected AI difficult (Easy, Medium, Hard)
    aiDiff = None
    #Variable for tracking where the hard AI is at to know the next space to shoot at
    hardPlace = 0
    #prevShot is a variable for storing if the medium AI previously hit a shot or not
    prevShot = False

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
    def mediumFire(opponentBoard, prevShot):
        #Array of possible column inputs for firing at
        colArr = ['A','B','C','D','E','F','G','H','I','J']
        # Generates a random number between 0-9 to index the array
        colRand = random.randrange(0,9,1)
        colTarget = None
        rowTarget = None
        if prevShot is False:    
            colTarget = colArr[colRand]
            rowTarget = random.randrange(1,9,1)


        return
        
