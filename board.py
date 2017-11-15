import numpy as np
import csv
import sys

class Board:

	# def init(self):
	# 	self.width = width

	#LOAD VEHICLES FROM FILE
	def loadVehiclesFromFile():
		cmdargs = sys.argv
		vehicles = dict()
		y = 1
		with open(cmdargs[1]) as file:
			for row in csv.reader(file):
				dict_row = dict(enumerate(row))
				for value in dict_row:
					if dict_row[value] != '.':
						if dict_row[value] not in vehicles:
							vehicles[dict_row[value]] = [( value+1,y )] 
						else:
							vehicles[dict_row[value]].append( ( value+1,y ) )
				y += 1
		return vehicles


	#CREATE EMPTY GRID
	grid = dict()
	width = 6
	height = 6
	for x in range(1, width+1):
		for y in range(1, height+1):
			grid[(x,y)] = '.'

	#PUT VEHICLES ON GRID
	def updateGrid(grid:dict, vehicles:dict):
		for id in vehicles:
			for positie in vehicles[id]:
				grid[positie] = id
		return grid

	#PUT VEHICLES ON GRID FIRST TIME TO START
	vehicles = loadVehiclesFromFile()
	updateGrid(grid, vehicles)


	def printGrid(grid):
		coordinates_sorted_y = sorted(grid.keys(), key=lambda tup: tup[1])
		dict_sorted_y = {}
		for key in coordinates_sorted_y:
			dict_sorted_y[key] = grid[key]
		values = list(dict_sorted_y.values())

		for i,item in enumerate(values):
		    if (i+1)%Board.width == 0:
		        print(item)
		    else:
		        print(item,end=' ')

	#DETERMINE WHETHER VEHICLE CAN MOVE VERTICAL OR HORIZONTAL
	def movingDirection(id):
		if Board.vehicles[id][0][0] == Board.vehicles[id][1][0]:
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
		Board.updateGrid(copyGrid, copyVehicles)
		return copyGrid, copyVehicles

	def moveDown(grid:dict, id:int, move:int, vehicles:dict):
		copyGrid = dict(grid)
		copyVehicles = dict(vehicles)
		copyVehicles[id] = [(x[0], x[1]+move) for x in vehicles[id]]
		for x in vehicles[id]:
			copyGrid[(x[0], x[1])] = '.'
		Board.updateGrid(copyGrid, copyVehicles)
		return copyGrid, copyVehicles

	def moveLeft(grid:dict, id:int, move:int, vehicles:dict):
		copyGrid = dict(grid)
		copyVehicles = dict(vehicles)
		copyVehicles[id] = [(x[0]-move, x[1]) for x in vehicles[id]]
		for x in vehicles[id]:
			copyGrid[(x[0], x[1])] = '.'
		Board.updateGrid(copyGrid, copyVehicles)
		return copyGrid, copyVehicles

	def moveRight(grid:dict, id:int, move:int, vehicles:dict):
		copyGrid = dict(grid)
		copyVehicles = dict(vehicles)
		copyVehicles[id] = [(x[0]+move, x[1]) for x in vehicles[id]]
		for x in vehicles[id]:
			copyGrid[(x[0], x[1])] = '.'
		Board.updateGrid(copyGrid, copyVehicles)
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
		vehicles_dict = Board.updateVehicles(grid)
		possible = {}
		for id in vehicles_dict:
			if Board.movingDirection(id) == "horizontal":
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
				if rightX_of_vehicle != Board.width:
					for x in range(rightX_of_vehicle+1,Board.width+1):
						if grid[ (x, y_of_vehicle) ] == '.':
							shift = x - rightX_of_vehicle
							if id in possible:
								possible[id].append(shift)
							else:
								possible[id] = [shift]
						else:
							break
			elif Board.movingDirection(id) == "vertical":
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
				if lowerY_of_vehicle != Board.height:
					for y in range(lowerY_of_vehicle+1,Board.width+1):
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
		vehicles_dict = Board.updateVehicles(grid)
		rightX_of_redCar = vehicles_dict['x'][1][0]
		y_of_redCar = vehicles_dict['x'][1][1]
		for x in range(rightX_of_redCar+1, Board.width+1):
			if grid[(x,y_of_redCar)] != '.':
				return False
		return True

	def getNeighborsForGrid(grid:dict, vehicles:dict):
		possibleMoves = Board.checkMovable(grid)
		neighbors = []
		for id in possibleMoves:
			for move in possibleMoves[id]:
				if Board.movingDirection(id) == "horizontal":
					if move < 0:	
						neighbors.append(Board.moveLeft(grid, id, -move, Board.updateVehicles(grid)))
					else:
						neighbors.append(Board.moveRight(grid, id, move, Board.updateVehicles(grid)))
				else:
					if move < 0:
						neighbors.append(Board.moveUp(grid, id, -move, Board.updateVehicles(grid)))
					else:
						neighbors.append(Board.moveDown(grid, id, move, Board.updateVehicles(grid)))
		return neighbors

