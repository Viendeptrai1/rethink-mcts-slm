def min_distance(n, k, rooms):
    free_rooms = [i for i in range(n) if rooms[i] == '0']
    
    min_dist = float('inf')
    
    for i in range(len(free_rooms) - k):
        left_cow = free_rooms[i]
        right_cow = free_rooms[i + k]
        dist_to_left_cow = abs(left_cow - free_rooms[i + k // 2])
        dist_to_right_cow = abs(right_cow - free_rooms[i + k // 2])
        max_dist = max(dist_to_left_cow, dist_to_right_cow)
        min_dist = min(min_dist, max_dist)
    
    return min_dist

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
rooms = data[2]

print(min_distance(n, k, rooms))