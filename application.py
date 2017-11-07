import numpy as np


#MAKE GRID
grid = dict()
for x in range(1, 6):
    for y in range(1, 6):
	       grid[(x,y)] = 0


print(grid)
print()

#INITIALIZE VEHICLES
vehicles = dict()

vehicles[1] = [(4,3),(5,3)]

#UPDATE GRID
for vehicle in vehicles:
	for positie in vehicles[vehicle]:
		grid[positie] = vehicle

print(grid)
