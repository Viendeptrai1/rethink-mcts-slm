import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        n = int(next(iterator))
    except StopIteration:
        return

    points = []
    for _ in range(n):
        x = float(next(iterator))
        y = float(next(iterator))
        points.append((x, y))

    if n == 0:
        print(0)
        return
    if n == 1:
        print(1)
        return

    # We need to find a line that intersects the maximum number of circles (radius 1).
    # A line intersects a circle if the distance from the center to the line is <= 1.
    # The optimal line can be rotated until it becomes tangent to one of the circles.
    # For each circle, there are two "critical" angles where the line is tangent to it.
    # Specifically, if we fix a circle i, the optimal line passing through it (or tangent to it)
    # that maximizes intersections will be one of the lines tangent to circle i.
    # Actually, the standard approach for this problem (maximum points covered by a line of width 2)
    # is to consider the angular intervals of lines that intersect each circle.
    # However, a simpler geometric transformation is:
    # A line intersects circle i if and only if the distance from center i to the line <= 1.
    # This is equivalent to saying the line passes through the annulus centered at i with inner radius 0 and outer radius 2? No.
    # Let's reframe: We are looking for a line L. Circle i is hit if dist(center_i, L) <= 1.
    # Consider the set of all lines tangent to circle i. There are infinitely many, but the "critical" events
    # happen when the line is tangent to circle i.
    # Actually, the standard solution for "maximum number of circles intersected by a line" involves:
    # For each pair of circles (i, j), compute the common external and internal tangents.
    # These tangents define candidate lines. Also, for each circle, any line tangent to it is a candidate.
    # But checking all pairs of tangents is O(N^2). With N=100, N^2 = 10000, which is fine.
    # Wait, the number of tangents between two circles is up to 4. So 4 * 10000 = 40000 lines.
    # Checking 40000 lines against 100 circles is 4 million operations, which is well within time limits for Python.
    
    # Let's implement the pair-wise tangent approach.
    # For every pair of circles (i, j):
    # 1. If they are far apart, there are 2 external tangents and 2 internal tangents.
    # 2. If they are close/overlapping, there are 2 external tangents and 0 internal tangents.
    # 3. If they are identical, infinite tangents, but we can skip or handle as a special case (just take one).
    # 4. Also, we must consider lines that are tangent to a single circle and don't necessarily touch another.
    #    However, the maximum set of intersected circles will always have a line that can be rotated 
    #    until it hits a circle at a tangent point without losing any other circle. 
    #    So checking all common tangents between all pairs is sufficient? 
    #    What if the optimal line only touches one circle? Then it's a tangent to that circle.
    #    But a tangent to a single circle is also a limit case of tangents between that circle and a "ghost" circle?
    #    Actually, the standard reduction is: The optimal line can be moved/rotated until it is tangent 
    #    to at least one circle. If it's tangent to only one, we can rotate it slightly until it hits 
    #    another circle or becomes tangent to another. If no other circle is close, then the count is 1.
    #    So we need to check:
    #    a) All common tangents between every pair (i, j).
    #    b) To be safe, we can also consider the case where the line is tangent to circle i and passes 
    #       through the center of circle i? No, that's not a tangent.
    #    Actually, the set of candidate lines is the set of all common tangents to every pair of circles.
    #    Is it possible the optimal line is tangent to only one circle and no other circle is tangent to it?
    #    Yes, if the max count is 1. But if max count >= 2, there exists a line tangent to at least two circles 
    #    (or one circle and the line is just grazing another).
    #    Wait, if the optimal line intersects k circles, we can rotate it until it becomes tangent to one of them.
    #    Then we can rotate it further until it becomes tangent to a second one (if k >= 2).
    #    So if the answer is >= 2, there exists a line tangent to at least two circles.
    #    Therefore, checking all common tangents between all pairs is sufficient for answer >= 2.
    #    For answer = 1, we can just output 1 (since n >= 1).
    #    Exception: If all circles are identical, any tangent works.
    
    # Algorithm:
    # 1. Initialize max_fruits = 1 (since n >= 1).
    # 2. For each pair (i, j) with i < j:
    #    Compute common tangents.
    #    For each tangent line, count how many circles it intersects.
    #    Update max_fruits.
    # 3. Print max_fruits.
    
    # How to compute tangents between two circles of radius R=1?
    # Let centers be C1=(x1, y1) and C2=(x2, y2).
    # Distance d = dist(C1, C2).
    # If d == 0: circles are identical. Skip (infinite tangents, covered by other pairs or single circle case).
    # If d < 2: circles overlap. Only external tangents exist (2 lines).
    # If d >= 2: 2 external and 2 internal tangents.
    
    # External tangents:
    # The line connecting the centers makes an angle theta = atan2(y2-y1, x2-x1).
    # The angle of the tangent relative to the center line is alpha = atan2(2*sqrt(R*R - (d/2)^2)? No.
    # For external tangents of equal radii R:
    # The tangent lines are parallel to the line connecting the centers? No, only if d=0.
    # Actually, for equal radii, the external tangents are symmetric with respect to the line of centers.
    # The angle of the tangent line with the x-axis is theta +/- beta, where sin(beta) = 0? No.
    # Let's derive:
    # Vector C1->C2 is (dx, dy). Length d.
    # The external tangents form a trapezoid (actually a rectangle if radii equal? No, the radii are parallel).
    # The distance between the two parallel lines (radii) is d. The tangents are parallel to the line connecting centers?
    # No. The external tangents for equal circles are parallel to the line connecting the centers ONLY if the circles are points? No.
    # Wait, if radii are equal, the external tangents are parallel to the line connecting the centers?
    # Imagine two circles side by side. The top external tangent goes from top of left to top of right.
    # The slope is the same as the line connecting centers. Yes!
    # So for equal radii, the two external tangents are parallel to the vector (dx, dy).
    # Their distance from the line of centers is 0? No.
    # The external tangents are the lines that pass "above" and "below" the segment connecting centers, parallel to it.
    # Wait, if they are parallel to the center line, then the distance from C1 to the line is 0? No.
    # Let's visualize. C1 at (0,0), C2 at (d, 0). Radii 1.
    # External tangents: y = 1 and y = -1. These are parallel to the x-axis (center line).
    # So yes, for equal radii, external tangents are parallel to the vector C1->C2.
    # There are two such lines.
    # How to get their equations?
    # Unit vector u = (dx/d, dy/d).
    # Perpendicular vector v = (-dy/d, dx/d).
    # The two external tangent lines are: P(t) = C1 + t*u + v  and P(t) = C1 + t*u - v?
    # No, the lines are offset from the center line by distance R=1 in the perpendicular direction.
    # Equation of line: (x - x1)*(-dy) - (y - y1)*(dx) = R * d? No.
    # Let's use the normal form.
    # Normal vector to the tangent lines is the perpendicular to the center line? No.
    # The tangent lines are parallel to the center line. So their normal is perpendicular to the center line.
    # Center line direction: (dx, dy). Normal: (-dy, dx).
    # The line equation: -dy * x + dx * y = C.
    # Distance from C1(x1, y1) to this line must be 1.
    # | -dy*x1 + dx*y1 - C | / sqrt(dx^2 + dy^2) = 1
    # | -dy*x1 + dx*y1 - C | = d
    # So -dy*x1 + dx*y1 - C = d  or  -dy*x1 + dx*y1 - C = -d
    # C = -dy*x1 + dx*y1 - d  or  C = -dy*x1 + dx*y1 + d
    # So we have two lines for external tangents.
    
    # Internal tangents (if d >= 2):
    # These cross between the circles.
    # For equal radii, the internal tangents intersect at the midpoint of C1 and C2.
    # The angle of the internal tangents with the center line is such that sin(phi) = R / (d/2) = 2/d.
    # So phi = arcsin(2/d).
    # The direction of the internal tangents is theta +/- phi.
    # Let's compute the lines explicitly.
    # Midpoint M = ((x1+x2)/2, (y1+y2)/2).
    # The internal tangents pass through M.
    # The angle of the line relative to the x-axis is theta + phi and theta - phi.
    # Where theta = atan2(dy, dx).
    # phi = arcsin(2/d).
    # So we have two lines passing through M with angles theta+phi and theta-phi.
    
    # Implementation details:
    # Represent a line by (A, B, C) such that Ax + By + C = 0.
    # Normalize so that A^2 + B^2 = 1? Or just keep as is and use distance formula.
    # Distance from (x0, y0) to Ax+By+C=0 is |Ax0+By0+C| / sqrt(A^2+B^2).
    # We need to check if this distance <= 1 + epsilon.
    
    # Let's code the tangent generation.
    
    def get_tangents(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        d2 = dx*dx + dy*dy
        d = math.sqrt(d2)
        
        if d < 1e-9:
            return [] # Identical centers, skip
        
        tangents = []
        
        # External tangents (always exist for equal radii)
        # Normal vector to the tangent lines is perpendicular to (dx, dy)
        # Normal n = (-dy, dx)
        # We want lines: -dy*x + dx*y + C = 0
        # Distance from p1 is 1.
        # |-dy*x1 + dx*y1 + C| / d = 1  => |-dy*x1 + dx*y1 + C| = d
        # Let K = -dy*x1 + dx*y1
        # K + C = d  => C = d - K
        # K + C = -d => C = -d - K
        # So two lines: -dy*x + dx*y + (d - K) = 0 and -dy*x + dx*y + (-d - K) = 0
        # Simplify: -dy*x + dx*y - K + d = 0 and -dy*x + dx*y - K - d = 0
        # Multiply by -1 to make it look nicer? Doesn't matter.
        
        K = -dy * x1 + dx * y1
        # Line 1: -dy*x + dx*y + (d - K) = 0
        # Line 2: -dy*x + dx*y + (-d - K) = 0
        # Note: A = -dy, B = dx, C = ...
        # To avoid large numbers, we can divide by d? No, keep integer-like precision.
        
        # External 1
        tangents.append((-dy, dx, d - K))
        # External 2
        tangents.append((-dy, dx, -d - K))
        
        # Internal tangents (only if d >= 2)
        if d >= 2.0 - 1e-9:
            # Pass through midpoint M
            mx = (x1 + x2) / 2.0
            my = (y1 + y2) / 2.0
            # Angle of center line
            theta = math.atan2(dy, dx)
            # Angle offset
            sin_phi = 2.0 / d
            # Clamp sin_phi to [-1, 1] just in case of floating point issues
            if sin_phi > 1.0: sin_phi = 1.0
            if sin_phi < -1.0: sin_phi = -1.0
            phi = math.asin(sin_phi)
            
            # Two angles: theta + phi, theta - phi
            ang1 = theta + phi
            ang2 = theta - phi
            
            # Line through M with angle ang:
            # Direction vector (cos(ang), sin(ang))
            # Normal vector (-sin(ang), cos(ang))
            # Equation: -sin(ang)*x + cos(ang)*y + C = 0
            # C = sin(ang)*mx - cos(ang)*my
            
            # Line 1
            A1 = -math.sin(ang1)
            B1 = math.cos(ang1)
            C1 = A1 * mx + B1 * my # Wait, Ax+By+C=0 => C = -(Ax0+By0). 
            # Let's re-verify: A*x + B*y + C = 0. At (mx, my): A*mx + B*my + C = 0 => C = - (A*mx + B*my).
            C1 = -(A1 * mx + B1 * my)
            tangents.append((A1, B1, C1))
            
            # Line 2
            A2 = -math.sin(ang2)
            B2 = math.cos(ang2)
            C2 = -(A2 * mx + B2 * my)
            tangents.append((A2, B2, C2))
            
        return tangents

    max_count = 1
    n_points = len(points)
    
    # Precompute all pairs tangents
    # To avoid duplicates, we can store lines as normalized tuples, but with floats it's tricky.
    # Given N=100, O(N^2) pairs, each generating up to 4 lines. Total lines ~ 40000.
    # Checking each line against 100 points is 4e6 ops. This is fast enough.
    # We don't need to deduplicate lines strictly, just check all.
    
    for i in range(n_points):
        for j in range(i + 1, n_points):
            tangents = get_tangents(points[i], points[j])
            for A, B, C in tangents:
                # Count intersections
                count = 0
                for k in range(n_points):
                    xk, yk = points[k]
                    # Distance = |Axk + Byk + C| / sqrt(A^2 + B^2)
                    # We need distance <= 1 + epsilon
                    val = abs(A * xk + B * yk + C)
                    norm = math.sqrt(A*A + B*B)
                    if norm < 1e-9:
                        # Line is degenerate (A=B=0), shouldn't happen
                        continue
                    dist = val / norm
                    if dist <= 1.0 + 1e-7:
                        count += 1
                if count > max_count:
                    max_count = count
    
    # Edge case: if n=1, loop doesn't run, max_count=1. Correct.
    # If all circles are same, loop runs, tangents generated, count will be n. Correct.
    
    print(max_count)

if __name__ == '__main__':
    solve()