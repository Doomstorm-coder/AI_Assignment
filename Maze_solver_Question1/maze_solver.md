
#  Maze Solver with Turtle Graphics and A*/Greedy Algorithm

This Python program uses the Turtle graphics module to **visualize a maze-solving algorithm** (either Greedy Best-First Search or A* Search). The maze is built from a text grid, and the solution path is displayed as the algorithm explores the space.

---

##  Imports

```python
import turtle
import time
import heapq
```

- `turtle`: Used for graphical drawing.
- `time`: (Not actively used here) Could be used for delays or timing.
- `heapq`: Provides a priority queue for efficient search algorithms (used in A* and Greedy).

---

##  Screen Setup

```python
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("A Maze Solving Program")
wn.setup(1300, 700)
```

- Sets up a black canvas using Turtle for drawing the maze.
- `wn.setup()` defines the window size.

---

##  Turtle Classes for Maze Elements

These are custom Turtle objects for different parts of the maze:

```python
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
        self.speed(0)    # Goal point and final path
    ...
```

Each class defines a turtle with a shape and color appropriate for its role in the maze.

---

##  Maze Grid Layout

```python
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
```

- A 2D grid where:
  - `"+"` = Wall
  - `" "` = Walkable path
  - `"s"` = Start
  - `"e"` = End (goal)

---

## Heuristic Function

```python
def heuristic(cell, goal):
    x1, y1 = cell
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)
```

- Calculates **Manhattan distance** between two points.
- Used by Greedy and A* to estimate how far a cell is from the goal.

---

## Backtracking the Path

```python
def backRoute(x, y):
    yellow.goto(x, y)
    yellow.stamp()
    while (x, y) != (start_x, start_y):
        x, y = solution[x, y]
        yellow.goto(x, y)
        yellow.stamp()
```

- Starts at the goal and **traces the path backwards** using a `solution` dictionary.
- Marks the final path with yellow circles.

---

## Maze-Solving Function

```python
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
```

This is the core of the program:
- Uses a **priority queue** (via `heapq`) to choose the next best cell.
- Supports:
  - `greedy`: Only considers how close a cell is to the goal.
  - `astar`: Considers both distance from start and to goal.
- Explores neighbors in 4 directions (up, down, left, right).
- Uses blue squares to show visited nodes and green squares to show the frontier.

---

##  Maze Setup

```python
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
```

- Reads the `grid1` and:
  - Draws walls (white squares)
  - Identifies walkable paths
  - Marks start and end positions

---

## ⚙️ Initialization & Execution

```python
maze = Maze()
red = Red()
...
```

- Initializes all turtles.
- Collects wall and path data.
- Asks the user to choose between `'greedy'` or `'astar'`.

```python
choice = wn.textinput(...)
```

- If invalid input is given, it defaults to A*.

```python
setup_maze(grid1)
solve(algorithm=choice)
```

- Sets up the maze and runs the solver.

```python
wn.getcanvas().postscript(file="maze_solution.eps")
wn.exitonclick()
```

- Saves the final solution image as `.eps`.
- Waits for a mouse click to exit.

---

### Summary

This code:
- Loads a maze from a grid,
- Uses a pathfinding algorithm (Greedy or A*),
- Animates the search process and solution using Turtle graphics.
