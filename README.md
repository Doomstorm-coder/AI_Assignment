AI Group Assignment

Tech Titans

1. Question 1: Search Algorithms - Informed Search
   Folder:Maze_solver_Question1

Implement Greedy Best-First Search and A* to find the shortest path in a maze.
Key components:
~Maze class to parse the file and define valid moves.
~Node class for storing state, parent, action, and cost.
~Solve(algorithm="greedy" or "astar") for the main logic.

Visual output using matplotlib or Pillow.

2. Question 2:CSP-Travel Salesperson Problem: Simulated Annealing
   Folder: Question2/Question2

Solve the TSP across 10 major Namibian towns using Simulated Annealing.
Key components:
~TSP class for route and distance handling.
~SimulatedAnnealingSolver class for optimization logic.
~Output includes visual comparison of the initial vs final routes.

3.Question 3: Adversarial Search
  Folder:Part3/tic tac toe

Implement an unbeatable Tic Tac Toe AI using the Minimax algorithm.
Key components:
player(), actions(), result(), winner(), terminal(), and minimax().
Ensure all board states are immutable for accurate simulations.

4. Question 4: MDPs – Q-learning
Folder:Question4

Implement a Q-learning agent to solve a 5x5 Gridworld MDP with special teleporting states and rewards.
Key components:
~Grid setup with states, actions, and rewards
~Q-table initialization and updates using: Q[s][a] += α(r + γ max Q[s'] − Q[s][a])
~ε-greedy action selection (ε = 0.1)
~Special transitions: A → A′ (+10), B → B′ (+5)
~Parameters: γ = 0.9, α = 0.2, 5000 episodes
~Output: optimal value function and policy

Contributors
Jerome Nanuseb 223033030 
Milu Simau 223035203 
Kristofina Shipalanga 223076147 
Orilio Naobeb 223077593 
Simeon Makili  223085456


NOTE: THE Final Notebook and PDF of the Notebook are also on the repository



