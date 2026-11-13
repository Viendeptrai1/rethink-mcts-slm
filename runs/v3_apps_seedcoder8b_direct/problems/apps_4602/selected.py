def min_total_distance():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    x = list(map(int, data[2:2+N]))
    
    min_distance = float('inf')
    
    for i in range(N):
        # Calculate distance if type-A robot is used
        distance_A = 2 * abs(x[i] - 0)
        # Calculate distance if type-B robot is used
        distance_B = 2 * abs(x[i] - K)
        # Find the minimum distance for the current ball
        min_distance = min(min_distance, distance_A, distance_B)
    
    print(min_distance)