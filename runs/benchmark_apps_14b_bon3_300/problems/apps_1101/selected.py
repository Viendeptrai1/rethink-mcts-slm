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
    
    # The maximum distance will be minimized by placing cows in the largest gaps first
    # We need to find the smallest gap that can accommodate k+1 cows
    max_distance = 0
    for i in range(k):
        max_distance = max(max_distance, (gaps[i] + 1) // 2)
    
    return max_distance

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
rooms = data[2]

# Calculate and print the result
print(min_max_distance(n, k, rooms))