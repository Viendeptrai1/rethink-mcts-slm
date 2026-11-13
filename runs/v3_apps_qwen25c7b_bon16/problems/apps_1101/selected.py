import sys

def min_distance_to_cow(n, k, rooms):
    # Convert the string of rooms into a list of indices where the rooms are free
    free_rooms = [i for i in range(n) if rooms[i] == '0']
    
    # Initialize the minimum distance to a large number
    min_distance = float('inf')
    
    # Iterate over all possible positions for Farmer John's room
    for i in range(len(free_rooms)):
        # Calculate the leftmost and rightmost bounds within the window of size k+1
        left_bound = max(0, i - k)
        right_bound = min(len(free_rooms), i + k + 1)
        
        # Find the maximum distance from Farmer John's room to any cow's room within this window
        distance_to_cows = max(abs(free_rooms[left_bound] - free_rooms[i]), abs(free_rooms[right_bound - 1] - free_rooms[i]))
        
        # Update the minimum distance found
        min_distance = min(min_distance, distance_to_cows)
    
    return min_distance

# Read input from stdin
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
rooms = data[2]

# Call the function and print the result
result = min_distance_to_cow(n, k, rooms)
print(result)