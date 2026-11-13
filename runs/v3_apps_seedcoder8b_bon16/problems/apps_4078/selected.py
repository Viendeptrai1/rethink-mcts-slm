def maximize_difference(n, m, a, segments):
    from collections import defaultdict
    
    # This will keep track of the net effect of each segment on different points
    effect = [0] * (n + 1)
    
    for i, (l, r) in enumerate(segments, 1):
        effect[l - 1] -= 1
        effect[r] += 1
    
    # This will calculate the prefix sum which will give us the value of array b
    b = [0] * n
    current_effect = 0
    for i in range(n):
        current_effect += effect[i]
        b[i] = a[i] + current_effect
    
    # Find max and min of the array b
    max_b = max(b)
    min_b = min(b)
    
    # The answer is the maximum possible difference
    max_difference = max_b - min_b
    
    # We can always choose no segments, achieving a difference of 0
    applied_segments = []
    
    print(max_difference)
    print(len(applied_segments))
    if applied_segments:
        print(" ".join(map(str, applied_segments)))

# Example usage
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
a = list(map(int, data[2:n+2]))
segments = []
index = n + 2
for _ in range(m):
    l = int(data[index])
    r = int(data[index + 1])
    segments.append((l, r))
    index += 2

maximize_difference(n, m, a, segments)