import sys
from collections import defaultdict, deque

def min_swaps_to_sort(n, m, permutation, allowed_swaps):
    # Create a graph where each node is a position in the permutation
    graph = defaultdict(list)
    
    # Build the graph based on allowed swaps
    for a, b in allowed_swaps:
        graph[a-1].append(b-1)
        graph[b-1].append(a-1)
    
    # Function to find the connected component of a given node
    def bfs(start):
        queue = deque([start])
        visited = set()
        component = []
        
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                component.append(node)
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        
        return component
    
    # Find all connected components in the graph
    components = []
    visited = set()
    
    for i in range(n):
        if i not in visited:
            component = bfs(i)
            components.append(component)
            visited.update(component)
    
    # Calculate the minimum swaps needed for each component
    total_swaps = 0
    
    for component in components:
        # Create a mapping from value to index in the current component
        value_to_index = {permutation[i]: i for i in component}
        
        # Create a sorted version of the current component
        sorted_component = sorted(permutation[i] for i in component)
        
        # Count the number of swaps needed to sort the current component
        swaps = 0
        for i in range(len(component)):
            while sorted_component[i] != permutation[component[i]]:
                target_index = value_to_index[sorted_component[i]]
                # Swap the values in the permutation
                permutation[component[i]], permutation[target_index] = permutation[target_index], permutation[component[i]]
                # Update the mapping
                value_to_index[permutation[component[i]]] = component[i]
                value_to_index[permutation[target_index]] = target_index
                swaps += 1
        
        total_swaps += swaps
    
    return total_swaps

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
permutation = list(map(int, data[2:2+n]))
allowed_swaps = [(int(data[2+n+2*i]), int(data[2+n+2*i+1])) for i in range(m)]

# Calculate and print the result
result = min_swaps_to_sort(n, m, permutation, allowed_swaps)
print(result)