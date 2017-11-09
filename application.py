import numpy as np


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
for x in range(1, 7):
	for y in range(1, 7):
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


def moveUp(grid:dict, id:int, moves:int): #layer 2 vereist vehicles als argument
	print("moveUp")
	copyGrid = dict(grid)
	copyVehicles = dict(vehicles)
	#print("Vehicle {} moved up from:".format(id), vehicles[id])
	copyVehicles[id] = [(x[0], x[1]-moves) for x in vehicles[id]]
	for x in vehicles[id]:
		copyGrid[(x[0], x[1])] = 0
	#copyGrid[ [(x[0], x[1]) for x in vehicles[id]] ] = 0
	#print("To:", vehicles[id])
	updateGrid(copyGrid, copyVehicles)
	printGrid(copyGrid)
	return copyGrid, copyVehicles

def moveDown(grid:dict, id:int, moves:int):
	copyGrid = dict(grid)
	copyVehicles = dict(vehicles)
	#print("Vehicle {} moved down from:".format(id), vehicles[id])
	copyVehicles[id] = [(x[0], x[1]+moves) for x in vehicles[id]]
	for x in vehicles[id]:
		copyGrid[(x[0], x[1])] = 0
	#print("To:", vehicles[id])
	updateGrid(copyGrid, copyVehicles)
	printGrid(copyGrid)
	return copyGrid, copyVehicles

def moveLeft(grid:dict, id:int, moves:int):
	copyGrid = dict(grid)
	if movingDirection(id) == "horizontal":
		if (vehicles[id][0][0]-1, vehicles[id][0][1]) in copyGrid:
			if copyGrid[ (vehicles[id][0][0]-1, vehicles[id][0][1]) ] == 0:
				print("Vehicle {} moved left from:".format(id), vehicles[id])
				vehicles[id] = [(x[0]-1, x[1]) for x in vehicles[id]]
				#print([(x[0]+1, x[1]) for x in vehicles[id][1]])
				copyGrid[ [(x[0]+1, x[1]) for x in vehicles[id]][1] ] = 0
				print("To:", vehicles[id])
				#updateGrid(copyGrid)
				printGrid(copyGrid)
	return copyGrid

def moveRight(grid:dict, id:int, moves:int):
	copyGrid = dict(grid)
	if movingDirection(id) == "horizontal":
		if (vehicles[id][1][0]+1, vehicles[id][1][1]) in copyGrid:
			if copyGrid[ (vehicles[id][1][0]+1, vehicles[id][1][1]) ] == 0:
				print("Vehicle {} moved right from:".format(id), vehicles[id])
				vehicles[id] = [(x[0]+1, x[1]) for x in vehicles[id]]
				copyGrid[ [(x[0]-1, x[1]) for x in vehicles[id]][0] ] = 0
				print("To:", vehicles[id])
				#updateGrid(copyGrid)
				printGrid(copyGrid)

	return copyGrid

def checkMovable(grid:dict):
	possible = {}
	for id in vehicles:
		if movingDirection(id) == "horizontal":
			#check if moveLeft is possible
			leftX_of_vehicle = vehicles[id][0][0]
			y_of_vehicle = vehicles[id][0][1]
			for x in reversed(range(1,leftX_of_vehicle)):
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
			for x in range(rightX_of_vehicle+1,7):
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
			for y in reversed(range(1, upperY_of_vehicle)):
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
			for y in range(lowerY_of_vehicle+1,7):
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
	for x in range(rightX_of_redCar+1,7):
		if grid[(x,y_of_redCar)] != 0:
			return False
	return True

def getNeighborsForGrid(grid:dict):
	possibleMoves = checkMovable(grid)
	neighbors = []
	for id in possibleMoves:
		for move in possibleMoves[id]:
			if movingDirection(id) == "horizontal":
				if move < 0:	
					neighbors.append(moveLeft(grid, id, -move))
				else:
					neighbors.append(moveRight(grid, id, move))
			else:
				if move < 0:
					neighbors.append(moveUp(grid, id, -move))
				else:
					neighbors.append(moveDown(grid, id, move))
	#print(possibleMoves)
	#for x in neighbors:
	#	printGrid(x)
	#	print()

getNeighborsForGrid(grid)


#solutionFound = isSolution(grid)
#queue = [grid]
#while solutionFound == False:
#	newSituation = queue.pop()
#	for possibleMove in  








