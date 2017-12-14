import os, sys
parentDir = os.path.abspath('.')
sys.path.insert(0, parentDir)
import csv
from timeit import default_timer as timer
from classes.board import Board

def bfs(first_board):
	"""
	This algorithm searches and returns the shortest path 
	for any given board in Rush hour style. 
	"""

	#Start the timer for the algorithm
	start = timer()
	solutionFound = first_board.isSolution()
	#Create an empty list for the queue
	queue = []
	#Append the first board board as it originally is
	queue.append( first_board )
	print("")
	#Create a set for the visited boards
	visited = set()
	number_of_boards = 0

	#Check and add boards to the queue if solution has not been found yet
	while solutionFound == False:
		#Get the first element from the queue
		newSituation = queue.pop(0)

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
			elif (possibleBoard.__str__() not in visited):
				#1. add it to the queue 
				queue.append( possibleBoard )
				#2. add a string representation of it to the set of visited boards
				visitedAadd( possibleBoard.__str__() )

		visited.add( newSituation.__str__() )
		number_of_boards +=1
	#When algorithm finds a solution, end the timer
	end = timer()

	print("Runtime:",round(end-start,4))

	#PATH
	path = [possibleBoard]
	while possibleBoard.parent != 0:
		path.insert(0, possibleBoard.parent )
		possibleBoard = possibleBoard.parent



	#Visualize path
	def visualize_path():
		print(" ")
		print("Path to solution with length:", len(path) -1) #1 stap minder want begin bord telt niet mee
		sleep(2)
		print(" ")
		print("B E G I N")
		if len(path) <= 50:
			for board in path:
				board.print_board()
				print(" ")
				sleep(1)
		print("E N D")

	
	question = "Do you want a visualization of the shortest path? "

	yes = {'yes','y', 'ye', ''}
	no = {'no','n'}

	sys.stdout.write(question + " yes/no, your input: ")
	choice = input().lower()
	if choice in yes:
	   return visualize_path()
	elif choice in no:
	   return "Finished"
	else:
	   sys.stdout.write("Please respond with 'yes' or 'no'")



if __name__ == "__main__":
	filename = "boards/"+sys.argv[1]
	with open(filename):
		first_board = Board.load_from_file(filename)
	bfs(first_board)