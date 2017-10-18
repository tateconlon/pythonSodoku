import sodoku as s

class SodokuGame:
	"""A sodoku game, in charge of checking 
	the board and seeing if it has been completed"""

	def __init__(self, board_file):
		self.board_file = board_file
		self.start_puzzle = s.SodokuBoard(board_file).board
	
	def start(self):
		self.gameOver = False

		self.puzzle = []
		for i in range(len(self.start_puzzle)):
			self.puzzle.append([])
			for j in range(len(self.start_puzzle[i])):
				self.puzzle[i].append(self.start_puzzle[i][j])



	def check_win(self):
		for i in range(9):
			if (not self.__check_row(i) 
				or not self.__check_col(i)
				or not self.__check_square(i//3,i%3)):
				self.gameOver = False
				return

		self.gameOver = True
		return True

	def __check_row(self, rowIndex):
		return self.__check_block(self.puzzle[rowIndex])

	def __check_col(self, colIndex):
		return self.__check_block(
			[row[colIndex] for row in self.puzzle])

	def __check_square(self, row, col):
		return self.__check_block(
			[
				self.puzzle[r][c]
				for r in range(row * 3, (row + 1) * 3)
				for c in range(col * 3, (col + 1) * 3)
			]
			)

	def __check_block(self, block):
		return set(block) == set(range(1,10))
