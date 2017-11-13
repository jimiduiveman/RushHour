import numpy as np
from timeit import default_timer as timer
import csv

vehicles = dict()
y = 1
with open("board1.txt") as file:
	for row in csv.reader(file):
		dict_row = dict(enumerate(row))
		for value in dict_row:
			if dict_row[value] != '.':
				if dict_row[value] not in vehicles:
					vehicles[dict_row[value]] = [( value+1,y )] 
				else:
					vehicles[dict_row[value]].append( ( value+1,y ) )
		y += 1


#CREATE GRID
grid = dict()
width = 6
height = 6
for x in range(1, width+1):
	for y in range(1, height+1):
		grid[(x,y)] = '.'

def updateGrid(grid:dict, vehicles:dict):
	for id in vehicles:
		for positie in vehicles[id]:
			grid[positie] = id
	return grid

updateGrid(grid, vehicles)


def printGrid(grid):
	coordinates_sorted_y = sorted(grid.keys(), key=lambda tup: tup[1])
	dict_sorted_y = {}
	for key in coordinates_sorted_y:
		dict_sorted_y[key] = grid[key]
	values = list(dict_sorted_y.values())

	for i,item in enumerate(values):
	    if (i+1)%width == 0:
	        print(item)
	    else:
	        print(item,end=' ')

#DETERMINE WHETHER VEHICLE CAN MOVE VERTICAL OR HORIZONTAL
def movingDirection(id):
	if vehicles[id][0][0] == vehicles[id][1][0]:
		return "vertical"
	else:
		return "horizontal"


def moveUp(grid:dict, id:int, move:int, vehicles:dict): #layer 2 vereist vehicles als argument
	#print("{} can moveUp {}".format(id, move))
	copyGrid = dict(grid)
	copyVehicles = dict(vehicles)
	#print("Vehicle {} moved up from:".format(id), vehicles[id])
	copyVehicles[id] = [(x[0], x[1]-move) for x in vehicles[id]]
	for x in vehicles[id]:
		copyGrid[(x[0], x[1])] = '.'
	updateGrid(copyGrid, copyVehicles)
	return copyGrid, copyVehicles

def moveDown(grid:dict, id:int, move:int, vehicles:dict):
	copyGrid = dict(grid)
	copyVehicles = dict(vehicles)
	copyVehicles[id] = [(x[0], x[1]+move) for x in vehicles[id]]
	for x in vehicles[id]:
		copyGrid[(x[0], x[1])] = '.'
	updateGrid(copyGrid, copyVehicles)
	return copyGrid, copyVehicles

def moveLeft(grid:dict, id:int, move:int, vehicles:dict):
	copyGrid = dict(grid)
	copyVehicles = dict(vehicles)
	copyVehicles[id] = [(x[0]-move, x[1]) for x in vehicles[id]]
	for x in vehicles[id]:
		copyGrid[(x[0], x[1])] = '.'
	updateGrid(copyGrid, copyVehicles)
	return copyGrid, copyVehicles

def moveRight(grid:dict, id:int, move:int, vehicles:dict):
	copyGrid = dict(grid)
	copyVehicles = dict(vehicles)
	copyVehicles[id] = [(x[0]+move, x[1]) for x in vehicles[id]]
	for x in vehicles[id]:
		copyGrid[(x[0], x[1])] = '.'
	updateGrid(copyGrid, copyVehicles)
	return copyGrid, copyVehicles

def updateVehicles(grid:dict):
	vehicles_dict = {}
	for coordinate in grid:
		id = grid[coordinate]
		if id != '.':
			if id not in vehicles_dict:
				vehicles_dict[id] = [coordinate]
			else:
				vehicles_dict[id].append(coordinate)
	return vehicles_dict

def checkMovable(grid:dict):
	vehicles_dict = updateVehicles(grid)
	possible = {}
	for id in vehicles_dict:
		if movingDirection(id) == "horizontal":
			leftX_of_vehicle = vehicles_dict[id][0][0]
			y_of_vehicle = vehicles_dict[id][0][1]
			if leftX_of_vehicle != 1:
				for x in reversed(range(1,leftX_of_vehicle)):
					if grid[ (x, y_of_vehicle) ] == '.':
						shift = x - leftX_of_vehicle
						if id in possible:
							possible[id].append(shift)
						else:
							possible[id] = [shift]
					else:
						break
			rightX_of_vehicle = vehicles_dict[id][-1][0]
			if rightX_of_vehicle != width:
				for x in range(rightX_of_vehicle+1,width+1):
					if grid[ (x, y_of_vehicle) ] == '.':
						shift = x - rightX_of_vehicle
						if id in possible:
							possible[id].append(shift)
						else:
							possible[id] = [shift]
					else:
						break
		elif movingDirection(id) == "vertical":
			upperY_of_vehicle = vehicles_dict[id][0][1]
			x_of_vehicle = vehicles_dict[id][0][0]
			if upperY_of_vehicle != 1:
				for y in reversed(range(1, upperY_of_vehicle)):
					if grid[ (x_of_vehicle, y) ] == '.':
						shift = y - upperY_of_vehicle
						if id in possible:
							possible[id].append(shift)
						else:
							possible[id] = [shift]
					else:
						break
			lowerY_of_vehicle = vehicles_dict[id][-1][1]
			if lowerY_of_vehicle != height:
				for y in range(lowerY_of_vehicle+1,width+1):
					if grid[ (x_of_vehicle, y) ] == '.':
						shift = y - lowerY_of_vehicle
						if id in possible:
							possible[id].append(shift)
						else:
							possible[id] = [shift]
					else:
						break
	return possible

def isSolution(grid:dict):
	vehicles_dict = updateVehicles(grid)
	rightX_of_redCar = vehicles_dict['x'][1][0]
	y_of_redCar = vehicles_dict['x'][1][1]
	for x in range(rightX_of_redCar+1,width+1):
		if grid[(x,y_of_redCar)] != '.':
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

while solutionFound == False:
	newSituation = queue.pop(0)
	print("")
	printGrid(newSituation)
	for possibleMove in getNeighborsForGrid(newSituation, updateVehicles(newSituation)):
		if isSolution(possibleMove[0]) == True:
			print(" ")
			print("Final:")
			printGrid(possibleMove[0])
			print("WINWINWIN")
			solutionFound = True
			break
		elif (possibleMove[0] not in visited) and (possibleMove[0] not in queue):
			queue.append(possibleMove[0])
		else:
			visited.append(possibleMove[0])
	visited.append(newSituation)
end = timer()

print("Runtime:",round(end-start,4))	





