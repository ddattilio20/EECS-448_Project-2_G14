class gameBoard:
	"""This class handles the board data and logic. Two instances are intitiaited from Executive, one for each player."""

	# Class Attributes
	columns = 10
	"""Number of columns, A-J"""
	rows = 9
	"""Number of rows, 1-9"""
	# Constructor: Creates a 2D array of integers with all spots marked empty(0)
	def __init__(self):
		"""Constructor, initializes empty array"""
		self.board = [["0" for i in range(self.columns)]
		                   for j in range(self.rows)]

	# Returns the content of the specified tile
	def getTile(self, row, col):
		"""Gets data at indices"""
		return(self.board[row][col])

	def placeShip(self, size, orientation, row, col): #i.e. (4, True, 5, 4)
		"""
		Called when setting up the board. Takes the type of ship, along with the orientation and coordinates for the leftmost or topmost coordinate of the ship.
		Takes in ship size, ship orientation (horizontal is 0, vertical is 1),	row index, column index.
		Returns whether ship placement failed.
		"""
		success = False  # this flag used to end while loop without breaking
		fail = False     # this flag used to break the loop and return a negative result if the input would lead to invalid placement
		while not success:
			# vertical
			if orientation:
				if row + size <= 10:
					for i in range(row, row + size):
						if self.board[i-1][col-1] != "0": # dry run checking if there are any ships in the way of placement
							fail = True

					if fail:
						break

					for i in range(row, row + size):
						if self.board[i-1][col-1] == "0":
							self.board[i-1][col-1] = str(size)  # placing ship
							success = True
				else:
					fail = True
					break

			# horizontal
			elif not orientation:
				if col + size <= 11:
					for i in range(col, col + size):
						if self.board[row-1][i-1] != "0": # dry run checking if there are any ships in the way of placement
							fail = True

					if fail:
						break

					for i in range(col, col + size):
						if self.board[row-1][i-1] == "0":
							self.board[row-1][i-1] = str(size)  # placing ship
							success = True
				else:
					fail = True
					break
		return(fail)

	def shotOn(self, row, col):
		"""
		Asserts whether a shot at a given coordinate is a hit or miss.
		Takes in row and column indices.
		Returns which ship was hit, otherwise 0.
		"""
		if(self.board[row][col] == "0"):
			self.board[row][col] = '*'
			return(0)
		elif(self.board[row][col] == '*' or self.board[row][col] == "X"):
			return(0)
		else:
			size = int(self.board[row][col])
			self.board[row][col] = 'X'
			return(size)

	def shipSunk(self, shipSize):
		"""
		Checks the board to see if a specific ship has been sunk.
		Takes in which ship to check if sunk.
		Returns whether the ship is sunk.
		"""
		sunk = False
		for i in range(self.rows):
			for j in range(self.columns):
				if self.board[i][j] == shipSize:
					sunk = True
		return(sunk)

	def gameLost(self):
		"""
		Checks if any ships are left unsunk.
		Returns whether there are any ships remaining on the board.
		"""
		lost = bool(1)
		for i in range(self.rows):
			for j in range(self.columns):
				if not(self.board[i][j] == "0" or self.board[i][j] == 'X' or self.board[i][j] == '*'):
					lost = bool(0)
		return(lost)

	# Prints the grid, showing ships and hits and misses
	def printPlayerView(self):
		"""Prints the player's own view of the board (i.e. can see ships)"""
		print("   ", end = '')
		for i in range(self.columns):
			char = chr(65+i)
			print(char, " ", end = '')

		print()

		for i in range(self.rows):
			print(i+1, " ", end = '')
			for j in range(self.columns):
				if self.board[i][j] == "0":
					print("~", " ", end = '')
				else:
					print(self.board[i][j], " ", end = '')
			print()

	# Prints the grid, showing only hits and misses
	def printOpponentView(self):
		"""Prints the opponent's view of the board (i.e. cannot see ships)"""
		print("   ", end = '')
		for i in range(self.columns):
			char = chr(65+i)
			print(char, " ", end = '')

		print()

		for i in range(self.rows):
			print(i+1, " ", end = '')
			for j in range(self.columns):
				if self.board[i][j] == 'X' or self.board[i][j] == '*':
					print(self.board[i][j], " ", end = '')
				else:
					print('~', " ", end = '')
			print()

	# Modifies a grid after a scan shot was declared
	def scanShot(self, scanType, row, col):
		"""
		ScanType is 0 for X shot, 1 for + shot and 2 for block shot. Row and Col correspond to the mid-point of each shot type.

		Examples:    X:  X X     +:  X    Block:  XXX
						  O         XOX           XOX
					     X X         X            XXX

		Note: X is a square revealed by the scan. O is the tile specified by row and col.
		Modifies the grid such that an empty tile is marked as a miss (*) and any revealed ship is un-marked and will still need to be fired at.
		"""

		# scan at middle
		if(self.board[row][col] == "0"):
			self.board[row][col] = '*'

		# X scan
		if scanType == 1:
			if (row != 0):
				if (col != 0):
					if (self.board[row-1][col-1] == "0"):
						self.board[row-1][col-1] = '*'
			if (row != 9):
				if (col != 0):
					if (self.board[row+1][col-1] == "0"):
						self.board[row+1][col-1] = '*'
			if (row != 0):
				if (col != 8):
					if (self.board[row-1][col+1] == "0"):
						self.board[row-1][col+1] = '*'
			if (row != 9):
				if (col != 8):
					if (self.board[row+1][col+1] == "0"):
						self.board[row+1][col+1] = '*'

		# + scan
		elif scanType == 2:
			if (col != 0):
				if (self.board[row][col-1] == "0"):
					self.board[row][col-1] = '*'
			if (col != 8):
				if (self.board[row][col+1] == "0"):
					self.board[row][col+1] = '*'
			if (row != 0):
				if (self.board[row-1][col] == "0"):
					self.board[row-1][col] = '*'
			if (row != 9):
				if (self.board[row+1][col] == "0"):
					self.board[row+1][col] = '*'
		# square scan, scanType == 3
		elif scanType == 3:
			if (row != 0):
				if (col != 0):
					if (self.board[row-1][col-1] == "0"):
						self.board[row-1][col-1] = '*'
			if (row != 9):
				if (col != 0):
					if (self.board[row+1][col-1] == "0"):
						self.board[row+1][col-1] = '*'
			if (row != 0):
				if (col != 8):
					if (self.board[row-1][col+1] == "0"):
						self.board[row-1][col+1] = '*'
			if (row != 9):
				if (col != 8):
					if (self.board[row+1][col+1] == "0"):
						self.board[row+1][col+1] = '*'
			if (col != 0):
				if (self.board[row][col-1] == "0"):
					self.board[row][col-1] = '*'
			if (col != 8):
				if (self.board[row][col+1] == "0"):
					self.board[row][col+1] = '*'
			if (row != 0):
				if (self.board[row-1][col] == "0"):
					self.board[row-1][col] = '*'
			if (row != 9):
				if (self.board[row+1][col] == "0"):
					self.board[row+1][col] = '*'
