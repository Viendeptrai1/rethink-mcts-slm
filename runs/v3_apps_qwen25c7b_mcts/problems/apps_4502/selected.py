from collections import deque
import sys

def process_sequence(n, a):
    b = deque()
    for x in a:
        b.append(x)
        b.reverse()
    return list(b)

# Read input
input = sys.stdin.read
data = input().split()

# Parse input
n = int(data[0])
a = list(map(int, data[1:]))

# Process the sequence
result = process_sequence(n, a)

# Print the result
print(' '.join(map(str, result)))