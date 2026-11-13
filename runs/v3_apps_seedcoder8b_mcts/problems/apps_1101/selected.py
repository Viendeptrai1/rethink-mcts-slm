def minimum_distance(n, k, rooms):
    # Find all the positions of free rooms
    free_rooms = [i for i in range(n) if rooms[i] == '0']
    
    # Initialize the minimum possible maximum distance
    min_max_distance = float('inf')
    
    # Iterate over all possible starting positions for Farmer John's room
    for i in range(len(free_rooms) - k):
        # Get the k+1 consecutive free rooms starting from position i
        selected_rooms = free_rooms[i:i + k + 1]
        
        # Calculate the distance from Farmer John's room to the farthest cow
        # The middle room among the selected k+1 rooms is the best choice
        farmer_room = selected_rooms[k // 2]
        max_distance = max(abs(farmer_room - selected_rooms[0]), abs(farmer_room - selected_rooms[-1]))
        
        # Update the minimum possible maximum distance
        min_max_distance = min(min_max_distance, max_distance)
    
    return min_max_distance

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
rooms = data[2]

# Output the result
print(minimum_distance(n, k, rooms))