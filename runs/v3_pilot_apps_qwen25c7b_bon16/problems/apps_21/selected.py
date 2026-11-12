def max_distance_after_swap(n, a):
    min_index = a.index(1)
    max_index = a.index(n)
    
    # Calculate the initial distance
    initial_distance = abs(min_index - max_index)
    
    # Try swapping the minimum with all other elements and calculate distances
    max_distance = initial_distance
    for i in range(n):
        if i != min_index:
            new_distance = abs(i - max_index)
            if new_distance > max_distance:
                max_distance = new_distance
    
    # Try swapping the maximum with all other elements and calculate distances
    for i in range(n):
        if i != max_index:
            new_distance = abs(min_index - i)
            if new_distance > max_distance:
                max_distance = new_distance
    
    return max_distance

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

# Output the result
print(max_distance_after_swap(n, a))