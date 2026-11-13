def reverse_sequence_operations(n, a):
    b = []
    for i in range(n-1, -1, -1):
        b.append(a[i])
        b.reverse()
    return b

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
n = int(data[0])
a = list(map(int, data[1:]))

# Get result
result = reverse_sequence_operations(n, a)

# Print result
print(' '.join(map(str, result)))