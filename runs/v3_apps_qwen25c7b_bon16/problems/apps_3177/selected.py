def min_swaps_to_sort(N, permutation, swaps):
    # Create a list of tuples where each tuple is (value, index)
    value_index = [(permutation[i], i) for i in range(N)]
    
    # Sort the list based on the values to find the target positions
    sorted_value_index = sorted(value_index)
    
    # Initialize visited array to keep track of visited elements
    visited = [False] * N
    
    # Initialize the swap count
    swap_count = 0
    
    for i in range(N):
        # If the element is already visited or is already at the correct position
        if visited[i] or value_index[i][1] == sorted_value_index[i][1]:
            continue
        
        # Find the cycle size
        cycle_size = 0
        x = i
        
        while not visited[x]:
            # Mark the node as visited
            visited[x] = True
            
            # Move to the next node
            x = sorted_value_index[x][1]
            cycle_size += 1
        
        # If there is a cycle of size k, it will take (k - 1) swaps to sort it
        if cycle_size > 0:
            swap_count += (cycle_size - 1)
    
    return swap_count

# Example usage
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

print(min_swaps_to_sort(N, permutation, swaps))