import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        p = int(next(iterator))
        q = int(next(iterator))
        
        projects = []
        for _ in range(n):
            a = int(next(iterator))
            b = int(next(iterator))
            projects.append((a, b))
    except StopIteration:
        return

    # If the target (p, q) is (0, 0), time is 0
    if p == 0 and q == 0:
        print(f"{0.0:.15f}")
        return

    # Check if any single project can satisfy the condition alone (though binary search will handle this, 
    # we need to ensure our hull logic works. Actually, the binary search approach with convex hull is general).
    
    # We will use binary search on the answer T.
    # For a fixed T, we need to check if (p, q) is in the convex hull of {(a_i * T, b_i * T)}.
    # This is equivalent to checking if (p/T, q/T) is in the convex hull of {(a_i, b_i)}.
    
    # Precompute the Convex Hull of the points (a_i, b_i).
    # Since we are in 2D, we can use Monotone Chain algorithm.
    
    points = []
    for a, b in projects:
        points.append((a, b))
    
    # Remove duplicates and sort
    points = sorted(list(set(points)))
    
    if len(points) == 1:
        # Only one unique project
        a, b = points[0]
        # Time needed = max(p/a, q/b)
        ans = max(p / a, q / b)
        print(f"{ans:.15f}")
        return

    # Monotone Chain to build Convex Hull
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    
    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    
    # Concatenate to get full hull (remove last point of each because it's repeated)
    hull = lower[:-1] + upper[:-1]
    
    # If the hull has only 1 or 2 points, it's a line segment or point.
    # The check function needs to handle this.
    
    def is_in_hull(target_x, target_y):
        # Check if point (target_x, target_y) is inside the convex hull of 'hull'
        # If hull has 1 point: check equality
        if len(hull) == 1:
            return abs(target_x - hull[0][0]) < 1e-9 and abs(target_y - hull[0][1]) < 1e-9
        
        # If hull has 2 points: check if on segment
        if len(hull) == 2:
            p1, p2 = hull
            # Check collinearity and bounds
            cross_prod = (p2[0] - p1[0]) * (target_y - p1[1]) - (p2[1] - p1[1]) * (target_x - p1[0])
            if abs(cross_prod) > 1e-9:
                return False
            # Check if between p1 and p2
            min_x, max_x = min(p1[0], p2[0]), max(p1[0], p2[0])
            min_y, max_y = min(p1[1], p2[1]), max(p1[1], p2[1])
            return min_x - 1e-9 <= target_x <= max_x + 1e-9 and min_y - 1e-9 <= target_y <= max_y + 1e-9
        
        # General case: Point is inside if it is on the same side of all edges (assuming counter-clockwise order)
        # Or simply, check if it lies to the left of every edge (or on the line) for a CCW hull.
        # Our Monotone Chain produces a CCW hull.
        # We check if the point is to the left (or on) of every edge.
        # However, due to floating point, we use a small epsilon.
        
        # Actually, a more robust way for point in convex polygon (CCW):
        # The point must be to the left of all edges.
        # But wait, if the point is outside, it will be to the right of at least one edge.
        # Let's verify orientation.
        
        # Check all edges
        for i in range(len(hull)):
            p1 = hull[i]
            p2 = hull[(i + 1) % len(hull)]
            # Cross product of (p2-p1) and (target-p1)
            cp = (p2[0] - p1[0]) * (target_y - p1[1]) - (p2[1] - p1[1]) * (target_x - p1[0])
            if cp < -1e-9: # Strictly to the right
                return False
        return True

    # Binary Search
    low = 0.0
    high = 1e18 # Sufficiently large upper bound (max p, q is 1e6, min a, b is 1, so max time is 1e6)
    # Actually max time could be 1e6 if a=1, p=1e6. But let's be safe.
    # If a=1, b=1, p=1e6, q=1e6 -> time = 1e6.
    # Let's set high to 2e6 to be safe, or even 1e9 to be absolutely sure.
    high = 1e9 
    
    # Optimization: If the origin (0,0) is not in the hull (which it isn't since a,b >= 1),
    # and we scale by T, the hull moves away from origin.
    # We are looking for smallest T such that (p, q) is in T * Hull.
    # Equivalent to (p/T, q/T) in Hull.
    
    # Check feasibility at high
    # If even at high T, (p, q) is not reachable, something is wrong, but given constraints a,b>=1, it's always reachable.
    
    for _ in range(100): # 100 iterations gives precision ~ 1e-30 relative to range
        mid = (low + high) / 2
        if mid == 0:
            low = mid
            continue
        
        tx = p / mid
        ty = q / mid
        
        if is_in_hull(tx, ty):
            high = mid
        else:
            low = mid
            
    print(f"{high:.15f}")

if __name__ == '__main__':
    solve()