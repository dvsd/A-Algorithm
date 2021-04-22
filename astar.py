#import libraries
from graphics import *
import math

# declare size of grid
row = 10
col = 10
grid = [] # declare grid that will contain an instance of Spot in each position

# declare open and closed sets for evaluating each position
openSet = []
closedSet = []

path = [] # declare best path
walls = [] # coordinates of obstacles

doneWalls = False

# Grid passes the amount of rows and columns and creates a 2D array and draws nonwalls white and walls black
def Grid(rows,cols):
	for i in range(rows):
		grid.append([])
		for j in range(cols):
			grid[i].append(Spot(i,j)) # create an instance of Spot for position in grid
			grid[i][j].draw("white")
			#if grid[i][j].wall:
			#	grid[i][j].draw("black")
			#else:
			#	grid[i][j].draw("white")

# The Spot class associates the A* function of f=g(cost)+h(heuristic) with each spot on the grid
class Spot():
	def __init__(self,i,j): #initialize with coordinates
		self.x = i
		self .y = j
		self.f = 0
		self.g = 0
		self.h = 0
		self.previous = None
		self.wall = False
	def draw(self,color):
		rectangle = Rectangle(Point(self.x*40,self.y*40),Point((self.x*40)+39,(self.y*40)+39))
		rectangle.setFill(color)
		rectangle.draw(win)
	#def updateWalls(self):
	#	if [self.x, self.y] in walls:
	#		self.wall = True
	#	else:
	#		self.wall = False

# heuristic function using eucledian distance
def distbetween(start,end):
	return math.sqrt((start.x-end.x)**2+(start.y-end.y)**2)

win = GraphWin("A* Simulation",400,400) # open GUI window

Grid(row,col) # create grid

# draw walls loop
while not doneWalls:
	mouseClick = win.checkMouse()
	if mouseClick:
		#walls.append([math.floor(mouseClick.x/40),math.floor(mouseClick.y/40)])
		grid[int(math.floor(mouseClick.x/40))][int(math.floor(mouseClick.y/40))].wall = True
		grid[int(math.floor(mouseClick.x/40))][int(math.floor(mouseClick.y/40))].draw("black")
	if win.checkKey():
		doneWalls = True

# declare start and end points
start = grid[0][0]
end = grid[row-1][col-1]

neighbors = []

openSet.append(start) # first node is added to open set
dirs = [[-1,0],[1,0],[0,1],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]]
current = openSet[0] # current node being evaluated is the start node

# draw open set(start node)
for i in openSet:
	i.draw("green")

# while every node in open set is evaluated
while len(openSet) != 0:
	neighbors=[] # reset neighbors array
	current = openSet[0] # first value in open set is set to initial minimum
	# find lowest f value in open set
	for spot in openSet:
		if spot.f < current.f:
			current = spot

	# current node is about to evaluated so remove from open set and add to closed set
	openSet.remove(current)
	closedSet.append(current)

	# if the end node is found
	if current == end:
		# draw final node in closed set
		for i in closedSet:
			i.draw("red")

		temp = current
		path.append(temp)
		while temp.previous is not None:
			path.append(temp.previous)
			temp = temp.previous
		for i in path: # draw best path in blue
			i.draw("blue")

		break # break out of while loop
	# find neighbors of current node in the LURD and diagnol directions
	for i in dirs:
		neighborX = current.x + i[0]
		neighborY = current.y + i[1]
		if neighborX > -1 and neighborY > -1 and neighborX < row and neighborY < col: # if on the grid
			if grid[neighborX][neighborY] not in closedSet and grid[neighborX][neighborY].wall == False: # if not evaluated and not a wall
				neighbors.append(grid[neighborX][neighborY]) # add spot to neighbor array

	for neighbor in neighbors: # for every neighbor
		tempg = current.g + 1
		if neighbor in openSet: # if neighbor already has a g value
			if tempg < neighbor.g: # if new g value is better than old g value
				neighbor.g = tempg # new g value becomes neighbor's g value
				neighbor.previous = current
		else: # if neightbor has not been evaluated
			neighbor.previous = current
			neighbor.g = tempg
			openSet.append(neighbor) # add to open set since it's a newly found node
		neighbor.h = distbetween(neighbor,end) # h value is the heuristic(euclidian distance)
		neighbor.f = neighbor.g + neighbor.h # f value is the g value plus the h value

	# draw open and closed sets
	for i in openSet:
		i.draw("green")
	for i in closedSet:
		i.draw("red")

win.getMouse() # close window on mouse click
