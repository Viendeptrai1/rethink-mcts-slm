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
    
    # To do this, we will track the effect of each segment on the min and max of the array
    min_effect = [0] * (n + 1)
    max_effect = [0] * (n + 1)
    
    for i, (l, r) in enumerate(segments):
        min_effect[l - 1] -= 1
        max_effect[r - 1] += 1
    
    # Calculate the cumulative effects
    current_min_effect = 0
    current_max_effect = 0
    for i in range(n):
        current_min_effect += min_effect[i]
        current_max_effect += max_effect[i]
        
        # Update the min and max of the array after applying the effects
        new_min = initial_min + current_min_effect
        new_max = initial_max + current_max_effect
        
        # Calculate the new difference
        new_diff = new_max - new_min
        
        # If the new difference is greater than the initial difference, update the result
        if new_diff > initial_diff:
            initial_diff = new_diff
            chosen_segments = [i + 1]  # Store 1-based index of the segment
    
    # Output the result
    print(initial_diff)
    print(len(chosen_segments))
    if chosen_segments:
        print(" ".join(map(str, chosen_segments)))
    else:
        print()