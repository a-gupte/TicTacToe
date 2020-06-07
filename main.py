import random
import constant
import tkinter
from ui import Grid

class Game:
	def __init__(self):
		self.board = [[' ' for j in range(3)] for i in range(3)]
		self.game_status = 'ongoing'
		self.next_player = None
		self.memory = {}
		self.toss()

		self.grid = Grid()

	def toss(self):
		'''
		Function that uniformly decides the first player at random.
		Takes 0 arguments.
		Returns None.
		'''
		self.next_player = random.choice([constant.HUMAN, constant.BOT])

	def display_gameover(self):
		'''
		Display message when game is over.
		Takes 0 arguments.
		Returns None.
		'''
		if self.game_status == constant.HUMAN:
			self.grid.display_message("Congratulations, you won!")
		elif self.game_status == constant.BOT:
			self.grid.display_message("Sorry, you lost")
		else:
			self.grid.display_message("That was close! You tied")
		self.grid.wait_window()

	def input_move(self):
		'''
		Takes input from human player.
		Takes 0 arguments.
		Returns None.
		'''
		self.grid.wait_variable(self.grid.input_x)
		x = self.grid.input_x.get()
		y = self.grid.input_y.get()

		try:
			cell = self.board[x][y]
		except IndexError:
			self.grid.display_message("Invalid move, please play again")
			self.input_move()
			return
		# Check if valid move
		if cell != ' ':
			self.grid.display_message("Invalid move, please play again")
			self.input_move()
			return

		self.update_board_and_grid(x, y, constant.HUMAN)

	def update_board_and_grid(self, x, y, player):
		'''
		Function to get human input from button clicks.
		Takes 2 arguments.
			i: int: Row number
			j: int: Column number
		Returns None.
		'''
		self.board[x][y] = player
		self.grid.update_grid(x, y, player)

	def play_best_move(self):
		'''
		Determines and plays best move for the bot player using minimax algorithm.
		Takes 0 arguments.
		Returns None.
		'''
		best_score = float('-inf')
		best_move = None
		for x in range(3):
			for y in range(3):
				if self.board[x][y] == ' ':
					self.board[x][y] = constant.BOT
					score = self.minmax(constant.HUMAN)
					if score>best_score:
						best_score = score
						best_move = x, y
					self.board[x][y] = ' '
		best_x, best_y = best_move
		self.update_board_and_grid(best_x, best_y, constant.BOT)

	def is_filled(self):
		'''
		Checks if the board is filled.
		Returns True or False.
		'''
		for i in range(3):
			for j in range(3):
				if self.board[i][j] == ' ':
					return False
		return True

	def minmax(self, next_player, depth = 0):
		'''
		Implements minimax algorithm to determine the next best move for the bot player.
		Takes 2 arguments:
			next_player: str: 'x' or 'o'
			depth: int: recursion depth
		Returns the best possible score earned.
		'''
		if self.in_memory(next_player):
			return self.get_memory(next_player)

		if self.has_won(constant.HUMAN):
			return -constant.MAXSCORE + depth
		elif self.has_won(constant.BOT):
			return constant.MAXSCORE - depth
		elif self.is_filled():
			return 0 - depth

		# If next player is bot, try to maximize score
		if next_player == constant.BOT:
			best_score = float('-inf')
			for x in range(3):
				for y in range(3):
					if self.board[x][y] == ' ':
						self.board[x][y] = constant.BOT
						best_score = max(best_score, self.minmax(constant.HUMAN, depth + 1))
						self.board[x][y] = ' '

		# If next player is human, try to minimize score
		elif next_player == constant.HUMAN:
			best_score = float('inf')
			for x in range(3):
				for y in range(3):
					if self.board[x][y] == ' ':
						self.board[x][y] = constant.HUMAN
						best_score = min(best_score, self.minmax(constant.BOT, depth +1))
						self.board[x][y] = ' '
		self.memoize(next_player, best_score)
		return best_score

	def in_memory(self, next_player):
		'''
		Returns if the current state of the game has been seen before or not.
		Takes 1 argument:
			next_player: str: 'x' or 'o'
		Returns True or False.
		'''
		return self.str_rep(next_player) in self.memory:

	def get_memory(self, next_player):
		'''
		Takes 1 argument:
			next_player: str: 'x' or 'o'
		Returns best possible score achievable given the current state of the game.
		'''
		return self.memory[self.str_rep(next_player)]

	def str_rep(self, next_player):
		'''
		Computes and returns a string representation of the current state of the game so that it can be memoized.
		Takes 1 arguments:
			next_player: str: 'x' or 'o'
		Returns the string representation.
		'''
		result = next_player
		for row in self.board:
			for cell in row:
				result = result + cell
		return result

	def memoize(self, next_player, best_score):
		'''
		Stores the best possible score achievable given the current state of the game. 
		Takes 2 arguments:
			next_player: str: 'x' or 'o'
			best_score: int
		Returns None.
		'''
		self.memory[self.str_rep(next_player)] = best_score


	def has_won(self, player):
		'''
		Takes 1 argument
			player: str: 'x' or 'o'
		Returns True if player has won, False otherwise
		'''
		win = [player for _ in range(3)]
		# Rows
		for row in self.board: 
			if row == win:
				return True

		# Columns
		for col in [[self.board[i][j] for i in range(3)] for j in range(3)]:
			if col == win:
				return True

		# Diagonals
		if [self.board[i][i] for i in range(3)] == win:
			return True
		if [self.board[i][2-i] for i in range(3)] == win:
			return True
		return False

	def update_game_status(self):
		'''
		Updates the status of the game to one of 'ongoing', 'draw', 'x', 'o'.
		Takes 0 arguments.
		Returns None.
		'''
		for player in [constant.BOT, constant.HUMAN]:
			if self.has_won(player):
				self.game_status = player
				return

		for i in range(3):
			for j in range(3):
				if self.board[i][j] == ' ':
					self.game_status = 'ongoing'
					return

		self.game_status = 'draw'

	def display_board(self):
		'''
		Displays the status of the game.
		Takes 0 arguments.
		Returns None.
		'''
		self.grid.display_message(f"Next player : {self.next_player} Game status : {self.game_status}")

	def start(self):
		'''
		Starts the game, checks if the game is over, transfers control to the appropraite functions to
			Take human input
			Determine and play best move for bot
			Update the TicTacToe board
			Display the current status of the game.
		'''
		if self.next_player == constant.HUMAN:
			self.grid.display_message("You get to start!")
		else:
			self.grid.display_message("I'm thinking")
		while True:
			if self.game_status != 'ongoing':
				self.display_gameover()
				break

			next_player = self.next_player
			if next_player == constant.HUMAN:
				self.input_move()
				self.next_player = constant.BOT
			else:
				self.play_best_move()
				self.next_player = constant.HUMAN

			self.update_game_status()
			self.display_board()

game = Game()
game.start()