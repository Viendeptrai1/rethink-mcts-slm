def min_actions_to_sort_train(n, p):
    # Create a list of tuples where each tuple is (value, original_index)
    indexed_p = [(p[i], i) for i in range(n)]
    # Sort the list based on the value of the cars
    sorted_p = sorted(indexed_p, key=lambda x: x[0])
    
    # Initialize variables
    actions = 0
    visited = [False] * n
    
    for i in range(n):
        if not visited[i]:
            cycle_size = 0
            x = i
            
            while not visited[x]:
                visited[x] = True
                x = sorted_p[x][1]
                cycle_size += 1
            
            if cycle_size > 0:
                actions += (cycle_size - 1)
    
    return actions

# Input handling
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
p = list(map(int, data[1:]))

# Output the result
print(min_actions_to_sort_train(n, p))