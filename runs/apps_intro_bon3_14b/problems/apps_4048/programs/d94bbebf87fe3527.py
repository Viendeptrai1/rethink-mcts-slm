import sys

def min_moves_to_reach_N(N):
    # Initialize the starting point
    i, j = 1, 1
    moves = 0
    
    # Move diagonally as much as possible
    while i * j < N:
        if i <= j:
            i += 1
        else:
            j += 1
        moves += 1
    
    # Now we are at a point where i * j >= N
    # We need to move horizontally or vertically to reach exactly N
    while i * j > N:
        if i > j:
            i -= 1
        else:
            j -= 1
        moves += 1
    
    return moves

# Read input
N = int(sys.stdin.read().strip())

# Calculate and print the result
print(min_moves_to_reach_N(N))