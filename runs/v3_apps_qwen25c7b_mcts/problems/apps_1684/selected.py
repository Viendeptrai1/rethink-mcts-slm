import sys
from math import gcd

def is_rotationally_symmetrical(n, m, segments):
    def rotate_segment(a, b, k):
        return ((a - 1 + k) % n + 1, (b - 1 + k) % n + 1)

    def normalize(segment):
        return tuple(sorted(segment))

    original_segments = {normalize(segment) for segment in segments}
    
    for k in range(1, n):
        rotated_segments = {normalize(rotate_segment(a, b, k)) for a, b in segments}
        if rotated_segments == original_segments:
            return True
    
    return False

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

segments = []
index = 2
for _ in range(m):
    a = int(data[index])
    b = int(data[index + 1])
    segments.append((a, b))
    index += 2

# Output result
if is_rotationally_symmetrical(n, m, segments):
    print("Yes")
else:
    print("No")