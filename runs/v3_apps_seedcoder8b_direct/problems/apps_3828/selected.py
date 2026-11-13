def min_moves_to_sort(n, p):
    # Create a list of tuples where each tuple is (value, index)
    indexed_p = [(value, index) for index, value in enumerate(p)]
    
    # Sort the list based on the values
    indexed_p.sort()
    
    # Initialize a visited array to keep track of visited elements
    visited = [False] * n
    
    # Initialize the number of moves
    moves = 0
    
    for i in range(n):
        # If the element is already visited or is already in the correct position
        if visited[i] or indexed_p[i][1] == i:
            continue
        
        # Find the cycle of misplaced elements
        cycle_size = 0
        j = i
        
        while not visited[j]:
            visited[j] = True
            j = indexed_p[j][1]
            cycle_size += 1
        
        # If there is a cycle of size k, we need k-1 swaps
        if cycle_size > 0:
            moves += cycle_size - 1
    
    return moves

# Read input
n = int(input())
p = list(map(int, input().split()))

# Calculate and print the result
result = min_moves_to_sort(n, p)
print(result)