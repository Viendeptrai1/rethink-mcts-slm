from collections import Counter
import sys

def max_rectangle_area(N, A):
    # Count occurrences of each stick length
    count = Counter(A)
    
    # Sort unique stick lengths
    lengths = sorted(count.keys())
    
    max_area = 0
    
    # Check all pairs of lengths
    for i in range(len(lengths)):
        for j in range(i + 1, len(lengths)):
            if lengths[i] * lengths[j] > max_area and count[lengths[i]] >= 2 and count[lengths[j]] >= 2:
                max_area = lengths[i] * lengths[j]
    
    return max_area

# Read input
input = sys.stdin.read
data = input().split()
N = int(data[0])
A = list(map(int, data[1:]))

# Calculate and print the result
print(max_rectangle_area(N, A))