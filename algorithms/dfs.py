import os, sys
parentDir = os.path.abspath('.')
sys.path.insert(0, parentDir)
import csv
from timeit import default_timer as timer
from classes.board import Board
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

def dfs(first_board):
	"""
	This algorithm searches and returns the path to the solution
	for any given board in Rush hour style. 
	"""

	#Start the timer for the algorithm
	start = timer()
	solutionFound = first_board.isSolution()
	#Create an empty list for the stack
	stack = []

	#Append the first board board as it originally is
	stack.append( first_board )
	print("")

	#Create a set for the visited boards
	visited = set()
	number_of_boards = 0

	def progress(depth):
		print('\r',"Visited boards: ", number_of_boards, "   Depth: ", depth, end="", flush=True)

	#Check and add boards to the stack if solution has not been found yet
	while solutionFound == False and stack != []:
		
		#Get the top node from the stack
		newSituation = stack.pop(-1)
		visited.add( (newSituation.__str__(), newSituation.layer) )

		#Print the number of visited boards when searching for the solution every 1000 boards
		if number_of_boards%1000 == 0 and number_of_boards > 0:
			progress(newSituation.layer)

		for possibleBoard in newSituation.possibleBoards():
			
			#Check if the current board is the final (solution) one, when this is true break the algorithm
			if possibleBoard.isSolution() == True:
				print(" ")
				print("S O L U T I O N   F O U N D")
				solutionFound = True
				break
			
			#If current board is not the final one: 
			elif newSituation.layer < 40:
				if ( (possibleBoard.__str__(),possibleBoard.layer ) not in visited ):
				
					#1. add it to the stack
					stack.append( possibleBoard )
					
					#2. add a string representation of it to the set of visited boards
					visited.add( (possibleBoard.__str__(), possibleBoard.layer) )

		number_of_boards +=1
	
	if possibleBoard.isSolution() == False:
		print(" ")
		print("N O   S O L U T I O N   F O U N D")

	#When algorithm finds a solution, end the timer
	end = timer()

	#PATH
	path = [possibleBoard, possibleBoard.setFinishingState()]
	while possibleBoard.parent != 0 and possibleBoard.__str__() != first_board.__str__():
		path.insert(0, possibleBoard.parent )
		possibleBoard = possibleBoard.parent

	print("Runtime:",round(end-start,4))
	print("It takes ", len(path) -2, " steps to solve this game.") #1 step less because starting point and end point doesn't count


	#create data array suitable for the visualization
	boards = [x.transform() for x in path]

	def visualize():

		fig = plt.figure()
		plt.axis('off')

		size = len(possibleBoard.make_board()) #get height/width of board
		board_init = [[0]*(size) for i in range((size))]

		im=plt.imshow(boards[0], cmap=plt.get_cmap("nipy_spectral_r"))

		# initialization function: plot the background of each frame
		def init():
			im.set_array(board_init)
			return im,

		# animation function.  This is called sequentially
		def animate(i):
			a=boards[i]    # exponential decay of the values
			im.set_array(a)
			return im,

		anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(boards), interval=200, blit=True, repeat=False)

		plt.show()


	question = "Do you want a visualization of the shortest path? (we don't recommend it, when the path is > 100) "

	yes = {'yes','y', 'ye', ''}
	no = {'no','n'}

	sys.stdout.write(question + " yes/no, your input: ")
	choice = input().lower()
	if choice in yes:
	   return visualize()
	elif choice in no:
	   return "Finished"
	else:
	   sys.stdout.write("Please respond with 'yes' or 'no'")


if __name__ == "__main__":
	filename = "boards/"+sys.argv[1]
	
	#Open the beginnen csv-file board (the original board)
	with open(filename):
		first_board = Board.load_from_file(filename)
	dfs(first_board)


