import numpy as np
from timeit import default_timer as timer


#INITIALIZE VEHICLES
vehicles = dict()

vehicles[1] = [(4,3),(5,3)]
vehicles[2] = [(4,1),(5,1)]
vehicles[3] = [(3,1),(3,2),(3,3)]
vehicles[4] = [(2,5),(3,5)]
vehicles[5] = [(5,6),(6,6)]
vehicles[6] = [(4,4),(4,5),(4,6)]
vehicles[7] = [(6,1),(6,2),(6,3)]
vehicles[8] = [(5,4),(6,4)]
vehicles[9] = [(1,5),(1,6)]

#CREATE GRID
grid = dict()
width = 6
height = 6
for x in range(1, width+1):
	for y in range(1, height+1):
		grid[(x,y)] = 0

def updateGrid(grid:dict, vehicles:dict):
	for vehicle in vehicles:
		for positie in vehicles[vehicle]:
			grid[positie] = vehicle
	return grid

updateGrid(grid, vehicles)

def printGrid(grid):
	board = []
	row1 = []
	row2 = []
	row3 = []
	row4 = []
	row5 = []
	row6 = []

	for column in grid:
		if column[1] == 1:
			row1.append(grid[column])
		elif column[1] == 2:
			row2.append(grid[column])
		elif column[1] == 3:
			row3.append(grid[column])
		elif column[1] == 4:
			row4.append(grid[column])
		elif column[1] == 5:
			row5.append(grid[column])
		elif column[1] == 6:
			row6.append(grid[column])

	board = [row1,row2,row3,row4,row5,row6]
	print('\n'.join(' '.join(map(str, x)) for x in board))

printGrid(grid)

#DETERMINE WHETHER VEHICLE CAN MOVE VERTICAL OR HORIZONTAL
def movingDirection(id):
	if vehicles[id][0][0] == vehicles[id][1][0]:
		return "vertical"
	else:
		return "horizontal"


def moveUp(grid:dict, id:int, moves:int, vehicles:dict): #layer 2 vereist vehicles als argument
	print("{} can moveUp {}".format(id, moves))
	copyGrid = dict(grid)
	copyVehicles = dict(vehicles)
	#print("Vehicle {} moved up from:".format(id), vehicles[id])
	copyVehicles[id] = [(x[0], x[1]-moves) for x in vehicles[id]]
	for x in vehicles[id]:
		copyGrid[(x[0], x[1])] = 0
	#copyGrid[ [(x[0], x[1]) for x in vehicles[id]] ] = 0
	#print("To:", vehicles[id])
	updateGrid(copyGrid, copyVehicles)
	#printGrid(copyGrid)
	return copyGrid, copyVehicles

def moveDown(grid:dict, id:int, moves:int, vehicles:dict):
	print("{} can moveDown {}".format(id, moves))
	copyGrid = dict(grid)
	copyVehicles = dict(vehicles)
	#print("Vehicle {} moved down from:".format(id), vehicles[id])
	copyVehicles[id] = [(x[0], x[1]+moves) for x in vehicles[id]]
	for x in vehicles[id]:
		copyGrid[(x[0], x[1])] = 0
	#print("To:", vehicles[id])
	updateGrid(copyGrid, copyVehicles)
	#printGrid(copyGrid)
	return copyGrid, copyVehicles

def moveLeft(grid:dict, id:int, moves:int, vehicles:dict):
	print("{} can moveLeft {}".format(id, moves))
	copyGrid = dict(grid)
	copyVehicles = dict(vehicles)
	copyVehicles[id] = [(x[0]-moves, x[1]) for x in vehicles[id]]
	for x in vehicles[id]:
		copyGrid[(x[0], x[1])] = 0
	updateGrid(copyGrid, copyVehicles)
	#printGrid(copyGrid)
	return copyGrid, copyVehicles

def moveRight(grid:dict, id:int, moves:int, vehicles:dict):
	print("{} can moveRight {}".format(id, moves))
	copyGrid = dict(grid)
	copyVehicles = dict(vehicles)
	copyVehicles[id] = [(x[0]+moves, x[1]) for x in vehicles[id]]
	for x in vehicles[id]:
		copyGrid[(x[0], x[1])] = 0
	updateGrid(copyGrid, copyVehicles)
	#printGrid(copyGrid)
	return copyGrid, copyVehicles

def updateVehicles(grid:dict):
	vehicles_dict = {}
	for coordinate in grid:
		id = grid[coordinate]
		if id != 0:
			if id not in vehicles_dict:
				vehicles_dict[id] = [coordinate]
			else:
				vehicles_dict[id].append(coordinate)
	return vehicles_dict

def checkMovable(grid:dict):
	updateVehicles(grid)
	possible = {}
	for id in vehicles:
		if movingDirection(id) == "horizontal":
			#check if moveLeft is possible
			leftX_of_vehicle = vehicles[id][0][0]
			y_of_vehicle = vehicles[id][0][1]
			for x in reversed(range(1,leftX_of_vehicle-1)):
				if grid[ (x, y_of_vehicle) ] == 0:
					shift = x - leftX_of_vehicle
					if id in possible:
						possible[id].append(shift)
					else:
						possible[id] = [shift]
				else:
					break
			#check if moveRight is possible
			rightX_of_vehicle = vehicles[id][-1][0]
			for x in range(rightX_of_vehicle+1,width+1):
				if grid[ (x, y_of_vehicle) ] == 0:
					shift = rightX_of_vehicle - x
					if id in possible:
						possible[id].append(shift)
					else:
						possible[id] = [shift]
				else:
					break
		elif movingDirection(id) == "vertical":
			#check if moveUp is possible
			upperY_of_vehicle = vehicles[id][0][1]
			x_of_vehicle = vehicles[id][0][0]
			for y in reversed(range(1, upperY_of_vehicle-1)):
				if grid[ (x_of_vehicle, y) ] == 0:
					shift = y - upperY_of_vehicle
					if id in possible:
						possible[id].append(shift)
					else:
						possible[id] = [shift]
				else:
					break
			#check if moveDown is possible
			lowerY_of_vehicle = vehicles[id][-1][1]
			for y in range(lowerY_of_vehicle+1,width+1):
				if grid[ (x_of_vehicle, y) ] == 0:
					shift = y - lowerY_of_vehicle
					if id in possible:
						possible[id].append(shift)
					else:
						possible[id] = [shift]
				else:
					break
	return possible

def isSolution(grid:dict):
	rightX_of_redCar = vehicles[1][1][0]
	y_of_redCar = vehicles[1][1][1]
	for x in range(rightX_of_redCar+1,width+1):
		if grid[(x,y_of_redCar)] != 0:
			return False
	return True

def getNeighborsForGrid(grid:dict, vehicles:dict):
	possibleMoves = checkMovable(grid)
	neighbors = []
	for id in possibleMoves:
		for move in possibleMoves[id]:
			if movingDirection(id) == "horizontal":
				if move < 0:	
					neighbors.append(moveLeft(grid, id, -move, updateVehicles(grid)))
				else:
					neighbors.append(moveRight(grid, id, move, updateVehicles(grid)))
			else:
				if move < 0:
					neighbors.append(moveUp(grid, id, -move, updateVehicles(grid)))
				else:
					neighbors.append(moveDown(grid, id, move, updateVehicles(grid)))
	return neighbors


start = timer()
solutionFound = isSolution(grid)
queue = [grid]
visited = []
#levelDict = {}
while solutionFound == False:
	newSituation = queue.pop(0)
	print("")
	printGrid(newSituation)
	for possibleMove in getNeighborsForGrid(newSituation, updateVehicles(newSituation)):
		#updateGrid(possibleMove[0], possibleMove[1])
		#printGrid(possibleMove[0])
		#print()
		#level[newSituation] = possibleMove
		if isSolution(possibleMove[0]) == True:
			print(" ")
			print("Final:")
			printGrid(possibleMove[0])
			print("WINWINWIN")
			solutionFound = True
			break
		elif (possibleMove[0] not in visited):
			queue.append(possibleMove[0])
		else:
			visited.append(newSituation)

	visited.append(newSituation)
#print(level)
end = timer()

print("Runtime:",round(end-start,4),"aka VERY FAST, GASSSSSSS")	
	
	#print(len(queue))
	#solutionFound = True


# solutionFound = isSolution(grid)
# queue = [grid]
# visited = []
# for x in range(1):
# 	newSituation = queue.pop()
# 	for possibleMove in getNeighborsForGrid(newSituation):
# 		#print(possibleMove[0])
# 		#print()
# 		print()
# 		if isSolution(possibleMove[0]) == True:
# 			solutionFound = True
# 		elif (possibleMove[0] not in queue):
# 			queue.append(possibleMove[0])
# 	visited.append(newSituation)
# 	print(len(visited))
# 	#print(queue)





