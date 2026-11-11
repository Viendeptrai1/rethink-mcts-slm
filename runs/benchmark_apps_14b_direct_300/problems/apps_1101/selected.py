import sys

def min_max_distance(n, k, rooms):
    # Find all the indices of the unoccupied rooms
    free_rooms = [i for i in range(n) if rooms[i] == '0']
    
    # We need to place k+1 cows in these free rooms
    # We want to minimize the maximum distance between any two cows
    # This can be done by placing the cows as evenly as possible
    
    # Calculate the gaps between the free rooms
    gaps = [free_rooms[i+1] - free_rooms[i] for i in range(len(free_rooms) - 1)]
    
    # Sort the gaps in descending order
    gaps.sort(reverse=True)
    
    # The maximum distance will be minimized by reducing the largest gap
    # We need to reduce the largest gap by at least (k+1) // 2
    max_gap = gaps[0]
    min_max_dist = (max_gap + (k + 1)) // (k + 1)
    
    return min_max_dist

# Read input
n, k = map(int, sys.stdin.readline().split())
rooms = sys.stdin.readline().strip()

# Output the result
print(min_max_distance(n, k, rooms))