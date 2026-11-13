from collections import Counter
import sys

def find_valid_positions(n, m, p, a, b):
    count_b = Counter(b)
    valid_positions = []
    
    for q in range(1, n - m * p + 2):
        if Counter(a[q-1:q+m*p-1:p]) == count_b:
            valid_positions.append(q)
    
    return len(valid_positions), valid_positions

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
p = int(data[2])

a = list(map(int, data[3:3+n]))
b = list(map(int, data[3+n:]))

# Find valid positions
result_count, result_positions = find_valid_positions(n, m, p, a, b)

# Print results
print(result_count)
print(" ".join(map(str, result_positions)))