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

for vehicle in vehicles:
	for positie in vehicles[vehicle]:
		grid[positie] = vehicle

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

def movingDirection(id):
	if vehicles[id][0][0] == vehicles[id][1][0]:
		return "vertical"
	else:
		return "horizontal"

def moveUp(id):
	if movingDirection(id) == "vertical":
		if board[vehicles[id][0][1]-1][vehicles[id][1][0]-2] == 0:
			vehicles[id][0][1] -= 1 # typeError: 'tuple' object does not support item assignment

moveUp(9)












