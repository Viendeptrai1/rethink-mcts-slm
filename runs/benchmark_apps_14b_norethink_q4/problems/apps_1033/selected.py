import sys

def min_spots(n, H):
    # If H is greater than or equal to n, we need at least H spots
    if H >= n:
        return H
    
    # Calculate the number of full levels we can have
    full_levels = (H * 2) // 3
    
    # Calculate the remaining sand after building full levels
    remaining_sand = n - (full_levels * (full_levels + 1)) // 2
    
    # If there is no remaining sand, we just need the full levels
    if remaining_sand == 0:
        return full_levels
    
    # If the remaining sand is less than or equal to the next level, we need one more spot
    if remaining_sand <= full_levels + 1:
        return full_levels + 1
    
    # Otherwise, we need one more spot for the remaining sand
    return full_levels + 2

# Read input
n, H = map(int, sys.stdin.read().split())

# Print the result
print(min_spots(n, H))