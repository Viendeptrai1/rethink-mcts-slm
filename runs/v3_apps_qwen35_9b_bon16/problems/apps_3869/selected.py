import sys
import math

def solve():
    input_data = sys.stdin.read().strip().split()
    if not input_data:
        return
    w = int(input_data[0])
    h = int(input_data[1])
    alpha_deg = int(input_data[2])
    alpha = math.radians(alpha_deg)

    # If angle is 0 or 180, rectangles coincide perfectly
    if alpha_deg == 0 or alpha_deg == 180:
        print(f"{w * h:.9f}")
        return

    # Ensure alpha is in [0, 90] due to symmetry
    if alpha_deg > 90:
        alpha_deg = 180 - alpha_deg
        alpha = math.radians(alpha_deg)

    # Half-dimensions
    half_w = w / 2.0
    half_h = h / 2.0

    # We consider the first quadrant of the rotated rectangle.
    # The intersection area is 4 times the area in the first quadrant.
    # Let's analyze the intersection of the axis-aligned rectangle with the rotated one.
    
    # Define the four lines of the rotated rectangle in the global coordinate system.
    # The rotated rectangle has corners at:
    # R1: (w/2 * cos - h/2 * sin, w/2 * sin + h/2 * cos)
    # R2: (-w/2 * cos - h/2 * sin, -w/2 * sin + h/2 * cos)
    # R3: (-w/2 * cos + h/2 * sin, -w/2 * sin - h/2 * cos)
    # R4: (w/2 * cos + h/2 * sin, w/2 * sin - h/2 * cos)
    
    # But we can simplify by considering the equations of the lines forming the rotated rectangle.
    # The sides are lines passing through the origin with normals rotated by alpha and alpha+90.
    # Original sides (unrotated) are x = +/- w/2 and y = +/- h/2.
    # Rotated sides:
    # Side 1 (was x = w/2): rotated by alpha. Normal vector (cos a, sin a). Distance w/2 from origin.
    # Equation: x*cos(a) + y*sin(a) = w/2
    # Side 2 (was x = -w/2): x*cos(a) + y*sin(a) = -w/2
    # Side 3 (was y = h/2): rotated by alpha. Normal vector (-sin a, cos a). Distance h/2 from origin.
    # Equation: -x*sin(a) + y*cos(a) = h/2
    # Side 4 (was y = -h/2): -x*sin(a) + y*cos(a) = -h/2

    # The axis aligned rectangle is defined by:
    # -w/2 <= x <= w/2
    # -h/2 <= y <= h/2

    # Due to symmetry, the intersection area is 4 times the area in the first quadrant (x>=0, y>=0).
    # In the first quadrant, we are bounded by:
    # x >= 0, y >= 0
    # x <= w/2, y <= h/2
    # And the two "positive" half-planes of the rotated rectangle:
    # x*cos(a) + y*sin(a) <= w/2
    # -x*sin(a) + y*cos(a) <= h/2

    # Let's find the intersection points of the boundaries of the rotated rectangle with the axes or each other.
    # Actually, we can compute the vertices of the polygon formed by the intersection in the first quadrant.
    # The polygon is convex. Its vertices are a subset of:
    # (0,0)
    # (w/2, 0) if it satisfies rotated constraints
    # (0, h/2) if it satisfies rotated constraints
    # Intersection of x*cos(a) + y*sin(a) = w/2 and -x*sin(a) + y*cos(a) = h/2
    # Intersection of x*cos(a) + y*sin(a) = w/2 with y=0 (if within x bounds)
    # Intersection of -x*sin(a) + y*cos(a) = h/2 with x=0 (if within y bounds)
    # Intersection of x*cos(a) + y*sin(a) = w/2 with x=w/2 (unlikely to be the only constraint)
    # ... this manual case analysis is error prone.

    # Better approach:
    # The intersection of two convex polygons can be found by clipping.
    # However, since both are centered at origin and symmetric, we can just compute the area of the polygon
    # formed by the intersection of the two rectangles.
    # The vertices of the intersection polygon are the intersection points of the edges of the two rectangles.
    # There are at most 8 edges. We find all intersection points between edges of Rect1 and Rect2,
    # plus the vertices of Rect1 that are inside Rect2, and vice versa.
    # Then compute the convex hull area of these points.

    # Let's define the rectangles as lists of vertices.
    # Rect1 (axis aligned):
    # A: (w/2, h/2), B: (-w/2, h/2), C: (-w/2, -h/2), D: (w/2, -h/2)
    # Rect2 (rotated by alpha):
    # Rotate each point of Rect1 by alpha.
    
    def rotate(p, ang):
        x, y = p
        cx = x * math.cos(ang) - y * math.sin(ang)
        cy = x * math.sin(ang) + y * math.cos(ang)
        return (cx, cy)

    p1 = (w/2, h/2)
    p2 = (-w/2, h/2)
    p3 = (-w/2, -h/2)
    p4 = (w/2, -h/2)

    r_p1 = rotate(p1, alpha)
    r_p2 = rotate(p2, alpha)
    r_p3 = rotate(p3, alpha)
    r_p4 = rotate(p4, alpha)

    rect1_pts = [p1, p2, p3, p4]
    rect2_pts = [r_p1, r_p2, r_p3, r_p4]

    def point_in_rect(pt, w, h):
        x, y = pt
        return -w/2 <= x <= w/2 and -h/2 <= y <= h/2

    def point_in_rotated_rect(pt, w, h, ang):
        # Rotate point back by -ang and check against axis aligned
        x, y = pt
        # Rotate back
        xb = x * math.cos(-ang) - y * math.sin(-ang)
        yb = x * math.sin(-ang) + y * math.cos(-ang)
        return -w/2 <= xb <= w/2 and -h/2 <= yb <= h/2

    def line_intersect(p1, p2, p3, p4):
        # Intersection of line p1-p2 and p3-p4
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4
        
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 1e-9:
            return None
        
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
        
        if 0 <= t <= 1 and 0 <= u <= 1:
            ix = x1 + t * (x2 - x1)
            iy = y1 + t * (y2 - y1)
            return (ix, iy)
        return None

    points = []

    # Add vertices of Rect1 that are inside Rect2
    for pt in rect1_pts:
        if point_in_rotated_rect(pt, w, h, alpha):
            points.append(pt)

    # Add vertices of Rect2 that are inside Rect1
    for pt in rect2_pts:
        if point_in_rect(pt, w, h):
            points.append(pt)

    # Add intersection points of edges
    # Edges of Rect1
    edges1 = [(rect1_pts[i], rect1_pts[(i+1)%4]) for i in range(4)]
    # Edges of Rect2
    edges2 = [(rect2_pts[i], rect2_pts[(i+1)%4]) for i in range(4)]

    for e1 in edges1:
        for e2 in edges2:
            inter = line_intersect(e1[0], e1[1], e2[0], e2[1])
            if inter:
                points.append(inter)

    # Remove duplicates (approximate)
    unique_points = []
    for p in points:
        is_new = True
        for up in unique_points:
            if math.hypot(p[0]-up[0], p[1]-up[1]) < 1e-9:
                is_new = False
                break
        if is_new:
            unique_points.append(p)

    # Compute convex hull area using Shoelace formula
    # Since the points are symmetric and form a convex polygon centered at origin,
    # we just need to sort them angularly and apply shoelace.
    # However, simpler: since the intersection is convex, the set of points we collected
    # (vertices inside + intersections) are exactly the vertices of the intersection polygon.
    # We just need to order them.
    
    # Sort by angle
    def angle(p):
        return math.atan2(p[1], p[0])

    unique_points.sort(key=angle)

    def polygon_area(pts):
        n = len(pts)
        if n < 3:
            return 0.0
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += pts[i][0] * pts[j][1]
            area -= pts[j][0] * pts[i][1]
        return abs(area) / 2.0

    total_area = polygon_area(unique_points)
    print(f"{total_area:.9f}")

if __name__ == '__main__':
    solve()