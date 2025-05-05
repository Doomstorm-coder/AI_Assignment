import numpy as np
import random
import tkinter as tk

# GridWorld parameters
GRID_SIZE = 5
A, A_PRIME = (0, 1), (4, 1)
B, B_PRIME = (0, 3), (2, 3)
A_REWARD, B_REWARD = 10, 5
ACTIONS = ['N', 'S', 'E', 'W']
ACTION_DELTAS = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
ARROWS = {'N': '↑', 'S': '↓', 'E': '→', 'W': '←'}

# Q-learning parameters
GAMMA = 0.9
EPSILON = 0.1
ALPHA = 0.2
EPISODES = 5000
STEPS_PER_EPISODE = 1  # Each episode is one step (simplified format)

def step(state, action):
    if state == A:
        return A_PRIME, A_REWARD
    elif state == B:
        return B_PRIME, B_REWARD

    delta = ACTION_DELTAS[action]
    new_row, new_col = state[0] + delta[0], state[1] + delta[1]
    if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
        return (new_row, new_col), 0
    else:
        return state, -1

def epsilon_greedy(Q, state):
    if random.random() < EPSILON:
        return random.choice(ACTIONS)
    else:
        max_q = max(Q[state].values())
        return random.choice([a for a in ACTIONS if Q[state][a] == max_q])

def initialize_Q():
    return { (i, j): {a: 0.0 for a in ACTIONS} for i in range(GRID_SIZE) for j in range(GRID_SIZE) }

def q_learning():
    print("Initializing Gridworld...")
    print(f"Grid size: {GRID_SIZE}x{GRID_SIZE}")
    print(f"Special_states = {{'A': {A}, 'B': {B}}}")
    print(f"Next_to_states = {{'A\\'': {A_PRIME}, 'B\\'': {B_PRIME}}}")
    print(f"Special_rewards = {{'A': {A_REWARD}, 'B': {B_REWARD}}}")
    print("Starting Q-learning with parameters:")
    print(f" γ = {GAMMA}")
    print(f" ε = {EPSILON}")
    print(f" α = {ALPHA}")
    print(f" Episodes = {EPISODES}")
    print(f"Steps = {EPISODES * STEPS_PER_EPISODE}")

    Q = initialize_Q()

    for _ in range(EPISODES):
        state = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        for _ in range(STEPS_PER_EPISODE):
            action = epsilon_greedy(Q, state)
            next_state, reward = step(state, action)
            max_next = max(Q[next_state].values())
            Q[state][action] += ALPHA * (reward + GAMMA * max_next - Q[state][action])
            state = next_state

    return Q

def extract_value_and_policy(Q):
    V = np.zeros((GRID_SIZE, GRID_SIZE))
    policy = np.full((GRID_SIZE, GRID_SIZE), '', dtype=object)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            state = (i, j)
            best_action = max(Q[state], key=Q[state].get)
            V[i, j] = Q[state][best_action]
            policy[i, j] = ARROWS[best_action]
    return V, policy

def print_results(V, policy):
    print("Evaluating optimal value function and policy...")
    print("Optimal Value Function:")
    for row in V:
        print(" ".join(f"{val:5.2f}" for val in row))
    print("Optimal Policy (arrows):")
    for row in policy:
        print(" ".join(row))

def display_gui(V, policy):
    root = tk.Tk()
    root.title("Q-Learning GridWorld Visualization")

    cell_size = 80
    canvas = tk.Canvas(root, width=GRID_SIZE * cell_size, height=GRID_SIZE * cell_size)
    canvas.pack()

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

            # Value function
            value = V[i][j]
            canvas.create_text(x1 + cell_size / 2, y1 + 20, text=f"{value:.2f}", font=("Helvetica", 12, "bold"))

            # Policy arrow
            arrow = policy[i][j]
            canvas.create_text(x1 + cell_size / 2, y1 + 50, text=arrow, font=("Helvetica", 20))

    # Highlight special states A, B, A', B'
    def mark_special(state, label, color):root = tk.Tk()
    root.title("Q-Learning GridWorld Visualization")

    cell_size = 80
    canvas = tk.Canvas(root, width=GRID_SIZE * cell_size, height=GRID_SIZE * cell_size)
    canvas.pack()

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

            # Value function
            value = V[i][j]
            canvas.create_text(x1 + cell_size / 2, y1 + 20, text=f"{value:.2f}", font=("Helvetica", 12, "bold"))

            # Policy arrow
            arrow = policy[i][j]
            canvas.create_text(x1 + cell_size / 2, y1 + 50, text=arrow, font=("Helvetica", 20))

        i, j = state
        x1, y1 = j * cell_size, i * cell_size
        canvas.create_text(x1 + cell_size / 2, y1 + cell_size / 2, text=label, font=("Helvetica", 16, "bold"), fill=color)

    mark_special(A, "A", "blue")
    mark_special(B, "B", "green")
    mark_special(A_PRIME, "A'", "blue")
    mark_special(B_PRIME, "B'", "green")

    root.mainloop()


if __name__ == "__main__":
    Q = q_learning()
    V, policy = extract_value_and_policy(Q)
    print_results(V, policy)
    display_gui(V, policy)
