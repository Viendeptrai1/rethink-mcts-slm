def is_rotational_symmetry(n, m, segments):
    # Create a dictionary to store the adjacency list of the graph
    adj_list = {i: [] for i in range(1, n+1)}
    
    # Build the adjacency list based on the given segments
    for a, b in segments:
        adj_list[a].append(b)
        adj_list[b].append(a)
    
    # Check for rotational symmetry
    for k in range(1, n):
        # Create a new adjacency list by rotating the graph by k positions
        rotated_adj_list = {i: [] for i in range(1, n+1)}
        for node in range(1, n+1):
            for neighbor in adj_list[node]:
                rotated_node = (node + k - 1) % n + 1
                rotated_neighbor = (neighbor + k - 1) % n + 1
                rotated_adj_list[rotated_node].append(rotated_neighbor)
        
        # Check if the rotated graph is the same as the original graph
        if all(sorted(original_neighbors) == sorted(rotated_neighbors) for original_neighbors, rotated_neighbors in zip(adj_list.values(), rotated_adj_list.values())):
            return "Yes"
    
    return "No"

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
segments = [(int(data[2*i+2]), int(data[2*i+3])) for i in range(m)]

# Output result
print(is_rotational_symmetry(n, m, segments))