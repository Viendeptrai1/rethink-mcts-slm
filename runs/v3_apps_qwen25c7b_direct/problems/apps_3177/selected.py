def min_swaps_to_sort(N, permutation, swaps):
    # Create a list of tuples where each tuple is (value, index)
    value_index = [(permutation[i], i) for i in range(N)]
    
    # Sort the list based on the values
    value_index.sort()
    
    # Initialize visited array to keep track of visited elements
    visited = [False] * N
    
    # Initialize result variable to store the number of swaps
    result = 0
    
    # Iterate through each element in the sorted list
    for i in range(N):
        # If the element is already visited or is already in the correct position
        if visited[i] or value_index[i][1] == i:
            continue
        
        # Find out the number of nodes in this cycle
        cycle_size = 0
        j = i
        
        while not visited[j]:
            # Mark node as visited
            visited[j] = True
            
            # Move to the next node
            j = value_index[j][1]
            cycle_size += 1
        
        # If there is a cycle of size k, we need (k-1) swaps to sort it
        if cycle_size > 0:
            result += (cycle_size - 1)
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
M = int(data[1])

permutation = list(map(int, data[2:N+2]))

swaps = []
index = N + 2
for _ in range(M):
    A = int(data[index]) - 1
    B = int(data[index + 1]) - 1
    swaps.append((A, B))
    index += 2

# Calculate and print the result
print(min_swaps_to_sort(N, permutation, swaps))