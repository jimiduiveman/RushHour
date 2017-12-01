import csv
from classes.vehicle import Vehicle

class Board:

	def __init__(self, vehicles=None, parent=None, layer=0):
		self.vehicles = vehicles
		self.board = self.make_board()
		self.parent = parent
		self.layer = layer


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
		#board = self.make_board()
		# for row in board:
		# 	print(row, sep=' ')

		values = [item for sublist in self.board for item in sublist]
		for i,item in enumerate(values):
		    if (i+1)% (self.width+1) == 0:
		        print(item)
		    else:
		        print(item,end=' ')


	def possibleBoards(self):
		#WITH LITTLE INSPIRATION FROM: https://github.com/ryanwilsonperkin/rushhour
		#board = self.make_board()
		vehicles = self.vehicles
		possibleBoards = []
		for vehicle in self.vehicles:
			if vehicle.orientation == "HORIZONTAL":
				
				leftX_of_vehicle = vehicle.coordinates[0][0]
				y_of_vehicle = vehicle.coordinates[0][1]
				if leftX_of_vehicle > 0:
					for x in reversed(range(leftX_of_vehicle)):
						if self.board[y_of_vehicle][x] == '.':
							shift = x - leftX_of_vehicle
							newCoordinates = [ (x[0]+shift,y_of_vehicle) for x in vehicle.coordinates]
							newVehicle = Vehicle(vehicle.id, newCoordinates, vehicle.orientation)
							newVehicles = vehicles.copy()
							newVehicles.remove(vehicle)
							newVehicles.append(newVehicle)
							possibleBoards.append( Board(newVehicles, self, self.layer+1 ) )
						else:
							break
				
				rightX_of_vehicle = vehicle.coordinates[-1][0]
				if rightX_of_vehicle < self.width:
					for x in range(rightX_of_vehicle+1, self.width+1):
						if self.board[y_of_vehicle][x] == '.':
							shift = x - rightX_of_vehicle
							newCoordinates = [ (x[0]+shift,y_of_vehicle) for x in vehicle.coordinates]
							newVehicle = Vehicle(vehicle.id, newCoordinates, vehicle.orientation)
							newVehicles = vehicles.copy()
							newVehicles.remove(vehicle)
							newVehicles.append(newVehicle)
							possibleBoards.append( Board(newVehicles, self, self.layer+1 ) )
						else:
							break

			#VERTICAL
			else:

				upperY_of_vehicle = vehicle.coordinates[0][1]
				x_of_vehicle = vehicle.coordinates[0][0]
				if upperY_of_vehicle > 0:
					for y in reversed(range(upperY_of_vehicle)):
						if self.board[y][x_of_vehicle] == '.':
							shift = y -upperY_of_vehicle
							newCoordinates = [ (x_of_vehicle,y[1]+shift) for y in vehicle.coordinates]
							newVehicle = Vehicle(vehicle.id, newCoordinates, vehicle.orientation)
							newVehicles = vehicles.copy()
							newVehicles.remove(vehicle)
							newVehicles.append(newVehicle)
							possibleBoards.append( Board(newVehicles, self, self.layer+1 ) )
						else:
							break

				lowerY_of_vehicle = vehicle.coordinates[-1][1]
				if lowerY_of_vehicle < self.height:
					for y in range(lowerY_of_vehicle+1,self.height+1):
						if self.board[y][x_of_vehicle] == '.':
							shift = y - lowerY_of_vehicle
							newCoordinates = [ (x_of_vehicle,y[1]+shift) for y in vehicle.coordinates]
							newVehicle = Vehicle(vehicle.id, newCoordinates, vehicle.orientation)
							newVehicles = vehicles.copy()
							newVehicles.remove(vehicle)
							newVehicles.append(newVehicle)
							possibleBoards.append( Board(newVehicles, self, self.layer+1 ) )
						else:
							break
		return possibleBoards

	def isSolution(self):
		#board = self.make_board()
		for vehicle in self.vehicles:
			if vehicle.id == 'x':
				rightX_of_redCar = vehicle.coordinates[-1][0]
				y_of_redCar = vehicle.coordinates[0][1]
		
		for x in range(rightX_of_redCar+1, self.width+1):
			if self.board[y_of_redCar][x] != '.':
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

		return Board(vehicles,0)