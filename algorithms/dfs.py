import os, sys
parentDir = os.path.abspath('.')
sys.path.insert(0, parentDir)
import csv
from timeit import default_timer as timer
from classes.board import Board

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

	#Check and add boards to the stack if solution has not been found yet
	while solutionFound == False and stack != []:
		#Get the top node from the stack
		newSituation = stack.pop(-1)
		visited.add( newSituation.__str__() )

		#Print the number of visited boards when searching for the solution every 1000 boards
		if number_of_boards%1000 == 0:
			print("Progress: ", number_of_boards, " boards visited")

		for possibleBoard in newSituation.possibleBoards():
			#Check if the current board is the final (solution) one, when this is true break the algorithm
			if possibleBoard.isSolution() == True:
				print(" ")
				print("S O L U T I O N   F O U N D")
				solutionFound = True
				break
			#If current board is not the final one: 
			elif ( possibleBoard.__str__() not in visited ):
				#1. add it to the stack
				stack.append( possibleBoard )
				#2. add a string representation of it to the set of visited boards
				visited.add( possibleBoard.__str__() )

		number_of_boards +=1
	#When algorithm finds a solution, end the timer
	end = timer()

	#Print the runtime of the algorithm
	print("Runtime:",round(end-start,4))


	#Path from original state of original board to solution
	path = [possibleBoard.__str__()]
	#While the current board has a parent, insert a string representstion of it to the path
	while possibleBoard.parent != 0:
		path.insert(0, possibleBoard.parent.__str__() )
		possibleBoard = possibleBoard.parent
	
	#Print the lenght of the path -1 because the orignal (beginning) board doesn't count as path to solution
	print("Path to solution with length:", len(path)-1) 


if __name__ == "__main__":
	filename = "boards/"+sys.argv[1]
	#Open the beginnen csv-file board (the original board)
	with open(filename):
		first_board = Board.load_from_file(filename)
	dfs(first_board)