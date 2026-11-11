import sys

def min_max_distance(n, k, rooms):
    # Find all indices of free rooms
    free_rooms = [i for i in range(n) if rooms[i] == '0']
    
    # We need to place k+1 cows in these free rooms
    # To minimize the maximum distance, we should try to distribute them evenly
    # Calculate the gaps between free rooms
    gaps = []
    for i in range(1, len(free_rooms)):
        gaps.append(free_rooms[i] - free_rooms[i-1] - 1)
    
    # Sort gaps in descending order
    gaps.sort(reverse=True)
    
    # The largest gap will determine the maximum distance
    # We can place k cows in the gaps such that the maximum distance is minimized
    # The number of gaps we can use is len(gaps) - k
    max_distance = (gaps[len(gaps) - k] + 1) // 2
    
    return max_distance

# Read input
n, k = map(int, sys.stdin.readline().split())
rooms = sys.stdin.readline().strip()

# Output the result
print(min_max_distance(n, k, rooms))