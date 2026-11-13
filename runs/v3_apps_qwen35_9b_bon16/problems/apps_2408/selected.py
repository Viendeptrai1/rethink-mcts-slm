import sys
from fractions import Fraction

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
    # Wires are defined by unique lines passing through at least two points.
    # If k points are collinear, they form 1 wire (line).
    # Total pairs of wires = C(total_lines, 2)
    # Minus pairs of wires that are parallel (never intersect).
    
    # Step 1: Identify all unique lines.
    # A line can be represented by ax + by + c = 0, with gcd(a,b,c) simplified.
    # Or more robustly, store a canonical representation.
    
    lines = set()
    
    # Iterate over all pairs to define lines
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            
            # Line equation: (y2-y1)x - (x2-x1)y + (x2-x1)y1 - (y2-y1)x1 = 0
            # A = y2 - y1
            # B = -(x2 - x1)
            # C = (x2 - x1)*y1 - (y2 - y1)*x1
            
            A = y2 - y1
            B = -(x2 - x1)
            C = (x2 - x1) * y1 - (y2 - y1) * x1
            
            # Simplify the line equation
            # Find GCD of A, B, C
            def gcd(a, b):
                while b:
                    a, b = b, a % b
                return abs(a)
            
            g = gcd(A, gcd(B, C))
            if g != 0:
                A //= g
                B //= g
                C //= g
            
            # Ensure a canonical sign: make the first non-zero among A, B positive
            # If A == 0 and B == 0, then points are same (impossible per problem)
            if A < 0 or (A == 0 and B < 0):
                A = -A
                B = -B
                C = -C
            
            lines.add((A, B, C))
    
    total_lines = len(lines)
    
    if total_lines < 2:
        print(0)
        return
    
    # Calculate total pairs
    total_pairs = total_lines * (total_lines - 1) // 2
    
    # Subtract pairs of parallel lines
    # Two lines A1x + B1y + C1 = 0 and A2x + B2y + C2 = 0 are parallel if A1/A2 == B1/B2
    # Since we normalized, we can just check if A1 == A2 and B1 == B2 (and lines are distinct, so C differs)
    
    parallel_count = 0
    # Group by (A, B)
    from collections import defaultdict
    groups = defaultdict(list)
    for line in lines:
        groups[(line[0], line[1])].append(line)
    
    for slope, group in groups.items():
        k = len(group)
        if k >= 2:
            parallel_count += k * (k - 1) // 2
    
    ans = total_pairs - parallel_count
    print(ans)

if __name__ == "__main__":
    solve()