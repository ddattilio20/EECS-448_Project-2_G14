"""This package handles the executive/game logic functionality."""
from gameBoard import gameBoard
from AI import *
import os
clear = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
"""Clears terminal with appropriate OS call"""

class Executive:
	"""This class handles the executive/game logic functionality. It is initiated from main"""

	playerTurn = 0
	"""Keeps track of which player's turn it is. 0 for player 1, 1 for player 2."""
	roundNum = 0
	"""Keeps track of what round the game is on. Extra, but could be used on transition screen and win screen"""
	aiOpp = False
	"""Bool variable for whether player is playing against AI."""
	ai = None
	"""Initializes selected AI difficulty"""

	def __init__(self):
		"""Constructor, creates two gameBoard instances"""
		self.boardOne = gameBoard()
		self.boardTwo = gameBoard()
		"""Keeps track of how many scans each player has. Intially have 3 scans, 1 of each.
		First element corresponds to X scans, second element corresponds to + scans, third element to block scans (3x3)."""
		self.player1scan = [1, 1, 1]
		self.player2scan = [1, 1, 1]
		self.scanShotName = ["X","Cross","Block"]

	def runGame(self):
		"""Does setup for game and AI then runs the game logic in a loop until someone wins"""

		# variable needed to transfer information from self.takeTurn to self.transition - andrew
		turnResult = [0, "A", 0]
		numShipInput = [1, 2, 3, 4, 5, 6]
		self.numShips = 0

		userInput = ''
		while userInput != 'Y' and userInput != 'N':
			userInput = input("Would you like to play against the AI? (Y or N): ")
			userInput = userInput.upper()

		if userInput == 'Y' or userInput == 'y':
			self.aiOpp = True
		elif userInput == 'N' or userInput == 'n':
			self.aiOpp = False

		diff = ''
		if self.aiOpp == True:
			while diff != 'E' and diff != 'M' and diff != 'H':
				diff = input("What difficulty would you like to play against, Easy, Medium, or Hard? (E, M, or H): ")
				diff = diff.upper()
			self.ai = AI(diff)

		# Ask how many ships there will be
		# This while loop prompts the user for the ship count and repromts until valid input is given.
		while self.numShips not in numShipInput:
			try:
				self.numShips = int(input("How many ships would you like in your BattleShip game? (1-6): "))
			except ValueError:
				print("Invalid input. Please try again.")
				continue
			if self.numShips not in numShipInput:
				print("Invalid input. Please try again.")

		# board setup for when not playing AI
		if self.aiOpp == False:
			# Set up each player's board
			clear()
			print ("Setting up Player 1's Board")
			print()
			print("Legend:")
			print("[X] = Hit, [*] = Miss, [1-6] = Ship, [~] = Open Waters")
			print()
			self.setUp(self.boardOne, self.numShips)
			clear()
			print ("Setting up Player 2's Board")
			print()
			print("Legend:")
			print("[X] = Hit, [*] = Miss, [1-6] = Ship, [~] = Open Waters")
			print()
			self.setUp(self.boardTwo, self.numShips)

		# If using AI, has user setup player 1 board and random ship method sets up player 2 board
		elif self.aiOpp == True:
			# Set up each player's board
			clear()
			print ("Setting up Player 1's Board")
			print()
			print("Legend:")
			print("[X] = Hit, [*] = Miss, [1-6] = Ship, [~] = Open Waters")
			print()
			self.setUp(self.boardOne, self.numShips)
			clear()
			# call random ship placement on self.boardTwo
			AI.randomPlace(self.boardTwo, self.numShips)

		# Small transition between player 2 setup and first turn
		clear()
		if self.aiOpp:
			# self.boardTwo.printPlayerView() # for testing AI placement
			input("Setup complete. Press enter to start game")
		else:
			input("Setup complete. Give control to player 1 and press enter to start game")

		gameOver = False
		while not(gameOver):
			# increment roundNum
			self.roundNum += 1

			# Each player takes their turn
			turnResult = self.takeTurn(self.boardOne, self.boardTwo)

			# display transition turn for player one, if player one has won break out of loop
			if(self.transitionScreen(turnResult)):
				gameOver = True
				break

			# increment the playerTurn
			self.playerTurn = (self.playerTurn + 1) % 2

			turnResult = self.takeTurn(self.boardTwo, self.boardOne)

			# display transition turn for player two, if player two has won break out of loop
			if(self.transitionScreen(turnResult)):
				gameOver = True
				break

			# increment the playerTurn
			self.playerTurn = (self.playerTurn + 1) % 2
			# Loop through above logic until someone wins

		self.winScreen()

	def setUp(self, gameBoard, numShips):
		"""
		Performs the board setup for one player's board. Will not let players place ships in an invalid spot.
		Takes in a game board and the maximum number of ships.
		"""
		ShipNames=["LifeBoat(size=1)", "Destroyer(size=2)", "Submarine(size=3)", "BattleShip(size=4)", "Carrier(size=5)", "Cruiser(size=6)"]
		orientation = True
		alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
		alphabetInt = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

		gameBoard.printPlayerView()      # initial print to show the board
		for i in range(numShips):
			failChecker = True           # this variable for use in the while loop guarding the usage of placeShip
			while(failChecker == True):
				x_coordinates = "0"
				y_coordinates = 0
				Input_orientation = "0"  # this variable used for taking initial orientation input before converting to a bool

				print("Placing the " + ShipNames[i])
				print("When placing ships, specify the column and row of the topmost or leftmost tile (based on orientation)")

				# take in and convert orientation to a bool

				if (i != 0): # no need to ask for orientation when ship is size 1
					while Input_orientation != "H" and Input_orientation != "V" and Input_orientation != "h" and Input_orientation != "v":
						Input_orientation = input("What orientation would you like (H/V)?: ")
						if Input_orientation != "H" and Input_orientation != "V" and Input_orientation != "h" and Input_orientation != "v":
							print("Invalid input. Please try again.")
					if (Input_orientation =='H' or Input_orientation == 'h'):
						orientation = False
					elif (Input_orientation == 'V' or Input_orientation == 'v'):
						orientation = True

				# take in and convert x-coordinate to an int (using ASCII values)
				while x_coordinates not in alphabet:
					x_coordinates = input("What column do you want the Ship to be placed in? (A-J): ")
					if x_coordinates not in alphabet:
						print("Invalid input. Please try again.")
				x_coordinates = x_coordinates.capitalize()
				x_coordinates = ord(x_coordinates) - 64

				# take in and convert y-coordinate to an int (from associated string)
				while y_coordinates not in alphabetInt:
					y_coordinates = input("What row do you want the Ship to be placed on? (1-9): ")
					if y_coordinates not in alphabetInt:
						print("Invalid input. Please try again.")
				y_coordinates = int(y_coordinates)

				ShipSize = int(i+1)

				# call placeShip passing in the input values. While loop will run again unless the placement is successful
				failChecker = gameBoard.placeShip(ShipSize, orientation, y_coordinates, x_coordinates)
				if failChecker == True:
					print("Unable to place ship!")

			# print the board so players can see where their ship was placed.
			gameBoard.printPlayerView()

		input("Press enter to continue...")

	def takeTurn(self, playerBoard, opponentBoard):
		"""
		Shows player their view of both game boards, asks for a row and column, then performs a shot.
		Returns an array containing [row of shot, column of shot, 0-6 miss/ship hit]
		"""
		# Initializing variables for input guards
		validRow = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		validCol = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
		validScan = ["1", "2", "3"]
		row = 0
		column = ""
		scanRow = 0
		scanCol = ""
		scanOption = ""
		scanType = 0
		scanMode = False


		# Prints player's view of current boardstate
		clear()
		if not(self.playerTurn):
			print("Player One's Turn")
		else:
			print("Player Two's Turn")
		print()
		print("Legend:")
		print("[X] = Hit, [*] = Miss, [1-6] = Ship, [~] = Open Waters... as far as you know")
		print()
		print("Enemy's Waters")
		opponentBoard.printOpponentView()
		print()
		print("Friendly Territory")
		playerBoard.printPlayerView()
		print()

		# Code for if there is an AI
		if self.aiOpp == True:
			# if its the user's turn, player1
			if self.playerTurn == 0:

				# Get scanShot option from player
				# here only player1 is human so only player1 will get a scan shot
				if self.player1scan[0] != 0 or self.player1scan[1] != 0 or self.player1scan[2] != 0:
					while scanOption != "Y" and scanOption != "N" and scanOption != "y" and scanOption != "n":
						scanOption = input("Would you like to use a scan? (Y or N): ")
						if scanOption != "Y" and scanOption != "N" and scanOption != "y" and scanOption != "n":
							print("Invalid input. Please try again.")
					# Player selects scan mode
					if (scanOption == "y" or scanOption == "Y"):
						# scanMode = True
						# Print to the player which scans are available
						print("You have these scans available: [", end = " ")
						for i in range(len(self.scanShotName)):
							if (self.player1scan[i] == 1):
								print(self.scanShotName[i], end = " ")
						print("]")
						# Guard against invalid scan input
						while scanType not in validScan:
							scanType = input("Select which scan you would like to use (X = 1, Cross = 2, Block = 3): ")
							if scanType not in validScan:
								print("Invalid scan input. Please try again.")
							# Guard against players using the same scan more than once
							# here scanType is valid but the corresponding scan may not be available
							elif self.player1scan[int(scanType)-1] != 1:
								print("Scan unavailable. Please select another one.")
								scanType = "0" # Needed to loop while condition
						# Print out which shot the player selected
						print("You selected:",self.scanShotName[int(scanType)-1])
						# Show the corresponding scan has been used in player1scan list
						self.player1scan[int(scanType)-1] = 0
						print("Choose coordinates to fire scan shot")
						# Get row and col input for scan shot location
						# This while loop prompts the user for the column and row and repromts until valid input is given.
						while scanCol not in validCol:
							scanCol = input("Input target column (A-J): ")
							if scanCol not in validCol:
								print("Invalid input. Please try again.")
						while scanRow not in validRow:
							try:
								scanRow = int(input("Input target row (1-9): "))
							except ValueError:
								print("Invalid input. Please try again.")
								continue
							if scanRow not in validRow:
								print("Invalid input. Please try again.")
						scanCol = scanCol.capitalize()
						int_scanCol = ord(scanCol) - 64
						# Scan shot on enemy board, then print enemy baord
						opponentBoard.scanShot(int(scanType), scanRow-1, int_scanCol-1)
						print("Scan shot fired!")
						print("Scanning Enemy's Waters...")
						opponentBoard.printOpponentView();
					# Player doesn't select scan mode, continue to firing regular shot
					elif (scanOption == "n" or scanOption == "N"):
						scanMode = False

				# Print this to help distinguisih between scan and regular shot
				print("Choose coordinates to fire regular shot")
				# Takes column and row input from user
				# This while loop prompts the user for the column and row and repromts until valid input is given.
				while column not in validCol:
					column = input("Input target column (A-J): ")
					if column not in validCol:
						print("Invalid input. Please try again.")
				while row not in validRow:
					try:
						row = int(input("Input target row (1-9): "))
					except ValueError:
						print("Invalid input. Please try again.")
						continue
					if row not in validRow:
						print("Invalid input. Please try again.")

				# Converts input, takes shot, and records results to output array
				column = column.capitalize()
				int_Column = ord(column) - 64
				hitOrMiss = opponentBoard.shotOn(row-1, int_Column-1)
				results = [row, column, hitOrMiss]
				return(results)

			# AI Gameplay functions if its the AI's turn
			elif self.playerTurn == 1:
				columnTarget, rowTarget = self.ai.takeTurn(opponentBoard.board)
				hitOrMiss = opponentBoard.shotOn(rowTarget, columnTarget)
				row = rowTarget+1
				column = validCol[columnTarget]
				results = [row, column, hitOrMiss]
				return(results)

		# Code for if no AI, PvP
		else:
			# Get scanShot option from player
			# Check which player is playing, player 1 -> turn = 0, player 2 -> turn = 1
			# If player 1, use player1scan
			if self.playerTurn == 0:
				if self.player1scan[0] != 0 or self.player1scan[1] != 0 or self.player1scan[2] != 0:
					while scanOption != "Y" and scanOption != "N" and scanOption != "y" and scanOption != "n":
						scanOption = input("Would you like to use a scan? (Y or N): ")
						if scanOption != "Y" and scanOption != "N" and scanOption != "y" and scanOption != "n":
							print("Invalid input. Please try again.")
					# Player selects scan mode
					if (scanOption == "y" or scanOption == "Y"):
						# scanMode = True
						# Print to the player which scans are available
						print("You have these scans available: [", end = " ")
						for i in range(len(self.scanShotName)):
							if (self.player1scan[i] == 1):
								print(self.scanShotName[i], end = " ")
						print("]")
						# Guard against invalid scan input
						while scanType not in validScan:
							scanType = input("Select which scan you would like to use (X = 1, Cross = 2, Block = 3): ")
							if scanType not in validScan:
								print("Invalid scan input. Please try again.")
						# Guard against players using the same scan more than once
						# here scanType is valid but the corresponding scan may not be available
							elif self.player1scan[int(scanType)-1] != 1:
								print("Scan unavailable. Please select another one.")
								scanType = "0" # Needed to loop while condition
					# Print out which shot the player selected
						print("You selected:",self.scanShotName[int(scanType)-1])
					# Show the corresponding scan has been used in player1scan list
						self.player1scan[int(scanType)-1] = 0
						print("Choose coordinates to fire scan shot")
						# Get row and col input for scan shot location
						# This while loop prompts the user for the column and row and repromts until valid input is given.
						while scanCol not in validCol:
							scanCol = input("Input target column (A-J): ")
							if scanCol not in validCol:
								print("Invalid input. Please try again.")
						while scanRow not in validRow:
							try:
								scanRow = int(input("Input target row (1-9): "))
							except ValueError:
								print("Invalid input. Please try again.")
								continue
							if scanRow not in validRow:
								print("Invalid input. Please try again.")
						scanCol = scanCol.capitalize()
						int_scanCol = ord(scanCol) - 64
						# Scan shot on enemy board, then print enemy baord
						# cast scanType to int to match function
						opponentBoard.scanShot(int(scanType), scanRow-1, int_scanCol-1)
						print("Scan shot fired!")
						print("Scanning Enemy's Waters...")
						opponentBoard.printOpponentView();

			# Player 2's turn, use player2scan
			elif self.playerTurn == 1:
				if self.player2scan[0] != 0 or self.player2scan[1] != 0 or self.player2scan[2] != 0:
					while scanOption != "Y" and scanOption != "N" and scanOption != "y" and scanOption != "n":
						scanOption = input("Would you like to use a scan? (Y or N): ")
						if scanOption != "Y" and scanOption != "N" and scanOption != "y" and scanOption != "n":
							print("Invalid input. Please try again.")
					# Player selects scan mode
					if (scanOption == "y" or scanOption == "Y"):
						# scanMode = True
						# Print to the player which scans are available
						print("You have these scans available: [", end = " ")
						for i in range(len(self.scanShotName)):
							if (self.player2scan[i] == 1):
								print(self.scanShotName[i], end = " ")
						print("]")
						# Guard against invalid scan input
						while scanType not in validScan:
							scanType = input("Select which scan you would like to use (X = 1, Cross = 2, Block = 3): ")
							if scanType not in validScan:
								print("Invalid scan input. Please try again.")
						# Guard against players using the same scan more than once
						# here scanType is valid but the corresponding scan may not be available
							elif self.player2scan[int(scanType)-1] != 1:
								print("Scan unavailable. Please select another one.")
								scanType = "0" # Needed to loop while condition
					# Print out which shot the player selected
						print("You selected:",self.scanShotName[int(scanType)-1])
					# Show the corresponding scan has been used in player1scan list
						self.player2scan[int(scanType)-1] = 0
						print("Choose coordinates to fire scan shot")
						# Get row and col input for scan shot location
						# This while loop prompts the user for the column and row and repromts until valid input is given.
						while scanCol not in validCol:
							scanCol = input("Input target column (A-J): ")
							if scanCol not in validCol:
								print("Invalid input. Please try again.")
						while scanRow not in validRow:
							try:
								scanRow = int(input("Input target row (1-9): "))
							except ValueError:
								print("Invalid input. Please try again.")
								continue
							if scanRow not in validRow:
								print("Invalid input. Please try again.")
						scanCol = scanCol.capitalize()
						int_scanCol = ord(scanCol) - 64
						# Scan shot on enemy board, then print enemy baord
						# cast scanType to int to match function
						opponentBoard.scanShot(int(scanType), scanRow-1, int_scanCol-1)
						print("Scan shot fired!")
						print("Scanning Enemy's Waters...")
						opponentBoard.printOpponentView();

			# Print this to help distinguisih between scan and regular shot
			print("Choose coordinates to fire regular shot")
			# Takes column and row input from user
			# This while loop prompts the user for the column and row and repromts until valid input is given.
			while column not in validCol:
				column = input("Input target column (A-J): ")
				if column not in validCol:
					print("Invalid input. Please try again.")
			while row not in validRow:
				try:
					row = int(input("Input target row (1-9): "))
				except ValueError:
					print("Invalid input. Please try again.")
					continue
				if row not in validRow:
					print("Invalid input. Please try again.")

		# Converts input, takes shot, and records results to output array
		column = column.capitalize()
		int_Column = ord(column) - 64
		hitOrMiss = opponentBoard.shotOn(row-1, int_Column-1)
		results = [row, column, hitOrMiss]
		return(results)


	def transitionScreen(self, turnResults):
		"""
		Displays the result of the last shot (hit/miss, which ship was hit/sunk). If a ship was sunk, check if game has been won. If so, end loop and go to winscreen. If not, ask to give control to next player and wait for confirmation.
		Takes in an array containing [row of shot, column of shot, 0-6 miss/ship hit].
		Returns whether the game has been won.
		"""

		# Ship names, for easy output
		ShipNames=["LifeBoat(size=1)", "Destroyer(size=2)", "Submarine(size=3)", "BattleShip(size=4)", "Carrier(size=5)", "Cruiser(size=6)"]

		# This is the return variable, if it is true, then the game ends
		endGame = False

		# clear screen and display the turn
		clear()
		turnNo = str(self.roundNum)
		print("Results of round " + turnNo + ": ")

		# display where shot
		row = str(turnResults[0])
		col = str(turnResults[1])
		print("Shot on " + col + row + "... ")
		# check if shot hit
		if(turnResults[2] != 0):
			print("Hit!")

			# print results of shot
			print("You hit a " + ShipNames[turnResults[2]-1])

			# check if the game has been won
			if(self.boardTwo.gameLost() or self.boardOne.gameLost()):
				endGame = True
		else:
			print("Missed!")

		# display opponentView of board that got hit
		print()
		if not self.playerTurn:
			print("Player 2's Board:")
		else:
			print("Player 1's Board:")
		print()
		print("Legend:")
		print("[X] = Hit, [*] = Miss, [1-6] = Ship, [~] = Open Waters")
		print()
		if not self.playerTurn:
			self.boardTwo.printOpponentView()
		else:
			self.boardOne.printOpponentView()
		print()

		# Prompt user to continue
		if not endGame:
			if(self.aiOpp and not self.playerTurn):
				print("Press enter when ready for AI turn")
			elif(not self.playerTurn):
				print("Please give control to player 2. Player 2, press enter when ready")
			elif(self.aiOpp):
				print("Player 1, press enter when ready for your turn")
			else:
				print("Please give control to player 1. Player 1, press enter when ready")
		else:
			if(not self.playerTurn):
				print("We have bad news for player 2... press enter when they're ready")
			else:
				print("We have bad news for player 1... press enter when they're ready")

		input()
		return endGame

	def winScreen(self):
		"""Displays both boards and announces the winner"""
		# Clear screen and display which player won and on what turn
		clear()
		round = str(self.roundNum)
		if self.boardOne.gameLost():
			print("Player Two wins on round " + round + "!\n")
		elif self.boardTwo.gameLost():
			print("Player One wins on round " + round + "!\n")

		print("Legend:")
		print("[X] = Hit, [*] = Miss, [1-6] = Ship, [~] = Open Waters")
		print()

		# Display both board states and thank the player
		print("Player One's board:\n")
		self.boardOne.printPlayerView()
		print()
		print("Player Two's board:\n")
		self.boardTwo.printPlayerView()
		print()
		print("Thanks for playing!")
