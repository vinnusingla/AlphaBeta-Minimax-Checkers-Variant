import pygame,sys,os
from copy import deepcopy
from random import randint

##COLORS##
#             R    G    B 
WHITE    = (255, 255, 255)
BLUE     = (  0,   0, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLACK    = (  0,   0,   0)
GOLD     = (255, 215,   0)
FADE     = (160, 190, 255)

# Player types
HUMAN  = 0
BOT    = 1
RANDOM = 2 

#######################
def getColor(curColor):
	if(curColor == 'r'):
		curColor = RED
	else:
		curColor = BLUE
	return curColor

def getColorLiteral(x):
	if(x == RED):
		return 'r'
	else:
		return 'b'
########################

class Board:
	def __init__ (self):
		self.length = 9		#vertical
		self.width = 8		#horizontal
		self.matrix = self.newBoard(self.length,self.width) 

	def newBoard(self,l,w):
		matrix = [['.' for x in range(w)] for y in range(l)]
		for i in range(0,2):
			for j in range(0,w):
				matrix[i][j]='r'
		for i in range(l-2,l):
			for j in range(0,w):
				matrix[i][j]='b'
		return matrix

	def updateBoard(self,mat):
		board = mat

	def legalPos(self,cur):
		if -1<cur[0] and cur[0]<self.length and -1<cur[1] and cur[1]<self.width:
			return True
		else:
			return False

	def findLegalMoves(self,cur):
		ans = []
		curColor = self.matrix[cur[0]][cur[1]]

		if cur is not None:

			if(self.legalPos((cur[0]+1,cur[1]))):
				if(self.matrix[cur[0]+1][cur[1]] == '.'):
					ans.append((cur[0]+1,cur[1]))
				elif self.matrix[cur[0]+1][cur[1]] != curColor and self.legalPos((cur[0]+2,cur[1])) and \
				self.matrix[cur[0]+2][cur[1]]  == '.':
					ans.append((cur[0]+2,cur[1]))

			if(self.legalPos((cur[0]-1,cur[1]))):
				if(self.matrix[cur[0]-1][cur[1]]=='.'):
					ans.append((cur[0]-1,cur[1]))
				elif self.matrix[cur[0]-1][cur[1]] != curColor and self.legalPos((cur[0]-2,cur[1])) and \
				self.matrix[cur[0]-2][cur[1]] == '.':
					ans.append((cur[0]-2,cur[1]))

			if(self.legalPos((cur[0],cur[1]+1))):
				if(self.matrix[cur[0]][cur[1]+1]=='.'):
					ans.append((cur[0],cur[1]+1))
				elif self.matrix[cur[0]][cur[1]+1] != curColor and self.legalPos((cur[0],cur[1]+2)) and \
				self.matrix[cur[0]][cur[1]+2]=='.':
					ans.append((cur[0],cur[1]+2))

			if(self.legalPos((cur[0],cur[1]-1))):
				if(self.matrix[cur[0]][cur[1]-1]=='.'):
					ans.append((cur[0],cur[1]-1))
				elif self.matrix[cur[0]][cur[1]-1] != curColor and self.legalPos((cur[0],cur[1]-2)) and \
				self.matrix[cur[0]][cur[1]-2]=='.':
					ans.append((cur[0],cur[1]-2))

		return ans

	def findAllLegalMoves(self,color):
		color = getColorLiteral(color)
		moves=[]
		for i in range(0,self.length):
			for j in range(0,self.width):
				if(self.matrix[i][j] != '.'):
					if(self.matrix[i][j]==color):
						possibleActions = self.findLegalMoves((i,j))
						for k in range (0,len(possibleActions)):
							moves.append(((i,j),possibleActions[k]))
		return moves

	def isJump(self,pos1,pos2):
		if(abs(pos1[0]-pos2[0])<=1 and abs(pos1[1]-pos2[1])<=1):
			return (-1,-1)
		else:
			return ( (pos1[0]+pos2[0])/2 , (pos1[1]+pos2[1])/2 )

	def performMove(self,pos1,pos2):
		self.matrix[pos2[0]][pos2[1]] = self.matrix[pos1[0]][pos1[1]]
		self.matrix[pos1[0]][pos1[1]] = '.'
		jump = self.isJump(pos1,pos2)
		if  jump != (-1,-1):
			#it means a jump
			self.matrix[jump[0]][jump[1]] = self.matrix[pos2[0]][pos2[1]]

	def rollbackMove(self,pos1,pos2):
		self.matrix[pos2[0]][pos2[1]] = self.matrix[pos1[0]][pos1[1]]
		self.matrix[pos1[0]][pos1[1]] = None
		jump = self.isJump(pos1,pos2)
		if  jump != (-1,-1):
			#it means a jump
			if self.matrix[pos2[0]][pos2[1]] == 'r':
				self.matrix[jump[0]][jump[1]] = 'b'
			else:
				self.matrix[jump[0]][jump[1]] = 'r'

	def verticallySafe(self,pos):
		color = self.matrix[pos[0]][pos[1]]
		if (self.legalPos((pos[0],pos[1]+1)) and self.matrix[pos[0]][pos[1]+1] != '.' and \
			self.matrix[pos[0]][pos[1]+1] != color and self.legalPos((pos[0],pos[1]-1)) and\
			 self.matrix[pos[0]][pos[1]-1] == '.'):
			return -5
		elif (self.legalPos((pos[0],pos[1]-1)) and self.matrix[pos[0]][pos[1]-1] != '.' and \
			self.matrix[pos[0]][pos[1]-1] != color and self.legalPos((pos[0],pos[1]+1)) and\
			 self.matrix[pos[0]][pos[1]+1] == '.'):
			return -5
		else:
			return 0

	def horizontallySafe(self,pos):
		color = self.matrix[pos[0]][pos[1]]
		if (self.legalPos((pos[0]+1,pos[1])) and self.matrix[pos[0]+1][pos[1]] != '.' and \
			self.matrix[pos[0]+1][pos[1]] != color and self.legalPos((pos[0]-1,pos[1])) and\
			 self.matrix[pos[0]-1][pos[1]] == '.'):
			return -5
		elif (self.legalPos((pos[0]-1,pos[1])) and self.matrix[pos[0]-1][pos[1]] != '.' and \
			self.matrix[pos[0]-1][pos[1]] != color and self.legalPos((pos[0]+1,pos[1])) and\
			 self.matrix[pos[0]+1][pos[1]] == '.'):
			return -5
		else:
			return 0

	def isSafe(self,pos):
		if(self.horizontallySafe(pos) == 0 and self.verticallySafe(pos) == 0):
			return True
			 

class Graphics:
	def __init__(self): 
		self.fps = 60
		self.clock = pygame.time.Clock()
		self.length = 720
		self.width = 640
		self.screen = pygame.display.set_mode((self.length, self.width))
		self.background = pygame.image.load('resources/board98.png')
		self.square_size = self.length / 9
		self.pLength = 40
		self.pWidth = 30
		self.caption = "Turtle War" 
		self.img = pygame.image.load("resources/turtle.png")
		self.redTurtle = pygame.Surface((self.pWidth,self.pLength))
		self.redTurtle.blit(self.img,(0,0),(self.pWidth,self.pLength,self.pWidth,self.pLength))
		self.redTurtle.set_colorkey((255,255,255))
		self.blueTurtle = pygame.Surface((self.pWidth,self.pLength))
		self.blueTurtle.blit(self.img,(0,0),(self.pWidth,0,self.pWidth,self.pLength))
		self.blueTurtle.set_colorkey((255,255,255))

	def setup_window(self):
		pygame.init()
		pygame.display.set_caption(self.caption)

	def updateDisplay(self,board,current,legalMoves=None):
		self.screen.blit(self.background, (0,0))
		self.highlightSquares(legalMoves,current)
		self.drawBoardPieces(board)
		pygame.display.update()
		self.clock.tick(self.fps)

	def drawBoardPieces(self, board):
		for x in range(0,board.length):
			for y in range(0,board.width):
				if board.matrix[x][y] != '.':
					if board.matrix[x][y] == 'r':
						self.screen.blit(self.redTurtle,self.pixelCoords((x,y)))
					else:
						self.screen.blit(self.blueTurtle,self.pixelCoords((x,y)))

	def highlightSquares(self, squares, origin):
		for square in squares:
			pygame.draw.rect(self.screen, FADE, (square[0] * self.square_size, square[1] * self.square_size, self.square_size, self.square_size))	

		# if origin != None:
		# 	origin=origin.pos
		# 	pygame.draw.rect(self.screen, FADE, (origin[0] * self.square_size, origin[1] * self.square_size, self.square_size, self.square_size))

	def pixelCoords(self, board_coords):
		return (board_coords[0] * self.square_size + (self.square_size-self.pWidth)/2 , board_coords[1] * self.square_size \
			+ (self.square_size-self.pLength)/2 )

	def board_coords(self,(pixel_x, pixel_y)):
		return (pixel_x / self.square_size, pixel_y / self.square_size)	

class Bot:
	def __init__(self,color1,color2):
		self.color = color1
		self.oppColor = color2
		self.alpha = -1000000000
		self.beta = 1000000000
		self.mvct = 0
		self.ct = 0

	def alphaBetaSearch(self,board,cutoff):
		moves = board.findAllLegalMoves(self.color)
		state = board
		maxxy = -100000000
		maxAction = None
		self.mvct = self.mvct + len(moves)
		self.ct = self.ct + 1
		for i in range(0,len(moves)):
			pos1 = moves[i][0]
			pos2 = moves[i][1]
			#perform move
			state.performMove(pos1,pos2)
			#call max func
			val = self.maxValue(state,cutoff)
			# print("val = ",val)
			if(val > maxxy):
				maxxy = val
				maxAction = moves[i]
			#rollback move
			state.rollbackMove(pos2,pos1)
		print("max action = ",maxAction)
		return maxAction

	def maxValue(self,board,cutoff):
		if(self.terminalTest(board,cutoff)):
			return self.eval(board)
		state = board
		maxxy = -100000000
		moves = board.findAllLegalMoves(self.oppColor)
		self.mvct = self.mvct + len(moves)
		self.ct = self.ct + 1
		for i in range(0,len(moves)):
			pos1 = moves[i][0]
			pos2 = moves[i][1]
			#perform move
			state.performMove(pos1,pos2)
			#call min func
			maxxy = max(maxxy , self.minValue(state,cutoff-1))
			if(maxxy >= self.beta):
				return maxxy
			alpha = max(self.alpha,maxxy)
			#rollback move
			state.rollbackMove(pos2,pos1)
		return maxxy

	def minValue(self,board,cutoff):
		if(self.terminalTest(board,cutoff)):
			return self.eval(board)
		state = board
		minny = 100000000
		moves = board.findAllLegalMoves(self.oppColor)
		self.mvct = self.mvct + len(moves)
		self.ct = self.ct + 1
		for i in range(0,len(moves)):
			pos1 = moves[i][0]
			pos2 = moves[i][1]
			#perform move
			state.performMove(pos1,pos2)
			#call min func
			minny = min(minny , self.maxValue(state,cutoff-1))
			if(minny <= self.alpha):
				return minny
			beta = min(self.beta,minny)
			#rollback move
			state.rollbackMove(pos2,pos1)
		return minny

	def eval(self,board):
		ans=0
		#player count
		for i in range(0,board.length):
			for j in range(0,board.width):
				if(board.matrix[i][j] != '.'):
					if(getColor(board.matrix[i][j]) == self.color):
						ans=ans+10
					else:
						ans=ans-10

		#defenses
		for i in range(0,board.length):
			for j in range(0,board.width):
				if(board.matrix[i][j] != '.'):
					if(getColor(board.matrix[i][j]) == self.color):
						ans = ans + board.verticallySafe((i,j))
						ans = ans + board.horizontallySafe((i,j))

		#attack1 we aren't safe after attacking attack2 we are safe after attacking
		move = board.findAllLegalMoves(self.color)
		for i in range (0,len(move)):
			pos1=move[i][0]
			pos2=move[i][1]
			if(board.isJump(pos1,pos2)):
				board.performMove(pos1,pos2)
				if board.isSafe(pos2):
					ans = ans + 8
				else:
					ans = ans + 2
				board.rollbackMove(pos2,pos1) 



		return ans

	def terminalTest(self,board,cutoff):
		if (cutoff == 0):
			return True
		blue = False
		red = False
		for i in range(0,board.length):
			for j in range(0,board.width):
				if(board.matrix[i][j] != False):
					if(getColor(board.matrix[i][j]) == BLUE):
						blue = True
					else:
						red = True
		if(blue == False or red == False):
			return True
		else:
			return False

class Game:
	def __init__(self):
		self.graphics = Graphics()
		self.board = Board()
		self.player = {}
		self.player[BLUE] = HUMAN
		self.player[RED] = BOT
		self.turn = BLUE
		self.selectedTile = None # a board location.
		self.legalMoves = []
		self.turnStep = 1
		self.bot = {}
		self.finished = False
		if (self.player[BLUE] == BOT):
			self.bot[BLUE] = Bot(BLUE,RED)
		if (self.player[RED] == BOT):
			self.bot[RED] = Bot(RED,BLUE)

	def setup(self):
		self.graphics.setup_window()

	def event_loop(self):
		self.mouse_pos = self.graphics.board_coords(pygame.mouse.get_pos()) # what square is the mouse in?

		if (self.finished == True):
			if(self.turn == RED):
				self.turn = BLUE
			else:
				self.turn = RED
			if(len(self.board.findAllLegalMoves(self.turn)) == 0):
				if(self.turn == RED):
					print("BLUE player wins")
				else:
					print ("RED player wins")
				self.terminate_game()
			self.finished = False

		if(self.player[self.turn] == RANDOM):
			moves = self.board.findAllLegalMoves(self.turn)
			move = moves[randint(0,len(moves)-1)]
			self.board.performMove(move[0],move[1])
			self.finished = True
					
		elif(self.player[self.turn] == BOT):
			# print("bot's turn")
			move = self.bot[self.turn].alphaBetaSearch(self.board,2)
			# print("move = ",move)
			self.board.performMove(move[0],move[1])
			self.finished = True


		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				if(self.player[RED] == BOT):
					print("Average Branching Factor = ",self.bot[RED].mvct/self.bot[RED].ct)

				self.terminate_game()

			elif event.type == pygame.MOUSEBUTTONDOWN:
				print(self.mouse_pos)
				if self.player[self.turn] == HUMAN:
					# print("Human turn")
					if(self.turnStep==1):
						self.selectedTile = self.board.matrix[self.mouse_pos[0]][self.mouse_pos[1]]
						self.legalMoves = []
						if(self.selectedTile == '.' or getColor(self.selectedTile) != self.turn):
							self.selectedTile = None
						elif(getColor(self.selectedTile) == self.turn):
							self.legalMoves = self.board.findLegalMoves(self.mouse_pos)
							self.turnStep = 2
							self.oldpos = self.mouse_pos
						self.finished = False
					else:
						validMove = False
						# print(self.legalMoves)
						for i in self.legalMoves:
							# print(i)
							if( i == self.mouse_pos):
								validMove = True
								break
						# print("validMove = ",validMove)
						if(validMove):
							self.board.matrix[self.mouse_pos[0]][self.mouse_pos[1]] = self.selectedTile
							self.board.matrix[self.oldpos[0]][self.oldpos[1]] = '.'
							jump = self.board.isJump(self.mouse_pos,self.oldpos)
							if  jump != (-1,-1):
								#it means a jump
								self.board.matrix[jump[0]][jump[1]] = getColorLiteral(self.turn)
							self.finished = True
						self.turnStep=1
						self.selectedTile = None
						self.legalMoves = []


	def update(self):
		self.graphics.updateDisplay(self.board, self.selectedTile, self.legalMoves)

	def terminate_game(self):
		pygame.quit()
		exit(0)

	def main(self):
		self.setup()
		while True: # main game loop
			self.event_loop()
			self.update()

#########################################################################

mat = ["rrrrrrrr",
      "rrrrrrrr",
      "........",
      "........",
      "........",
      "......b.",
      "........",
      "bbbbbb.b",
      "bbbbbbbb"]
g=Game()
# g.board.updateBoard(mat)
g.main()