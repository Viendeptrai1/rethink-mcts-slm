def shortest_distances_to_zeroes(n, a):
    left_min_distance = [float('inf')] * n
    right_min_distance = [float('inf')] * n
    
    min_dist = float('inf')
    for i in range(n):
        if a[i] == 0:
            min_dist = 0
        else:
            min_dist += 1
        left_min_distance[i] = min_dist
    
    min_dist = float('inf')
    for i in range(n-1, -1, -1):
        if a[i] == 0:
            min_dist = 0
        else:
            min_dist += 1
        right_min_distance[i] = min_dist
    
    result = []
    for i in range(n):
        result.append(min(left_min_distance[i], right_min_distance[i]))
    
    return result

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

result = shortest_distances_to_zeroes(n, a)
print(" ".join(map(str, result)))