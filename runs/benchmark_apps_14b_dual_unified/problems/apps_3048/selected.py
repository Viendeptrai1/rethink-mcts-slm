import sys
from collections import defaultdict

def count_optimal_paths_of_length_2(N, edges):
    # Build the adjacency list
    adj_list = defaultdict(list)
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    
    # Function to perform DFS and count paths of length 2
    def dfs(node, parent):
        count = 0
        for neighbor in adj_list[node]:
            if neighbor != parent:
                for next_neighbor in adj_list[neighbor]:
                    if next_neighbor != node and next_neighbor != neighbor:
                        count += 1
        return count
    
    total_count = 0
    for i in range(1, N + 1):
        total_count += dfs(i, -1)
    
    return total_count

# Read input
input = sys.stdin.read
data = input().split()
N = int(data[0])
edges = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N-1)]

# Calculate and print the result
result = count_optimal_paths_of_length_2(N, edges)
print(result)