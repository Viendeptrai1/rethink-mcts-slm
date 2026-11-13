def earliest_not_so_rainy_day(n, x, y, a):
    left_max = [0] * n
    right_min = [float('inf')] * n
    
    max_val = float('-inf')
    for i in range(n):
        max_val = max(max_val, a[i])
        left_max[i] = max_val
    
    min_val = float('inf')
    for i in range(n-1, -1, -1):
        min_val = min(min_val, a[i])
        right_min[i] = min_val
    
    for i in range(x, n-y):
        if a[i] < left_max[i-x] and a[i] < right_min[i+y]:
            return i + 1
    
    return -1

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
x = int(data[1])
y = int(data[2])
a = list(map(int, data[3:]))

print(earliest_not_so_rainy_day(n, x, y, a))