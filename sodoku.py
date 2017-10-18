try:
	#python2 uppercase T
	from Tkinter import Tk
except ImportError:
	#python3 lowercase t
	from tkinter import Tk

import argparse
import sodokugame as sgame
import sodokuui as sui
BOARDS = ['debug', 'noob', 'l33t', 'error'] #Soduku board types

class SudokuError(Exception):
	"""An application specific error"""
	pass

class SodokuBoard(object):
	"""Sudoku Board representation"""

	def __init__(self, board_file):
		self.board = self.__create_board(board_file)

	def __create_board(self, board_file):
		"""creates a matrix (via list of lists) from the .sudoku board file"""

		with open(board_file, "r") as f:
			data = f.readlines()
		board = [list(line.strip()) for line in data]
		
		if len(board) != 9:
			raise SudokuError("9 lines are needed for a sudoku board, not {0}".format(len(board)))

		for row in board:
			if len(row) != 9:
				raise SudokuError("9 entries are needed per sudoku board, not {0}".format(len(row)))
			for i, c in enumerate(row):
				if not c.isdigit():
					raise SudokuError("cell entry must be a digit, not {0}".format(c))
				row[i] = int(c)
		return board

def main():
	board_name = parse_arguments()

	game = sgame.SodokuGame("{0}.sodoku".format(board_name))
	game.start()

	root = Tk()
	sui.SodokuUI(root, game)
	root.geometry("{0}x{1}".format(sui.WIDTH, sui.HEIGHT + 40))
	root.mainloop()


def parse_arguments():
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument("--board",
							help="Desired board name",
							type=str,
							choices=BOARDS,
							required=True)

	args = vars(arg_parser.parse_args()) #returns dict {"name": val}

	return args['board']

if __name__ == "__main__":
	main()