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
    
    # We need to find the maximum possible difference
    # We can increase the max value and decrease the min value by applying segments
    # The maximum possible difference is achieved by applying segments to the max and min values
    
    # To find the best segments to apply, we need to find the segments that cover the max and min values
    max_segments = []
    min_segments = []
    
    for i, (l, r) in enumerate(segments):
        if a[l-1] == initial_max:
            max_segments.append(i + 1)
        if a[r-1] == initial_min:
            min_segments.append(i + 1)
    
    # We can choose any subset of max_segments and min_segments
    # The maximum possible difference is achieved by applying one segment from each set
    # If one set is empty, we just take the segments from the other set
    
    if max_segments and min_segments:
        # We can apply one segment from each set
        print(2 * initial_diff)
        print(2)
        print(max_segments[0], min_segments[0])
    elif max_segments:
        # We can only apply segments from max_segments
        print(initial_diff)
        print(1)
        print(max_segments[0])
    elif min_segments:
        # We can only apply segments from min_segments
        print(initial_diff)
        print(1)
        print(min_segments[0])
    else:
        # No segments can be applied
        print(initial_diff)
        print(0)