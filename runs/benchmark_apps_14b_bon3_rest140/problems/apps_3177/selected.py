import sys
from collections import defaultdict

def min_swaps_to_sort(n, m, permutation, allowed_swaps):
    # Create a graph where each node is connected to its allowed swap partners
    graph = defaultdict(list)
    for a, b in allowed_swaps:
        graph[a].append(b)
        graph[b].append(a)
    
    # Function to find the cycle length starting from node `start`
    def find_cycle_length(start, visited):
        stack = [(start, 0)]
        while stack:
            node, depth = stack.pop()
            if node == start and depth > 0:
                return depth
            if node not in visited:
                visited.add(node)
                for neighbor in graph[node]:
                    stack.append((neighbor, depth + 1))
        return 0
    
    # Find all cycles in the graph
    visited = set()
    total_swaps = 0
    for i in range(1, n + 1):
        if i not in visited:
            cycle_length = find_cycle_length(i, visited)
            if cycle_length > 0:
                total_swaps += (cycle_length - 1)
    
    return total_swaps

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
permutation = list(map(int, data[2:2+n]))
allowed_swaps = [(int(data[2+n+2*i]), int(data[2+n+2*i+1])) for i in range(m)]

# Output the result
print(min_swaps_to_sort(n, m, permutation, allowed_swaps))