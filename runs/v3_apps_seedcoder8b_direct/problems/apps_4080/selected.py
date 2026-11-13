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
    
    # If there are no segments, the maximum difference is the initial difference
    if m == 0:
        print(initial_diff)
        print(0)
        return
    
    # We need to maximize the difference by applying some segments
    # The maximum possible difference is achieved by applying segments that cover the entire range
    # and have the largest negative and positive effect on the array.
    
    # We will use a greedy approach to find the segments that maximize the difference
    # We will sort the segments by their left endpoint, and then by their right endpoint
    segments.sort()
    
    # We will use a set to keep track of the segments we choose
    chosen_segments = set()
    
    # We will iterate through the segments and choose the ones that maximize the difference
    for i in range(m):
        l, r = segments[i]
        # Check if applying this segment increases the difference
        new_max = max(initial_max, a[l-1] - 1, a[r-1] - 1)
        new_min = min(initial_min, a[l-1] - 1, a[r-1] - 1)
        new_diff = new_max - new_min
        
        if new_diff > initial_diff:
            initial_diff = new_diff
            chosen_segments.add(i + 1)  # Store 1-based index
    
    # Output the result
    print(initial_diff)
    print(len(chosen_segments))
    if chosen_segments:
        print(' '.join(map(str, chosen_segments)))