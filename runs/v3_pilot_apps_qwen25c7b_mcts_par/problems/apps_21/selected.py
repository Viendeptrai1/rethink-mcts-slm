def max_distance(n, a):
    min_val = min(a)
    max_val = max(a)
    min_index = a.index(min_val)
    max_index = a.index(max_val)
    
    # Calculate initial distance
    initial_distance = abs(min_index - max_index)
    
    # Try swapping the minimum value with every other value
    max_distance = initial_distance
    for i in range(n):
        if i != min_index:
            new_distance = abs(i - max_index)
            if new_distance > max_distance:
                max_distance = new_distance
    
    # Try swapping the maximum value with every other value
    for i in range(n):
        if i != max_index:
            new_distance = abs(min_index - i)
            if new_distance > max_distance:
                max_distance = new_distance
    
    return max_distance

# Input handling
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Output the result
print(max_distance(n, a))