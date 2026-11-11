import sys

def max_participants(n, k, preferences):
    # Create a graph where each node points to its dependent node
    graph = {i+1: preferences[i] for i in range(n)}
    
    # Create a reverse graph to find all nodes pointing to a particular node
    reverse_graph = {}
    for i in range(1, n+1):
        if graph[i] not in reverse_graph:
            reverse_graph[graph[i]] = []
        reverse_graph[graph[i]].append(i)
    
    # Initialize a set to keep track of visited nodes
    visited = set()
    
    # Initialize a counter for the number of participants that can join
    count = 0
    
    # Iterate over each node
    for i in range(1, n+1):
        if i not in visited:
            # Perform a DFS to find all nodes in the current component
            stack = [i]
            component = []
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    component.append(node)
                    if node in reverse_graph:
                        stack.extend(reverse_graph[node])
            
            # Check if we can add the entire component to the trip
            if len(component) <= k:
                count += len(component)
                k -= len(component)
    
    return count

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
preferences = list(map(int, data[2:]))

# Print the result
print(max_participants(n, k, preferences))