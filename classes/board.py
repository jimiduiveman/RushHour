import csv
from classes.vehicle import Vehicle
import numpy as np

class Board:
	"""
	Creates board instances from the original .csv/.txt board files
	using the vehicles instances from the vehicles class.
	"""

	def __init__(self, vehicles=None, parent=None, layer=0):
		self.vehicles = vehicles
		self.board = self.make_board()
		self.parent = parent
		self.layer = layer

	def __str__(self):
		#Creates a string representation of any given Rush hour style board
		string = ""
		for row in self.make_board():
			for value in row:
				string += value
		return string


	def make_board(self):
		"""
		Returns an instance board.
		"""
		#Create a board with dot (empty) values for the given height and width
		board = [['.']*(self.width+1) for i in range((self.height+1))] #+1 because the range begins at 0

		#Fill the board with the given vehicle coordinates
		for vehicle in self.vehicles:
			coordinates = vehicle.coordinates
			for coordinate in coordinates:
				x,y = coordinate[0],coordinate[1]
				board[y][x] = vehicle.id
		
		return board

	def transform(self):
		board = self.board
		for row in self.board:
			for (i, item) in enumerate(row):
				if item == 'x':
					row[i] = float(2)
				elif item == '.':
					row[i] = float(1)
				else:
					row[i] = float( ord(item)-61 )
		
		return board



	def print_board(self):
		"""
		Print function for the instaces board.
		"""
		
		#Returns a board instance
		values = [item for sublist in self.board for item in sublist]
		for i,item in enumerate(values):
		    if (i+1)% (self.width+1) == 0:
		        print(item)
		    else:
		        print(item,end=' ')


	def possibleBoards(self):
		"""
		Returns possible instaces of boards by shifting vehicles.
		"""
		#With a little inspiration from: https://github.com/ryanwilsonperkin/rushhour
		
		vehicles = self.vehicles
		
		#Create an empty list for the possible board instances
		possibleBoards = []
		for vehicle in self.vehicles:
		
			#If the orientation of the given vehicle is horizontal:
			if vehicle.orientation == "HORIZONTAL":
		
				#1.Check if left space from vehicle is empty
				leftX_of_vehicle = vehicle.coordinates[0][0]
				y_of_vehicle = vehicle.coordinates[0][1]
				if leftX_of_vehicle > 0:
					for x in reversed(range(leftX_of_vehicle)):
		
						#If the space is empty, shift the vehicle to the left
						if self.board[y_of_vehicle][x] == '.':
							shift = x - leftX_of_vehicle
		
							#Create a new coordinate of the shifted vehicle
							newCoordinates = [ (x[0]+shift,y_of_vehicle) for x in vehicle.coordinates]
		
							#With new coordinate of shifted vehicle, create a new board instance
							newVehicle = Vehicle(vehicle.id, newCoordinates, vehicle.orientation)
							newVehicles = vehicles.copy()
							newVehicles.remove(vehicle)
							newVehicles.append(newVehicle)
							possibleBoards.append( Board(newVehicles, self, self.layer+1 ) )
						else:
							break
		
				#2.Check if right space from vehicle is empty
				rightX_of_vehicle = vehicle.coordinates[-1][0]
				if rightX_of_vehicle < self.width:
					for x in range(rightX_of_vehicle+1, self.width+1):
		
						#If the space is empty, shift the vehicle to the right
						if self.board[y_of_vehicle][x] == '.':
							shift = x - rightX_of_vehicle
		
							#Create a new coordinate of the shifted vehicle
							newCoordinates = [ (x[0]+shift,y_of_vehicle) for x in vehicle.coordinates]
		
							#With new coordinate of shifted vehicle, create a new board instance
							newVehicle = Vehicle(vehicle.id, newCoordinates, vehicle.orientation)
							newVehicles = vehicles.copy()
							newVehicles.remove(vehicle)
							newVehicles.append(newVehicle)
							possibleBoards.append( Board(newVehicles, self, self.layer+1 ) )
						else:
							break

			#Else if the orientation of the given vehicle is vertical:
			else:
		
				#1.Check if space above of the vehicle is empty
				upperY_of_vehicle = vehicle.coordinates[0][1]
				x_of_vehicle = vehicle.coordinates[0][0]
				if upperY_of_vehicle > 0:
					for y in reversed(range(upperY_of_vehicle)):
		
						#If the space is empty, shift the vehicle upwards
						if self.board[y][x_of_vehicle] == '.':
							shift = y -upperY_of_vehicle
		
							#Create a new coordinate of the shifted vehicle
							newCoordinates = [ (x_of_vehicle,y[1]+shift) for y in vehicle.coordinates]
		
							#With new coordinate of shifted vehicle, create a new board instance
							newVehicle = Vehicle(vehicle.id, newCoordinates, vehicle.orientation)
							newVehicles = vehicles.copy()
							newVehicles.remove(vehicle)
							newVehicles.append(newVehicle)
							possibleBoards.append( Board(newVehicles, self, self.layer+1 ) )
						else:
							break
		
				#2.Check if space below the vehicle is empty
				lowerY_of_vehicle = vehicle.coordinates[-1][1]
				if lowerY_of_vehicle < self.height:
					for y in range(lowerY_of_vehicle+1,self.height+1):
		
						#If the space is empty, shift the vehicle down
						if self.board[y][x_of_vehicle] == '.':
							shift = y - lowerY_of_vehicle
		
							#Create a new coordinate of the shifted vehicle
							newCoordinates = [ (x_of_vehicle,y[1]+shift) for y in vehicle.coordinates]
		
							#With new coordinate of shifted vehicle, create a new board instance
							newVehicle = Vehicle(vehicle.id, newCoordinates, vehicle.orientation)
							newVehicles = vehicles.copy()
							newVehicles.remove(vehicle)
							newVehicles.append(newVehicle)
							possibleBoards.append( Board(newVehicles, self, self.layer+1 ) )
						else:
							break
		
		return possibleBoards

	def isSolution(self):
		"""
		Returns a solution board.
		"""
		
		for vehicle in self.vehicles:
		
			#Find the right coordinates of the vehicle with 'x' id
			if vehicle.id == 'x':
				rightX_of_redCar = vehicle.coordinates[-1][0]
				y_of_redCar = vehicle.coordinates[0][1]
		
		#Check if the spaces of the right of the car with id 'x' are empty
		for x in range(rightX_of_redCar+1, self.width+1):
			if self.board[y_of_redCar][x] != '.':
				return False
		
		#Return the solution instance		
		return True

	def setFinishingState(self):
		"""
		Makes the board with the finishing state.
		In other words, the set which moves the red vehicle out of the board.
		"""
		vehicles = self.vehicles
		for vehicle in self.vehicles:
		
			#Find the right coordinates of the vehicle with 'x' id
			if vehicle.id == 'x':
				y_of_vehicle = vehicle.coordinates[0][1]
				newVehicle = Vehicle(vehicle.id, [(self.width-1,y_of_vehicle),(self.width,y_of_vehicle)], vehicle.orientation)
				newVehicles = vehicles.copy()
				newVehicles.remove(vehicle)
				newVehicles.append(newVehicle)

		return Board(newVehicles, self, self.layer+1 )


	def load_from_file(filename):
		"""
		Loads a .csv/.txt file to create a board instance.
		"""
		
		#Create an empty list for vehicles
		vehicles = []
		
		#Create an empty dictionary for vehicles
		vehicles_dict = dict()
		y = 0
		with open(filename) as filename:
			
			#Create coordinates
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
		
		#Append the coordinates to their right place in board
		for vehicle in vehicles_dict:
			id = vehicle
			coordinates = vehicles_dict[vehicle]
			if coordinates[0][0] == coordinates[1][0]:
				orientation = "VERTICAL"
			else:
				orientation = "HORIZONTAL"
			
			vehicles.append(Vehicle(id,coordinates,orientation))

		return Board(vehicles,0)