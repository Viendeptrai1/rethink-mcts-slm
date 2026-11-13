import sys
from math import gcd

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    n = int(next(iterator))
    
    points = []
    for _ in range(n):
        x = int(next(iterator))
        y = int(next(iterator))
        points.append((x, y))
    
    # We need to find the number of pairs of wires that intersect.
    # A wire is defined by a unique line passing through at least two points.
    # If multiple points are collinear, they form a single wire.
    # Two wires intersect if they are not parallel.
    # However, we must be careful: if two wires share a point (i.e., they are not parallel but meet at one of the original poles),
    # do they count as intersecting? The problem says "whenever two different electric wires intersect".
    # In geometry, distinct non-parallel lines always intersect at exactly one point.
    # The only case where they don't intersect is if they are parallel.
    # So the problem reduces to: Count pairs of distinct lines such that they are not parallel.
    # But wait, what if the intersection point is not one of the poles? It still counts.
    # What if the intersection point is a pole? It still counts.
    # The only exception is if the lines are the same (which we handle by grouping collinear points).
    
    # Step 1: Identify all unique lines.
    # A line can be represented by (A, B, C) such that Ax + By + C = 0.
    # To handle collinearity and uniqueness, we can normalize the coefficients.
    # For two points (x1, y1) and (x2, y2):
    # A = y1 - y2
    # B = x2 - x1
    # C = -Ax1 - By1
    # Then divide A, B, C by gcd(|A|, |B|, |C|) and ensure a canonical sign (e.g., first non-zero is positive).
    
    lines = set()
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            
            A = y1 - y2
            B = x2 - x1
            C = -A * x1 - B * y1
            
            # Normalize
            common = gcd(A, gcd(B, C))
            if common != 0:
                A //= common
                B //= common
                C //= common
            
            # Canonical sign
            if A < 0 or (A == 0 and B < 0) or (A == 0 and B == 0 and C < 0):
                A = -A
                B = -B
                C = -C
            
            lines.add((A, B, C))
    
    # Now we have a set of unique lines.
    # We need to count pairs of lines that are not parallel.
    # Two lines (A1, B1, C1) and (A2, B2, C2) are parallel if A1*B2 == A2*B1.
    # Since they are distinct lines (different C or different A,B), if they are parallel, they never intersect.
    # If they are not parallel, they intersect at exactly one point.
    
    line_list = list(lines)
    count = 0
    num_lines = len(line_list)
    
    for i in range(num_lines):
        for j in range(i + 1, num_lines):
            A1, B1, _ = line_list[i]
            A2, B2, _ = line_list[j]
            
            # Check if parallel
            if A1 * B2 == A2 * B1:
                continue
            
            count += 1
            
    print(count)

if __name__ == '__main__':
    solve()