
# Q-Learning in GridWorld

This project simulates a **5x5 GridWorld** where an agent learns the optimal policy using **Q-learning**. Special transitions (teleportation) and rewards are assigned to specific cells, encouraging the agent to learn effective behavior through exploration.

---

## Imports and Constants

```python
import numpy as np
import random
import tkinter as tk
```
- **NumPy**: For handling value function matrices.
- **Random**: For action selection and environment randomness.
- **Tkinter**: To visualize the learned policy and value function.

---

###  Environment Configuration

```python
GRID_SIZE = 5
A, A_PRIME = (0, 1), (4, 1)
B, B_PRIME = (0, 3), (2, 3)
A_REWARD, B_REWARD = 10, 5
ACTIONS = ['N', 'S', 'E', 'W']
```
- Defines a **5x5 grid**.
- States `A` and `B` are **teleportation cells**:
  - Stepping into `A` takes the agent to `A'` with a reward of **+10**.
  - Stepping into `B` moves the agent to `B'` with a reward of **+5**.
- Movement actions: North, South, East, West.

---

## Environment Transition Function

```python
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
```
- Implements **transition dynamics**.
- If the agent is on A or B, it is teleported with a reward.
- Otherwise, it moves normally unless it hits a wall (getting a penalty of -1).

---

## Action Selection: Epsilon-Greedy Policy

```python
def epsilon_greedy(Q, state):
        if random.random() < EPSILON:
        return random.choice(ACTIONS)
    else:
        max_q = max(Q[state].values())
        return random.choice([a for a in ACTIONS if Q[state][a] == max_q])
```
- Uses **ε-greedy policy** for exploration:
  - With probability `ε`, selects a random action.
  - Otherwise, selects the action with the highest Q-value.

---

## Q-Table Initialization

```python
def initialize_Q():
    return { (i, j): {a: 0.0 for a in ACTIONS} for i in range(GRID_SIZE) for j in range(GRID_SIZE) }
```
- Creates a Q-table for each state-action pair initialized to **0.0**.

---

## Q-Learning Algorithm

```python
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
```
- Runs the learning loop for a number of **episodes**.
- Each episode:
  - Picks a random starting state.
  - Performs **one step** (single-step episodes).
  - Updates Q-values using:
    \\[
    Q(s, a) \leftarrow Q(s, a) + \alpha (r + \gamma \max_{a'} Q(s', a') - Q(s, a))
    \\]

---

## Extracting Value Function & Optimal Policy

```python
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
```
- For each cell in the grid:
  - Finds the action with the highest Q-value.
  - Uses this to:
    - Compute the **value function** `V(s)`.
    - Assign an **arrow** as the policy (`↑`, `→`, etc.).

---

## Result Printing

```python
def print_results(V, policy):
       print("Evaluating optimal value function and policy...")
    print("Optimal Value Function:")
    for row in V:
        print(" ".join(f"{val:5.2f}" for val in row))
    print("Optimal Policy (arrows):")
    for row in policy:
        print(" ".join(row))
```
- Nicely prints:
  - The learned value function.
  - The learned policy using arrows.

---

## GUI Display with Tkinter

```python
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
```
- Displays the GridWorld visually:
  - Each cell shows:
    - Its **value**.
    - The **optimal action** (as an arrow).
  - Special cells `A`, `B`, `A'`, `B'` are color-highlighted.

---

## Main Execution

```python
if __name__ == "__main__":
    ...
```
- Trains the agent using Q-learning.
- Extracts and prints the optimal value function and policy.
- Launches the **Tkinter GUI**.

---

## Summary

- **Goal**: Learn an optimal policy in a grid with special rewards and transitions.
- **Algorithm**: Q-learning with ε-greedy exploration.
- **Output**: Optimal value function and action policy, visualized in a GUI.
