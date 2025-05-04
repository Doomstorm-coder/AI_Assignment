import turtle
import time
import heapq

# Set up screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("A Maze Solving Program")
wn.setup(1300, 700)

# Define *
class Maze(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)

class Green(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("green")
        self.penup()
        self.speed(0)

class Blue(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)

class Red(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("red")
        self.setheading(270)
        self.penup()
        self.speed(0)

class Yellow(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("yellow")
        self.penup()
        self.speed(0)

# Maze grid
grid1 = [
    "++++++++++++++++++++++++++++++++++++++++++++++",
    "+ s             +                            +",
    "+ +++++++++++ +++++++++++++++ ++++++++ +++++ +",
    "+           +                 +        +     +",
    "++ +++++++ ++++++++++++++ ++++++++++++++++++++",
    "++ ++    + ++           + ++                 +",
    "++ ++ ++ + ++ ++ +++++ ++ ++ +++++++++++++++ +",
    "++ ++ ++ + ++ ++ +     ++ ++ ++ ++        ++ +",
    "++ ++ ++++ ++ +++++++++++ ++ ++ +++++ +++ ++ +",
    "++ ++   ++ ++             ++          +++ ++ +",
    "++ ++++ ++ +++++++++++++++++ +++++++++++++++ +",
    "++    + ++                   ++              +",
    "+++++ + +++++++++++++++++++++++ ++++++++++++ +",
    "++ ++ +                   ++          +++ ++ +",
    "++ ++ ++++ ++++++++++++++ ++ +++++ ++ +++ ++ +",
    "++ ++ ++   ++     +    ++ ++ ++    ++     ++ +",
    "++ ++ ++ +++++++ +++++ ++ ++ +++++++++++++++ +",
    "++                     ++ ++ ++              +",
    "+++++ ++ + +++++++++++ ++ ++ ++ ++++++++++++e+",
    "++++++++++++++++++++++++++++++++++++++++++++++",
]

# Heuristic function (Manhattan distance)
def heuristic(cell, goal):
    x1, y1 = cell
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)

# Draw shortest path
def backRoute(x, y):
    yellow.goto(x, y)
    yellow.stamp()
    while (x, y) != (start_x, start_y):
        x, y = solution[x, y]
        yellow.goto(x, y)
        yellow.stamp()

# Greedy or A* search
def solve(algorithm="greedy"):
    frontier = []
    heapq.heappush(frontier, (heuristic((start_x, start_y), (end_x, end_y)), 0, (start_x, start_y)))
    solution[start_x, start_y] = None
    costs = { (start_x, start_y): 0 }

    while frontier:
        _, g, current = heapq.heappop(frontier)
        x, y = current

        if (x, y) == (end_x, end_y):
            backRoute(x, y)
            return

        for dx, dy in [(-24, 0), (0, -24), (24, 0), (0, 24)]:
            neighbor = (x + dx, y + dy)
            if neighbor in path and neighbor not in visited:
                visited.append(neighbor)
                solution[neighbor] = (x, y)
                blue.goto(neighbor)
                blue.stamp()

                new_cost = costs[(x, y)] + 1
                costs[neighbor] = new_cost

                if algorithm == "greedy":
                    priority = heuristic(neighbor, (end_x, end_y))
                else:
                    priority = new_cost + heuristic(neighbor, (end_x, end_y))

                heapq.heappush(frontier, (priority, new_cost, neighbor))
                green.goto(x, y)
                green.stamp()

# Setup maze
def setup_maze(grid):
    global start_x, start_y, end_x, end_y
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            char = grid[y][x]
            screen_x = -588 + (x * 24)
            screen_y = 288 - (y * 24)

            if char == "+":
                maze.goto(screen_x, screen_y)
                maze.stamp()
                walls.append((screen_x, screen_y))
            elif char == " ":
                path.append((screen_x, screen_y))
            elif char == "e":
                end_x, end_y = screen_x, screen_y
                yellow.goto(screen_x, screen_y)
                yellow.stamp()
                path.append((screen_x, screen_y))
            elif char == "s":
                start_x, start_y = screen_x, screen_y
                red.goto(screen_x, screen_y)
                red.stamp()
                path.append((screen_x, screen_y))

# Initialize
maze = Maze()
red = Red()
blue = Blue()
green = Green()
yellow = Yellow()
walls, path, visited = [], [], []
solution = {}

# Get user input
choice = wn.textinput("Choose Algorithm", "Enter 'greedy' or 'astar':").strip().lower()
if choice not in ("greedy", "astar"):
    print("Invalid input! Defaulting to A* Search.")
    choice = "astar"

# Run
setup_maze(grid1)
solve(algorithm=choice)

# Save image
wn.getcanvas().postscript(file="maze_solution.eps")

# Finish
wn.exitonclick()
