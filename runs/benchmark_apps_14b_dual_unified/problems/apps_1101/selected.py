import sys

def min_max_distance(n, k, rooms):
    # Find all indices of free rooms
    free_rooms = [i for i in range(n) if rooms[i] == '0']
    
    # Initialize the minimum possible maximum distance
    min_max_dist = float('inf')
    
    # Iterate over all possible starting points for the block of k+1 rooms
    for i in range(len(free_rooms) - k):
        leftmost = free_rooms[i]
        rightmost = free_rooms[i + k]
        middle = free_rooms[i + k // 2]
        
        # Calculate the maximum distance from the middle room to either end
        max_dist = max(middle - leftmost, rightmost - middle)
        
        # Update the minimum possible maximum distance
        min_max_dist = min(min_max_dist, max_dist)
    
    return min_max_dist

# Read input from standard input
n, k = map(int, sys.stdin.readline().split())
rooms = sys.stdin.readline().strip()

# Calculate and print the result
print(min_max_distance(n, k, rooms))