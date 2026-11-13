def solve():
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
    
    # Calculate the initial max and min of the array
    initial_max = max(a)
    initial_min = min(a)
    initial_diff = initial_max - initial_min
    
    # If there are no segments, the max difference is just the initial difference
    if m == 0:
        print(initial_diff)
        print(0)
        return
    
    # We need to maximize the difference by applying some segments
    # The maximum possible difference is achieved by applying segments that cover the entire range
    # and have the largest negative effect on the initial min and positive effect on the initial max.
    
    # To find such segments, we can use a greedy approach:
    # 1. Find the segment that covers the entire range and has the largest negative effect on the initial min.
    # 2. Find the segment that covers the entire range and has the largest positive effect on the initial max.
    
    # We will use a prefix and suffix array to efficiently calculate the effect of segments.
    
    # Calculate the effect of each segment on the min and max
    min_effect = [0] * (n + 1)
    max_effect = [0] * (n + 1)
    
    for l, r in segments:
        min_effect[l - 1] -= 1
        if r < n:
            min_effect[r] += 1
        max_effect[l - 1] += 1
        if r < n:
            max_effect[r] -= 1
    
    # Calculate the prefix sums for min_effect and max_effect
    current_min_effect = 0
    current_max_effect = 0
    for i in range(n):
        current_min_effect += min_effect[i]
        current_max_effect += max_effect[i]
        min_effect[i] = current_min_effect
        max_effect[i] = current_max_effect
    
    # Find the segment that gives the maximum increase in max and maximum decrease in min
    best_min_segment = -1
    best_max_segment = -1
    best_min_increase = -float('inf')
    best_max_decrease = -float('inf')
    
    for i in range(m):
        l, r = segments[i]
        l -= 1
        r -= 1
        min_increase = min_effect[r] - (min_effect[l - 1] if l > 0 else 0)
        max_decrease = max_effect[r] - (max_effect[l - 1] if l > 0 else 0)
        
        if min_increase > best_min_increase:
            best_min_increase = min_increase
            best_min_segment = i
        
        if max_decrease > best_max_decrease:
            best_max_decrease = max_decrease
            best_max_segment = i
    
    # Calculate the new max and min after applying the best segments
    new_max = initial_max + best_max_decrease
    new_min = initial_min + best_min_increase
    new_diff = new_max - new_min
    
    # Output the result
    print(new_diff)
    print(2)
    print(best_min_segment + 1, best_max_segment + 1)