def max_difference(n, m, a, segments):
    # Initialize variables
    max_diff = 0
    best_segments = []
    
    # Iterate over all possible subsets of segments
    for i in range(1 << m):
        diff = 0
        selected_segments = []
        for j in range(m):
            if i & (1 << j):
                diff += sum(a[l-1:r]) for l, r in segments[j])
                selected_segments.append(j+1)
        
        # Calculate the current difference
        current_max = max(a)
        current_min = min(a)
        for l, r in segments:
            current_max -= diff * (r - l + 1)
            current_min -= diff * (r - l + 1)
        
        # Update the maximum difference and best segments
        if current_max - current_min > max_diff:
            max_diff = current_max - current_min
            best_segments = selected_segments
    
    return max_diff, len(best_segments), best_segments

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
a = list(map(int, data[2:2+n]))
segments = []

for i in range(m):
    l = int(data[2+n+i*2]) - 1
    r = int(data[2+n+i*2+1]) - 1
    segments.append((l, r))

# Get the result
result = max_difference(n, m, a, segments)

# Print the result
print(result[0])
print(result[1])
print(' '.join(map(str, result[2])))