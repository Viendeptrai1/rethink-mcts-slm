def solve():
    MOD = 998244353
    N = int(input())
    points = [tuple(map(int, input().split())) for _ in range(N)]
    
    # Sort points by x-coordinate and y-coordinate
    points.sort()
    points.sort(key=lambda p: p[1])
    
    # Initialize result
    result = 0
    
    # Iterate through all possible subsets using bitmask
    for mask in range(1, 1 << N):
        # Find min and max x and y for current subset
        min_x = min(points[i][0] for i in range(N) if mask & (1 << i))
        max_x = max(points[i][0] for i in range(N) if mask & (1 << i))
        min_y = min(points[i][1] for i in range(N) if mask & (1 << i))
        max_y = max(points[i][1] for i in range(N) if mask & (1 << i))
        
        # Count points in rectangle
        count = 0
        for x, y in points:
            if min_x <= x <= max_x and min_y <= y <= max_y:
                count += 1
        
        # Add to result
        result = (result + count) % MOD
    
    print(result)

solve()