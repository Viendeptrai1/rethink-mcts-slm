def min_distance_to_cows(n, k, rooms):
    # List to store the positions of free rooms
    free_rooms = [i for i in range(n) if rooms[i] == '0']
    
    # Function to check if it's possible to place k+1 cows with max distance `max_dist`
    def can_place_cows(max_dist):
        count = 0
        last_position = -1
        for i in free_rooms:
            if last_position == -1 or i - last_position >= max_dist:
                count += 1
                last_position = i
                if count > k:
                    return False
        return count >= k + 1
    
    # Binary search for the minimum possible maximum distance
    left, right = 0, n
    while left < right:
        mid = (left + right) // 2
        if can_place_cows(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
rooms = data[2]

# Output the result
print(min_distance_to_cows(n, k, rooms))