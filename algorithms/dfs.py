from board import Board
from timeit import default_timer as timer

def dfs():
	start = timer()
	solutionFound = Board.isSolution(Board.grid)
	stack = [(Board.grid,0)]
	visited = []

	while solutionFound == False:
		newSituation, layer = stack.pop(-1)
		print("")
		Board.printGrid(newSituation)
		for possibleMove in Board.getNeighborsForGrid(newSituation, Board.updateVehicles(newSituation)):
			if len(stack) > 100000:
				print("Stack length critical")
				solutionFound = True
				break
			elif Board.isSolution(possibleMove[0]) == True:
				print(" ")
				print("Final:")
				Board.printGrid(possibleMove[0])
				print("WINWINWIN")
				print("Total steps to solution:",layer+1)
				solutionFound = True
				break
			elif (possibleMove[0] not in visited) and ((possibleMove[0],layer+1) not in stack):
				stack.append( (possibleMove[0],layer+1) )
		visited.insert(0,newSituation)
	end = timer()

	if round(end-start,4) < 20:
		print("Runtime:",round(end-start,4), "aka VERY FAST, GASSSS")	
	else:
		print("Runtime:",round(end-start,4))


if __name__ == "__main__":
	dfs()

