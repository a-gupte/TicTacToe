from tkinter import *
import constant

class Grid(Tk):
	def __init__(self):
		super().__init__()

		# Frame to Display Player Information
		self.player_frame = Frame(self)
		self.player_frame.pack()
		self.player_info = Label(self.player_frame, text = f'HUMAN:{constant.HUMAN}\nBOT:{constant.BOT}')
		self.player_info.pack()


		# Frame to display messages
		self.display_frame = Frame(self)
		self.display_frame.pack(side = BOTTOM)

		self.status_info = Label(self.display_frame, text='')
		self.status_info.pack()

		# The board
		self.board_frame = Frame(self)

		# Variables to get human input
		self.input_x = IntVar()
		self.input_y = IntVar()

		# Buttons to represent cells of the TicTacToe grid
		for i in range(3):
			self.board_frame.columnconfigure(i, pad=10)
			self.board_frame.rowconfigure(i, pad=10)

		self.cells = []
		for i in range(3):
			self.cells.append([])
			for j in range(3):
				self.cells[i].append(Button(self.board_frame, text='', height = constant.BUTTON_HEIGHT, width = constant.BUTTON_WIDTH))

		for i in range(3):
			for j in range(3):
				self.cells[i][j].grid(row=i, column = j)
				self.cells[i][j]['command'] = lambda x = i, y= j: self.get_input(x, y)

		self.board_frame.pack()

	def display_message(self, message):
		'''
		Function to display status of the game
		Takes 1 argument
			message: str: Message to be displayed
		Returns None
		'''
		self.status_info['text'] = message

	def get_input(self, i, j):
		'''
		Function to get human input from button clicks
		Takes 2 arguments
			i: int: Row number
			j: int: Column number
		Returns None
		'''
		self.input_x.set(i)
		self.input_y.set(j)

	def update_grid(self, x, y, player):
		'''
		Function to update the grid UI to reflect changes
		Takes 3 argument
			x: int: Row number
			y: int: Column number
			player: player that made the move
		Returns None
		'''
		self.cells[x][y]['text'] = player
		self.cells[x][y]['state'] = DISABLED