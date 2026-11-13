import sys
from collections import defaultdict

def expected_time_to_escape(N, M, paths):
    # Create adjacency list representation of the graph
    adj_list = defaultdict(list)
    for K, L in paths:
        adj_list[K].append(L)
        adj_list[L].append(K)

    # Initialize distance array with infinity
    distances = [float('inf')] * N
    distances[0] = 0

    # Use BFS to find shortest path to all nodes
    queue = [0]
    while queue:
        current = queue.pop(0)
        for neighbor in adj_list[current]:
            if distances[neighbor] == float('inf'):
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    # Calculate expected time to escape
    total_time = 0
    num_simulations = 100000
    for _ in range(num_simulations):
        current = 0
        steps = 0
        visited = set()
        while current != N - 1:
            if current in visited:
                break
            visited.add(current)
            neighbors = adj_list[current]
            next_clearing = neighbors[steps % len(neighbors)]
            steps += 1
            current = next_clearing
        total_time += steps

    return total_time / num_simulations

# Read input
input = sys.stdin.read
data = input().split()

N = int(data[0])
M = int(data[1])

paths = []
index = 2
for _ in range(M):
    K = int(data[index])
    L = int(data[index + 1])
    paths.append((K, L))
    index += 2

# Calculate and print the expected time to escape
result = expected_time_to_escape(N, M, paths)
print(f"{result:.6f}")