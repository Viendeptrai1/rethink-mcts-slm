def has_self_intersections(n, points):
    # Sort the points based on their x-coordinates
    points.sort()
    
    # Check for overlaps between consecutive semi-circles
    for i in range(n - 1):
        x1, x2 = points[i], points[i + 1]
        # The range of the semi-circle formed by (x1, 0) and (x2, 0)
        range_start = min(x1, x2)
        range_end = max(x1, x2)
        
        # Check if the next semi-circle overlaps with the current one
        if i + 2 < n:
            x3 = points[i + 2]
            if min(x2, x3) < range_end:
                return "yes"
    
    return "no"

# Read input
n = int(input())
points = list(map(int, input().split()))

# Output the result
print(has_self_intersections(n, points))