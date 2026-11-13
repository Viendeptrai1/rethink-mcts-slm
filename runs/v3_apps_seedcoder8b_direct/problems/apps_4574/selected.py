def max_rectangle_area():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    if N < 4:
        print(0)
        return
    
    A.sort()
    
    max_area = 0
    
    # We need to find the largest two distinct pairs of sides
    # The largest two sides will form the rectangle's sides
    for i in range(N - 1, 2, -1):
        for j in range(i - 1, 2, -1):
            # Check if we have at least two more distinct sides
            if A[i] != A[j]:
                # The largest two distinct sides are A[i] and A[j]
                # The second largest two distinct sides are A[i-1] and A[j-1]
                max_area = max(max_area, A[i] * A[j])
                break
    
    print(max_area)