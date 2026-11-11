import sys

def min_max_distance(n, k, rooms):
    # Find all indices of free rooms
    free_rooms = [i for i in range(n) if rooms[i] == '0']
    
    # Initialize the minimum possible distance to infinity
    min_distance = float('inf')
    
    # Iterate over each possible position for Farmer John
    for i in range(len(free_rooms) - k):
        # Calculate the maximum distance to the nearest cow for this position
        max_distance = (free_rooms[i + k] - free_rooms[i]) // 2
        # Update the minimum possible distance
        min_distance = min(min_distance, max_distance)
    
    return min_distance

# Read input from stdin
n, k = map(int, sys.stdin.readline().split())
rooms = sys.stdin.readline().strip()

# Print the result
print(min_max_distance(n, k, rooms))