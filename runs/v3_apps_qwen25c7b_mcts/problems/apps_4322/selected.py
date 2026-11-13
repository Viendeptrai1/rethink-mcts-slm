def max_balanced_circle(n, heights):
    heights.sort()
    max_length = 1
    start_index = 0
    current_start = 0
    
    for i in range(1, n):
        if heights[i] - heights[i - 1] > 1:
            if i - current_start > max_length:
                max_length = i - current_start
                start_index = current_start
            current_start = i
    
    if n - current_start > max_length:
        max_length = n - current_start
        start_index = current_start
    
    result = heights[start_index:start_index + max_length]
    return max_length, result

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
heights = list(map(int, data[1:]))

# Output
k, res = max_balanced_circle(n, heights)
print(k)
print(*res)