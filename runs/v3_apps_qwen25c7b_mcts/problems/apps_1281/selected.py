def max_segments(n, k, a):
    # Initialize variables
    max_segments = 0
    current_xor = 0
    
    # Iterate through the array to find potential flip points
    for i in range(1, n):
        current_xor ^= a[i]
        if current_xor != 0:
            max_segments += 1
    
    # Each element can also form a segment by itself
    max_segments += n
    
    return max_segments

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Calculate and print the result
result = max_segments(n, k, a)
print(result)