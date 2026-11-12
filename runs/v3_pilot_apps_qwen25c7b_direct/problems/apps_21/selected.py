def max_distance_after_one_swap(n, a):
    min_index = a.index(1)
    max_index = a.index(n)
    
    # Calculate initial distance
    initial_distance = abs(min_index - max_index)
    
    # Try swapping the minimum with all other elements except itself
    max_distance = initial_distance
    for i in range(n):
        if i != min_index:
            new_distance = abs(i - max_index)
            if new_distance > max_distance:
                max_distance = new_distance
    
    # Try swapping the maximum with all other elements except itself
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

# Output result
print(max_distance_after_one_swap(n, a))