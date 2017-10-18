try:
	#python2 uppercase T
	from Tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM
except ImportError:
	#python3 lowercase t
	from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

MARGIN = 20 #Pixels around the board
SIDE = 50 #width of every board cell
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9

class SodokuUI(Frame):
	"""The Tkinter UI responsible for drawing sodoku boards and accepting user input"""
	def __init__(self, parent, game):
		self.game = game
		self.parent = parent
		Frame.__init__(self, parent)

		self.row, self.col = 0, 0
		self.__initUI()

	def __initUI(self):
		self.parent.title("Soduku") #title of parent window
		self.pack(fill=BOTH, expand=1)
		self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
		self.canvas.pack(fill=BOTH, side=TOP)
		clear_button = Button(self, text="Clear answers", command=self.__clear_answers)
		clear_button.pack(fill=BOTH, side=BOTTOM)

		self.__draw_puzzle()

		self.canvas.bind("<Button-1>", self.__cell_clicked) #sends x, y coordinates of left mouse click to self.__cell_clicked
		self.canvas.bind("<Key>", self.__key_pressed) #sends key pressed to self.__key_pressed  

	def __draw_grid(self):
		"""
		Draws grid with blue lines divided into 3x3 squares by grey lines
		"""
		for i in range(10):
			color, dash, thickness = ("grey", None, 2) if i%3 == 0 else ("grey", (1,) , 1)

			x0 = MARGIN
			x1 = WIDTH - MARGIN
			y0 = MARGIN + i * SIDE
			y1 = MARGIN + i * SIDE

			self.canvas.create_line(x0, y0, x1, y1, dash=dash, fill=color, width=thickness)

			x0 = MARGIN + i * SIDE
			x1 = MARGIN + i * SIDE
			y0 = MARGIN
			y1 = HEIGHT - MARGIN

			self.canvas.create_line(x0, y0, x1, y1, dash=dash, fill=color, width=thickness) 

	def __draw_puzzle(self):
		"""
		Draws the numbers on the puzzle
		"""
		self.canvas.delete("numbers") #deletes everything tagged numbers
		for i in range(9):
			for j in range(9):
				answer = self.game.puzzle[i][j]
				if answer != 0:
					x = MARGIN + (j+0.5) * SIDE
					y = MARGIN + (i+0.5) * SIDE
					if answer == self.game.start_puzzle[i][j]:
						self.canvas.create_rectangle(x - SIDE/2, y - SIDE/2, x + SIDE/2, y + SIDE/2, fill="grey")
						self.canvas.create_text(x, y, text=answer, tags="numbers", fill="white")
					else:
						self.canvas.create_rectangle(x - SIDE/2, y - SIDE/2, x + SIDE/2, y + SIDE/2, fill="seashell")
						self.canvas.create_text(x, y, text=answer, tags="numbers", fill="black")

		self.__draw_grid()

	def __clear_answers(self):
		self.game.start()
		self.canvas.delete("victory")
		self.__draw_puzzle()

	def __cell_clicked(self, event):
		'''
		event param gives us the x & y coordinates
		'''
		if self.game.gameOver:
			return #do nothing

		x, y = event.x, event.y
		if(MARGIN < x < WIDTH-MARGIN and MARGIN < y < HEIGHT - MARGIN):
			self.canvas.focus_set()

			r, c = (event.y - MARGIN) // SIDE, (event.x - MARGIN) // SIDE

			if((self.row == r and self.col == c)
				or self.game.start_puzzle[r][c] != 0):
				self.row, self.col = -1, -1 #if same cell reselected or cell part of original board, deselect
			else:
				self.row, self.col = r, c
		else:
			self.row, self.col = -1, -1

		self.__draw_cursor()

	def __draw_cursor(self):
		'''
		Draws cursor around selected box
		'''
		self.canvas.delete("cursor")

		if self.row == -1 or self.col == -1:
			return

		x0 = MARGIN + self.col * SIDE
		x1 = MARGIN + (self.col + 1) * SIDE
		y0 = MARGIN + self.row * SIDE
		y1 = MARGIN + (self.row + 1) * SIDE

		self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="cursor")

	def __key_pressed(self, event):
		if self.game.gameOver:
			return
		if self.row != -1 and self.col != -1 and event.char in "0123456789" and event.char != '':
			self.game.puzzle[self.row][self.col] = int(event.char)
			self.__draw_puzzle()
			if self.game.check_win():
				self.__draw_victory()

	def __draw_victory(self):
		x0 = y0 = MARGIN + SIDE * 2
		x1 = y1 = MARGIN + SIDE * 7
		self.canvas.create_oval(x0, y0, x1, y1, fill="dark orange", outline="orange", tags="victory")

		x = y = MARGIN + SIDE * 4.5
		self.canvas.create_text(x, y, text="You win!", font=("Arial", 32), fill="white", tags="victory")

