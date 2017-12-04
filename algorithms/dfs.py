import os, sys
parentDir = os.path.abspath('.')
sys.path.insert(0, parentDir)
import csv
from timeit import default_timer as timer
from classes.board import Board

def dfs(first_board):

	start = timer()
	solutionFound = first_board.isSolution()
	stack = []
	stack.append( first_board )
	print("")
	print("First Board:")
	visited = set()
	number_of_boards = 0

	while solutionFound == False and stack != []:
		newSituation = stack.pop(-1)
		visited.add( newSituation.__str__() )

		if number_of_boards%5000 == 0:
			print("")
			newSituation.print_board()

		for possibleBoard in newSituation.possibleBoards():
			
			if possibleBoard.isSolution() == True:
				print(" ")
				print("Final:")
				possibleBoard.print_board()
				print("WINWINWIN")
				solutionFound = True
				break

			elif ( possibleBoard.__str__() not in visited ):
				stack.append( possibleBoard )
				visited.add( possibleBoard.__str__() )

		number_of_boards +=1

	end = timer()


	if round(end-start,4) < 20:
		print("Runtime:",round(end-start,4), "aka VERY FAST, GASSSS")	
	else:
		print("Runtime:",round(end-start,4))


	#PATH
	path = [possibleBoard.__str__()]
	while possibleBoard.parent != 0:
		path.insert(0, possibleBoard.parent.__str__() )
		possibleBoard = possibleBoard.parent

	print(path)
	print("Path to solution with length:", len(path)-1) #voor begin bord, is geen stap


if __name__ == "__main__":
	filename = "boards/"+sys.argv[1]
	with open(filename):
		first_board = Board.load_from_file(filename)
	dfs(first_board)