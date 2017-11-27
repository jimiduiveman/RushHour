import sys
sys.path.append("/Users/jimiduiveman/Documents/Informatiekunde/Jaar3/ProgrammeerTheorie/RushHour/")
import csv
from timeit import default_timer as timer

from collections import deque


class Vehicle:

	def __init__(self, id, coordinates, orientation):
		self.id = id
		self.coordinates = coordinates
		self.orientation = orientation



class Board:

	def __init__(self, vehicles=None):
		self.vehicles = vehicles


	def __str__(self):
		string = ""
		for row in self.make_board():
			for value in row:
				string += value
		return string


	def make_board(self):
		#CREATE BOARD WITH DOT VALUES
		board = []
		for y in range(self.height+1):
			board.append([])
			for x in range(self.width+1):
				board[y].append('.',)

		#FILL BOARD WITH VEHICLES
		for vehicle in self.vehicles:
			coordinates = vehicle.coordinates
			for coordinate in coordinates:
				x,y = coordinate[0],coordinate[1]
				board[y][x] = vehicle.id
		return board

	def print_board(self):
		board = self.make_board()
		# for row in board:
		# 	print(row, sep=' ')

		values = [item for sublist in board for item in sublist]
		for i,item in enumerate(values):
		    if (i+1)% (self.width+1) == 0:
		        print(item)
		    else:
		        print(item,end=' ')


	def possibleBoards(self):
		#WITH LITTLE INSPIRATION FROM: https://github.com/ryanwilsonperkin/rushhour
		board = self.make_board()
		vehicles = self.vehicles
		possibleBoards = []
		for vehicle in self.vehicles:
			if vehicle.orientation == "HORIZONTAL":
				
				leftX_of_vehicle = vehicle.coordinates[0][0]
				y_of_vehicle = vehicle.coordinates[0][1]
				if leftX_of_vehicle > 0:
					for x in reversed(range(leftX_of_vehicle)):
						if board[y_of_vehicle][x] == '.':
							shift = x - leftX_of_vehicle
							newCoordinates = [ (x[0]+shift,y_of_vehicle) for x in vehicle.coordinates]
							newVehicle = Vehicle(vehicle.id, newCoordinates, vehicle.orientation)
							newVehicles = vehicles.copy()
							newVehicles.remove(vehicle)
							newVehicles.append(newVehicle)
							possibleBoards.append( Board(newVehicles) )
						else:
							break
				
				rightX_of_vehicle = vehicle.coordinates[-1][0]
				if rightX_of_vehicle < self.width:
					for x in range(rightX_of_vehicle+1, self.width+1):
						if board[y_of_vehicle][x] == '.':
							shift = x - rightX_of_vehicle
							newCoordinates = [ (x[0]+shift,y_of_vehicle) for x in vehicle.coordinates]
							newVehicle = Vehicle(vehicle.id, newCoordinates, vehicle.orientation)
							newVehicles = vehicles.copy()
							newVehicles.remove(vehicle)
							newVehicles.append(newVehicle)
							possibleBoards.append( Board(newVehicles) )
						else:
							break

			elif vehicle.orientation == "VERTICAL":

				upperY_of_vehicle = vehicle.coordinates[0][1]
				x_of_vehicle = vehicle.coordinates[0][0]
				if upperY_of_vehicle > 0:
					for y in reversed(range(upperY_of_vehicle)):
						if board[y][x_of_vehicle] == '.':
							shift = y -upperY_of_vehicle
							newCoordinates = [ (x_of_vehicle,y[1]+shift) for y in vehicle.coordinates]
							newVehicle = Vehicle(vehicle.id, newCoordinates, vehicle.orientation)
							newVehicles = vehicles.copy()
							newVehicles.remove(vehicle)
							newVehicles.append(newVehicle)
							possibleBoards.append( Board(newVehicles) )
						else:
							break

				lowerY_of_vehicle = vehicle.coordinates[-1][1]
				if lowerY_of_vehicle < self.height:
					for y in range(lowerY_of_vehicle+1,self.height+1):
						if board[y][x_of_vehicle] == '.':
							shift = y - lowerY_of_vehicle
							newCoordinates = [ (x_of_vehicle,y[1]+shift) for y in vehicle.coordinates]
							newVehicle = Vehicle(vehicle.id, newCoordinates, vehicle.orientation)
							newVehicles = vehicles.copy()
							newVehicles.remove(vehicle)
							newVehicles.append(newVehicle)
							possibleBoards.append( Board(newVehicles) )
						else:
							break
		return possibleBoards

	def isSolution(self):
		board = self.make_board()
		for vehicle in self.vehicles:
			if vehicle.id == 'x':
				rightX_of_redCar = vehicle.coordinates[-1][0]
				y_of_redCar = vehicle.coordinates[0][1]
		
		for x in range(rightX_of_redCar+1, self.width+1):
			if board[y_of_redCar][x] != '.':
				return False
		return True



#FIRST TIME LOAD FILE AND CREATE A BOARD INSTANCE
def load_from_file(filename):
	vehicles = []
	vehicles_dict = dict()
	y = 0
	with open(filename) as filename:
		
		#CREATE COORDINATES
		for row in csv.reader(filename):
			dict_row = dict(enumerate(row))
			width = len(dict_row)
			heigth = width
			for value in dict_row:
				if dict_row[value] != '.':
					if dict_row[value] not in vehicles_dict:
						vehicles_dict[dict_row[value]] = [( value,y )] 
					else:
						vehicles_dict[dict_row[value]].append( ( value,y ) )
			y += 1
	y -= 1
	Board.height = y
	Board.width = y

	for vehicle in vehicles_dict:
		id = vehicle
		coordinates = vehicles_dict[vehicle]
		if coordinates[0][0] == coordinates[1][0]:
			orientation = "VERTICAL"
		else:
			orientation = "HORIZONTAL"
		
		vehicles.append(Vehicle(id,coordinates,orientation))

	return Board(vehicles)



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
		first_board = load_from_file(filename)
	bfs(first_board)




