import random
import math
import matplotlib.pyplot as plt

class TSP:
    def __init__(self, towns, distance_matrix):
        self.towns = towns
        self.distances = distance_matrix

    def total_distance(self, route):
        return sum(self.distances[route[i]][route[i+1]] for i in range(len(route) - 1))
        # Removed return to start (no circular route)

class SimulatedAnnealingSolver:
    def __init__(self, tsp, initial_temp=15000, cooling_rate=0.998, max_iter=20000):
        self.tsp = tsp
        self.temp = initial_temp
        self.cooling_rate = cooling_rate
        self.max_iter = max_iter

    def generate_initial_route(self):
        route = list(range(1, len(self.tsp.towns)))  # exclude Windhoek
        random.shuffle(route)
        return [0] + route  # start at Windhoek

    def swap_two_towns(self, route):
        a, b = random.sample(range(1, len(route)), 2)
        new_route = route[:]
        new_route[a], new_route[b] = new_route[b], new_route[a]
        return new_route

    def solve(self):
        current_route = self.generate_initial_route()
        current_cost = self.tsp.total_distance(current_route)
        best_route = current_route[:]
        best_cost = current_cost

        for _ in range(self.max_iter):
            new_route = self.swap_two_towns(current_route)
            new_cost = self.tsp.total_distance(new_route)
            delta = new_cost - current_cost

            if delta < 0 or random.random() < math.exp(-delta / self.temp):
                current_route = new_route
                current_cost = new_cost
                if new_cost < best_cost:
                    best_route = new_route
                    best_cost = new_cost

            self.temp *= self.cooling_rate

        return best_route, best_cost

# Approximate coordinates for plotting towns geographically
coordinates = {
    "Windhoek": (500, 500),
    "Swakopmund": (300, 450),
    "Walvis Bay": (280, 430),
    "Otjiwarongo": (520, 650),
    "Tsumeb": (650, 800),
    "Grootfontein": (700, 820),
    "Mariental": (520, 300),
    "Keetmanshoop": (580, 100),
    "Ondangwa": (730, 920),
    "Oshakati": (750, 940)
}

def plot_route(towns, route, title):
    x = [coordinates[towns[i]][0] for i in route]
    y = [coordinates[towns[i]][1] for i in route]

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='blue')

    for i in range(len(route)):
        town_name = towns[route[i]]
        plt.text(x[i]+5, y[i]+5, town_name, fontsize=9)

    # Mark start and end
    plt.scatter(x[0], y[0], color='green', s=100, label='Start')
    plt.scatter(x[-1], y[-1], color='red', s=100, label='End')
    plt.legend()

    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis("equal")
    plt.tight_layout()
    plt.show()

# --- 10 towns ---
towns = [
    "Windhoek", "Swakopmund", "Walvis Bay", "Otjiwarongo", "Tsumeb",
    "Grootfontein", "Mariental", "Keetmanshoop", "Ondangwa", "Oshakati"
]

distance_matrix = [
    [0, 361, 395, 249, 433, 459, 268, 497, 678, 712],
    [361, 0, 35.5, 379, 562, 589, 541, 859, 808, 779],
    [395, 35.5, 0, 413, 597, 623, 511, 732, 884, 855],
    [249, 379, 413, 0, 260, 183, 519, 768, 514, 485],
    [433, 562, 597, 260, 0, 60, 682, 921, 254, 288],
    [459, 589, 623, 183, 60, 0, 708, 947, 308, 342],
    [268, 541, 511, 519, 682, 708, 0, 231, 909, 981],
    [497, 859, 732, 768, 921, 947, 231, 0, 1175, 1210],
    [678, 808, 884, 514, 254, 308, 909, 1175, 0, 30],
    [712, 779, 855, 485, 288, 342, 981, 1210, 30, 0]
]

# Create TSP and Solver
tsp = TSP(towns, distance_matrix)
solver = SimulatedAnnealingSolver(tsp)

# Initial route
initial_route = solver.generate_initial_route()
initial_distance = tsp.total_distance(initial_route)
print("Initial Route:")
print(" -> ".join(towns[i] for i in initial_route))
print(f"Initial Distance: {initial_distance:.2f} km")
plot_route(towns, initial_route, "Initial Route (10 towns, No Return to Windhoek)")

# Optimized route
best_route, best_distance = solver.solve()
print("\nOptimized Route:")
print(" -> ".join(towns[i] for i in best_route))
print(f"Optimized Distance: {best_distance:.2f} km")
plot_route(towns, best_route, "Optimized Route (10 towns, No Return to Windhoek)")
