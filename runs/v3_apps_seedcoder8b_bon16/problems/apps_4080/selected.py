def solve(n, m, a, segments):
    # Initialize the difference array
    diff = [0] * (n + 1)
    
    # Process all segments
    for i, (l, r) in enumerate(segments):
        diff[l-1] += 1
        diff[r] -= 1
    
    # Calculate the prefix sum of the difference array
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i+1] = prefix_sum[i] + diff[i]
    
    # Find the minimum and maximum values in the prefix sum
    min_val = min(prefix_sum[:n])
    max_val = max(prefix_sum[:n])
    
    # Calculate the maximum possible difference
    max_diff = max_val - min_val
    
    # Find the segments to apply
    applied_segments = []
    for i, (l, r) in enumerate(segments):
        if prefix_sum[l-1] == max_val and prefix_sum[r] == min_val:
            applied_segments.append(i + 1)
    
    # Print the results
    print(max_diff)
    print(len(applied_segments))
    if applied_segments:
        print(*applied_segments)

# Read input
n, m = map(int, input().split())
a = list(map(int, input().split()))
segments = [tuple(map(int, input().split())) for _ in range(m)]

# Call the solve function
solve(n, m, a, segments)