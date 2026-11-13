def max_balanced_circle_heights(n, heights):
    sorted_heights = sorted(heights)
    max_length = 0
    start_index = 0
    
    for i in range(n):
        current_length = 1
        while i + 1 < n and abs(sorted_heights[i] - sorted_heights[i + 1]) <= 1:
            i += 1
            current_length += 1
        if current_length > max_length:
            max_length = current_length
            start_index = i - current_length + 1
            
    result = sorted_heights[start_index:start_index + max_length]
    
    return max_length, result

import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
heights = list(map(int, data[1:]))

max_len, result = max_balanced_circle_heights(n, heights)

print(max_len)
print(' '.join(map(str, result)))