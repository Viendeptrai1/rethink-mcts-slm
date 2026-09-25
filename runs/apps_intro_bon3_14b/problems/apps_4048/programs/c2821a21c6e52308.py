import sys

def min_moves_to_reach_n(N):
    # Initialize the starting point
    i = 1
    j = 1
    moves = 0
    
    # Move right until the product is greater than or equal to N
    while i * j < N:
        if i <= j:
            i += 1
        else:
            j += 1
        moves += 1
    
    # If the product is exactly N, return the number of moves
    if i * j == N:
        return moves
    
    # Otherwise, we need one more move to reach a square containing N
    return moves + 1

# Read input from standard input
N = int(sys.stdin.read().strip())

# Calculate and print the result
print(min_moves_to_reach_n(N))