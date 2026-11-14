import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    w = int(input_data[0])
    h = int(input_data[1])
    alpha_deg = int(input_data[2])
    
    alpha = math.radians(alpha_deg)
    
    if alpha == 0:
        print(f"{w * h:.9f}")
        return
    
    if alpha == math.pi:
        print(f"{w * h:.9f}")
        return
    
    # Half-widths and half-heights of the axis-aligned rectangle
    hw = w / 2.0
    hh = h / 2.0
    
    # Vertices of the axis-aligned rectangle (R1)
    r1 = [(hw, hh), (-hw, hh), (-hw, -hh), (hw, -hh)]
    
    # Vertices of the rotated rectangle (R2)
    r2 = []
    for x, y in r1:
        xr = x * math.cos(alpha) - y * math.sin(alpha)
        yr = x * math.sin(alpha) + y * math.cos(alpha)
        r2.append((xr, yr))
    
    # Function to check if a point (x, y) is inside the axis-aligned rectangle
    def in_r1(x, y):
        return -hw <= x <= hw and -hh <= y <= hh
    
    # Function to check if a point (x, y) is inside the rotated rectangle
    # We rotate the point back by -alpha and check against the axis-aligned bounds
    def in_r2(x, y):
        xr = x * math.cos(alpha) + y * math.sin(alpha)
        yr = -x * math.sin(alpha) + y * math.cos(alpha)
        return -hw <= xr <= hw and -hh <= yr <= hh
    
    # Collect all vertices of both rectangles that lie inside the other rectangle
    candidates = []
    for p in r1:
        if in_r2(p[0], p[1]):
            candidates.append(p)
    for p in r2:
        if in_r1(p[0], p[1]):
            candidates.append(p)
    
    # If no vertices are shared (only possible if one is completely inside the other, 
    # but since centers coincide and dimensions are same, this implies alpha=0 or 180 which we handled)
    # However, if one rectangle is strictly inside the other, the area is the area of the inner one.
    # But with same center and same dimensions, strict inclusion is impossible unless alpha=0.
    # The intersection polygon is convex. We need to find the intersection of the two convex polygons.
    # Since we have vertices of both, and the intersection is convex, we can compute the intersection polygon
    # by clipping one polygon against the half-planes of the other.
    
    # Let's use the Sutherland-Hodgman algorithm to clip R1 against the edges of R2.
    # R1 is the subject polygon, R2 defines the clipping region.
    
    def clip(subject_poly, clip_poly):
        output_list = subject_poly
        for i in range(len(clip_poly)):
            input_list = output_list
            output_list = []
            if not input_list:
                break
            
            A = input_list[-1]
            B = clip_poly[i]
            C = clip_poly[(i + 1) % len(clip_poly)]
            
            # Define the line from B to C
            # Line equation: (y - By) = m * (x - Bx)
            # Or in general form: ax + by + c = 0
            # Vector BC = (Cx - Bx, Cy - By)
            # Normal vector pointing inward? We need to check which side is inside.
            # The rectangle is convex. The interior is to the left of the edge if vertices are counter-clockwise.
            # Let's verify orientation of R2.
            # R1 vertices are (hw, hh), (-hw, hh), (-hw, -hh), (hw, -hh) -> CCW.
            # Rotation preserves orientation. So R2 is CCW.
            # So for edge B->C, the interior is to the left.
            
            dx = C[0] - B[0]
            dy = C[1] - B[1]
            
            # Function to check if point P is to the left of line BC
            # Cross product (C-B) x (P-B)
            def is_left(P):
                return (C[0] - B[0]) * (P[1] - B[1]) - (C[1] - B[1]) * (P[0] - B[0]) >= -1e-9
            
            for P in input_list:
                if is_left(P):
                    if not is_left(A):
                        # Entering the clip region: compute intersection
                        # Line AP intersects line BC
                        # Parametric form: P = A + t*(P-A)
                        # Intersection with line BC:
                        # We can use the ratio of cross products.
                        # t = dist(A, line BC) / dist(A, P) ? No.
                        # Using cross products:
                        # Let cp1 = cross(C-B, A-B)
                        # Let cp2 = cross(C-B, P-B)
                        # t = cp1 / (cp1 - cp2)
                        cp1 = (C[0] - B[0]) * (A[1] - B[1]) - (C[1] - B[1]) * (A[0] - B[0])
                        cp2 = (C[0] - B[0]) * (P[1] - B[1]) - (C[1] - B[1]) * (P[0] - B[0])
                        if abs(cp1 - cp2) < 1e-12:
                            continue
                        t = cp1 / (cp1 - cp2)
                        ix = A[0] + t * (P[0] - A[0])
                        iy = A[1] + t * (P[1] - A[1])
                        output_list.append((ix, iy))
                    output_list.append(P)
                elif is_left(A):
                    # Leaving the clip region: compute intersection
                    cp1 = (C[0] - B[0]) * (A[1] - B[1]) - (C[1] - B[1]) * (A[0] - B[0])
                    cp2 = (C[0] - B[0]) * (P[1] - B[1]) - (C[1] - B[1]) * (P[0] - B[0])
                    if abs(cp1 - cp2) < 1e-12:
                        continue
                    t = cp1 / (cp1 - cp2)
                    ix = A[0] + t * (P[0] - A[0])
                    iy = A[1] + t * (P[1] - A[1])
                    output_list.append((ix, iy))
            A = input_list[-1] if input_list else None
            # Note: The loop logic above for A update is slightly flawed in the standard implementation.
            # Let's rewrite the inner loop more carefully.
            
    # Re-implementing Sutherland-Hodgman cleanly
    def clip_polygon(subject, clip_edges):
        output = subject
        for edge in clip_edges:
            if not output:
                return []
            input_list = output
            output = []
            S = input_list[-1]
            for E in input_list:
                # Check if E is inside the half-plane defined by edge
                # Edge is from edge[0] to edge[1]
                # Inside is to the left
                def inside(P):
                    return (edge[1][0] - edge[0][0]) * (P[1] - edge[0][1]) - (edge[1][1] - edge[0][1]) * (P[0] - edge[0][0]) >= -1e-9
                
                if inside(E):
                    if not inside(S):
                        # Intersection
                        # Line SE intersects edge line
                        # S is outside, E is inside
                        # t = dist(S, line) / dist(S, E)
                        # Using cross products relative to edge start
                        cp_S = (edge[1][0] - edge[0][0]) * (S[1] - edge[0][1]) - (edge[1][1] - edge[0][1]) * (S[0] - edge[0][0])
                        cp_E = (edge[1][0] - edge[0][0]) * (E[1] - edge[0][1]) - (edge[1][1] - edge[0][1]) * (E[0] - edge[0][0])
                        if abs(cp_S - cp_E) < 1e-12:
                            continue
                        t = cp_S / (cp_S - cp_E)
                        ix = S[0] + t * (E[0] - S[0])
                        iy = S[1] + t * (E[1] - S[1])
                        output.append((ix, iy))
                    output.append(E)
                elif inside(S):
                    # Intersection
                    cp_S = (edge[1][0] - edge[0][0]) * (S[1] - edge[0][1]) - (edge[1][1] - edge[0][1]) * (S[0] - edge[0][0])
                    cp_E = (edge[1][0] - edge[0][0]) * (E[1] - edge[0][1]) - (edge[1][1] - edge[0][1]) * (E[0] - edge[0][0])
                    if abs(cp_S - cp_E) < 1e-12:
                        continue
                    t = cp_S / (cp_S - cp_E)
                    ix = S[0] + t * (E[0] - S[0])
                    iy = S[1] + t * (E[1] - S[1])
                    output.append((ix, iy))
                S = E
        return output

    # Generate edges of R2
    r2_edges = []
    n = len(r2)
    for i in range(n):
        r2_edges.append((r2[i], r2[(i+1)%n]))
    
    # Clip R1 against R2 edges
    intersection_poly = clip_polygon(r1, r2_edges)
    
    # Calculate area using shoelace formula
    if len(intersection_poly) < 3:
        print(f"{0.0:.9f}")
        return
    
    area = 0.0
    for i in range(len(intersection_poly)):
        j = (i + 1) % len(intersection_poly)
        area += intersection_poly[i][0] * intersection_poly[j][1]
        area -= intersection_poly[j][0] * intersection_poly[i][1]
    area = abs(area) / 2.0
    
    print(f"{area:.9f}")

if __name__ == "__main__":
    solve()