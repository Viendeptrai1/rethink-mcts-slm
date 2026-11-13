def max_diff_segments(n, m, a, segments):
    # Calculate the initial differences
    diff = max(a) - min(a)
    
    # Initialize variables to track the best result
    best_diff = diff
    best_segments = []
    
    # Try all subsets of segments
    for i in range(1 << m):
        current_diff = diff
        selected_segments = []
        
        # Check which segments are in the current subset
        for j in range(m):
            if i & (1 << j):
                l, r = segments[j]
                for k in range(l - 1, r):
                    a[k] -= 1
                selected_segments.append(j + 1)
        
        # Update the current difference
        current_diff = max(a) - min(a)
        
        # If the current difference is better, update the best result
        if current_diff > best_diff:
            best_diff = current_diff
            best_segments = selected_segments
        
        # Revert the changes for the next iteration
        for j in range(m):
            if i & (1 << j):
                l, r = segments[j]
                for k in range(l - 1, r):
                    a[k] += 1
    
    return best_diff, len(best_segments), best_segments

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
a = list(map(int, data[2:2+n]))
segments = []

for i in range(2+n, 2+n+m*2, 2):
    l = int(data[i])
    r = int(data[i+1])
    segments.append((l, r))

# Solve the problem
best_diff, q, best_segments = max_diff_segments(n, m, a, segments)

# Print the result
print(best_diff)
print(q)
print(' '.join(map(str, best_segments)))