import sys
sys.path.append("/Users/Drea/Desktop/Rush/")
import csv
from timeit import default_timer as timer
from classes.board import Board

def bfs(first_board):


	#first_board.print_board()
	

	start = timer()
	solutionFound = first_board.isSolution()
	queue = []
	queue.append( first_board )
	print("")
	print("First Board:")
	first_board.print_board()
	visited = set()
	layer = 0
	while solutionFound == False:
		newSituation = queue.pop(-1)
		if layer%5000 == 0:
			print("")
			print("Progress:")
			newSituation.print_board()
		for possibleBoard in newSituation.possibleBoards():
			# if len(queue) > 100000:
			# 	print("Queue length critical")
			# 	solutionFound = True
			# 	break
			if possibleBoard.isSolution() == True:
				print(" ")
				print("Final:")
				possibleBoard.print_board()
				print("WINWINWIN")
				solutionFound = True
				break
			elif (possibleBoard.__str__() not in visited):
				queue.append( possibleBoard )
				visited.add( possibleBoard.__str__() )

		visited.add( newSituation.__str__() )
		layer +=1

	end = timer()


	if round(end-start,4) < 20:
		print("Runtime:",round(end-start,4), "aka VERY FAST, GASSSS")	
	else:
		print("Runtime:",round(end-start,4))



if __name__ == "__main__":
	filename = "boards/"+sys.argv[1]
	with open(filename):
		first_board = Board.load_from_file(filename)
	bfs(first_board)