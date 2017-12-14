import os, sys
parentDir = os.path.abspath('.')
sys.path.insert(0, parentDir)
import csv
from timeit import default_timer as timer
from classes.board import Board
import random

def random_search(first_board):
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

	#Check boards if solution has not been found yet
	while solutionFound == False and stack != []:
		#shuffle possible boards
		random.shuffle(stack)
		#Get the top node from the stack
		newSituation = stack.pop(-1)
		#empty stack to make next choice completely random
		stack = []

		#Print the number of visited boards when searching for the solution every 100 boards
		if number_of_boards%100 == 0:
			print("Visited boards: ", number_of_boards)

		#Check if the current board is the final (solution) one, when this is true break the algorithm
		for possibleBoard in newSituation.possibleBoards():
			
			if possibleBoard.isSolution() == True:
				print(" ")
				print("S O L U T I O N   F O U N D")
				solutionFound = True
				break
			#If current board is not the final one, append to stack
			else:
				stack.append( possibleBoard )

		number_of_boards +=1

	#When algorithm finds a solution, end the timer
	end = timer()

	#Print the runtime of the algorithm
	print("Runtime:",round(end-start,4))


	#PATH
	path = [possibleBoard.__str__()]
	while possibleBoard.parent != 0:
		path.insert(0, possibleBoard.parent.__str__() )
		possibleBoard = possibleBoard.parent
		
	print("Path to solution with length:", len(path)-1) #voor begin bord, is geen stap


if __name__ == "__main__":
	filename = "boards/"+sys.argv[1]
	with open(filename):
		first_board = Board.load_from_file(filename)
	random_search(first_board)


