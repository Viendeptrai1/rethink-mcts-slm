import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    w = int(input_data[0])
    h = int(input_data[1])
    alpha_deg = int(input_data[2])
    
    if alpha_deg == 0 or alpha_deg == 180:
        print(f"{w * h:.9f}")
        return
    
    alpha = math.radians(alpha_deg)
    
    # Half dimensions
    hw = w / 2.0
    hh = h / 2.0
    
    # If the rectangle is a square and angle is 45, we can use a specific formula,
    # but the general logic below covers it.
    
    # We need to find the intersection area of two rectangles centered at origin.
    # One is axis-aligned: [-w/2, w/2] x [-h/2, h/2]
    # The other is rotated by alpha.
    
    # The intersection of two convex polygons (rectangles) is a convex polygon.
    # Since both are centrally symmetric and centered at the same point, the intersection
    # is also centrally symmetric.
    
    # Strategy:
    # 1. Define the 4 vertices of the axis-aligned rectangle (R1).
    # 2. Define the 4 vertices of the rotated rectangle (R2).
    # 3. Compute the intersection polygon of R1 and R2 using the Sutherland-Hodgman algorithm
    #    or a simple clipping approach since we know the shapes.
    # 4. Calculate the area of the resulting polygon.
    
    # Vertices of R1 (counter-clockwise starting from bottom-left)
    r1 = [
        (-hw, -hh),
        (hw, -hh),
        (hw, hh),
        (-hw, hh)
    ]
    
    # Vertices of R2 (rotated by alpha)
    r2 = []
    for x, y in r1:
        xr = x * math.cos(alpha) - y * math.sin(alpha)
        yr = x * math.sin(alpha) + y * math.cos(alpha)
        r2.append((xr, yr))
    
    # Function to check if a point is inside a rectangle defined by center and half-dims
    # But here we will clip polygon P against the 4 lines of the other rectangle.
    
    def clip_polygon(poly, rect_center, rect_w, rect_h, angle):
        # rect_w, rect_h are full dimensions of the clipping rectangle
        # angle is the rotation of the clipping rectangle
        # We clip 'poly' against the 4 half-planes defined by the clipping rectangle
        
        # Define the 4 lines of the clipping rectangle
        # The clipping rectangle has corners:
        # c1: (-w/2, -h/2) rotated
        # c2: (w/2, -h/2) rotated
        # c3: (w/2, h/2) rotated
        # c4: (-w/2, h/2) rotated
        
        # Let's get the 4 lines in the form Ax + By + C <= 0
        # The 4 sides are:
        # 1. Left side (from c4 to c1)
        # 2. Bottom side (from c1 to c2)
        # 3. Right side (from c2 to c3)
        # 4. Top side (from c3 to c4)
        
        # Actually, easier: transform the polygon points into the local coordinate system of the clipping rectangle,
        # check bounds, then transform back? No, that changes the polygon shape if we just filter points.
        # We must clip edges.
        
        # Let's define the 4 lines explicitly.
        # Clipping rectangle corners in global coords:
        cw = rect_w / 2.0
        ch = rect_h / 2.0
        
        # Rotate the axis-aligned corners by 'angle' to get the global corners of the clipping rect
        corners = []
        for x, y in [(-cw, -ch), (cw, -ch), (cw, ch), (-cw, ch)]:
            rx = x * math.cos(angle) - y * math.sin(angle)
            ry = x * math.sin(angle) + y * math.cos(angle)
            corners.append((rx, ry))
        
        # Lines:
        # L1: from corners[0] to corners[1] (Bottom)
        # L2: from corners[1] to corners[2] (Right)
        # L3: from corners[2] to corners[3] (Top)
        # L4: from corners[3] to corners[0] (Left)
        
        def get_line(p1, p2):
            x1, y1 = p1
            x2, y2 = p2
            # Line equation: (y2-y1)x - (x2-x1)y + (x2-x1)y1 - (y2-y1)x1 = 0
            # Ax + By + C = 0
            A = y2 - y1
            B = -(x2 - x1)
            C = (x2 - x1) * y1 - (y2 - y1) * x1
            return A, B, C
        
        lines = [
            get_line(corners[0], corners[1]), # Bottom
            get_line(corners[1], corners[2]), # Right
            get_line(corners[2], corners[3]), # Top
            get_line(corners[3], corners[0])  # Left
        ]
        
        def eval_line(A, B, C, x, y):
            return A * x + B * y + C
        
        def clip(poly, A, B, C):
            new_poly = []
            if not poly:
                return new_poly
            for i in range(len(poly)):
                p1 = poly[i]
                p2 = poly[(i + 1) % len(poly)]
                v1 = eval_line(A, B, C, p1[0], p1[1])
                v2 = eval_line(A, B, C, p2[0], p2[1])
                
                if v1 <= 1e-9:
                    new_poly.append(p1)
                if v1 <= 1e-9 and v2 <= 1e-9:
                    pass # Both inside
                elif v1 > 1e-9 and v2 <= 1e-9:
                    # Entering the half-plane (from outside to inside)
                    # Intersection
                    t = v1 / (v1 - v2)
                    ix = p1[0] + t * (p2[0] - p1[0])
                    iy = p1[1] + t * (p2[1] - p1[1])
                    new_poly.append((ix, iy))
                elif v1 > 1e-9 and v2 > 1e-9:
                    pass # Both outside
                else: # v1 <= 1e-9 and v2 > 1e-9
                    # Exiting
                    t = v1 / (v1 - v2)
                    ix = p1[0] + t * (p2[0] - p1[0])
                    iy = p1[1] + t * (p2[1] - p1[1])
                    new_poly.append((ix, iy))
                    new_poly.append(p2)
            return new_poly

        current_poly = poly
        for A, B, C in lines:
            current_poly = clip(current_poly, A, B, C)
            if not current_poly:
                break
        return current_poly

    # Clip R1 against R2
    # R1 is the polygon to clip, R2 defines the clipping planes
    intersection_poly = clip_polygon(r1, (0,0), w, h, alpha)
    
    # Calculate area of polygon
    area = 0.0
    n = len(intersection_poly)
    if n < 3:
        print("0.0")
        return
    
    for i in range(n):
        x1, y1 = intersection_poly[i]
        x2, y2 = intersection_poly[(i + 1) % n]
        area += (x1 * y2 - x2 * y1)
    
    area = abs(area) / 2.0
    print(f"{area:.9f}")

if __name__ == "__main__":
    solve()