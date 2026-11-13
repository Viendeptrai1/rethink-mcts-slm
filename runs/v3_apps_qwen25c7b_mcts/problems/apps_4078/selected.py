def max_range_after_segments(n, m, a, segments):
    # Calculate the effect of each segment on the array
    effects = []
    for i, (l, r) in enumerate(segments):
        min_val = min(a[l-1:r])
        max_val = max(a[l-1:r])
        effects.append((i+1, max_val - min_val))

    # Sort segments by their impact on the array
    effects.sort(key=lambda x: x[1], reverse=True)

    # Select the top k segments that maximize the range
    selected_segments = []
    current_min = float('inf')
    current_max = float('-inf')
    for _, diff in effects:
        if diff == 0:
            continue
        if current_min > diff or current_max < diff:
            selected_segments.append(effects[effects.index((_, diff))][0])
            current_min = min(current_min, diff)
            current_max = max(current_max, diff)

    # Calculate the final array after applying the selected segments
    b = list(a)
    for l, r in segments:
        if l in selected_segments or r in selected_segments:
            for i in range(l-1, r):
                b[i] -= 1

    # Calculate the maximum possible value of the range of b
    d = max(b) - min(b)

    return d, len(selected_segments), selected_segments

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
a = list(map(int, data[2:2+n]))
segments = [(int(data[2+n+2*i])-1, int(data[2+n+2*i+1])) for i in range(m)]

# Solve the problem
result = max_range_after_segments(n, m, a, segments)

# Print the result
print(result[0])
print(result[1])
print(*result[2])